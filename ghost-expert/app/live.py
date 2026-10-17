"""Live coaching session over a WebSocket.

Browser -> server: binary frames = 8-byte little-endian float64 timestamp (s) + JPEG bytes, ~4 fps.
                   text = {"cmd": "advance" | "reset"} (presenter hotkeys).
Server -> browser: {"type": "tick", "events": [...], "state": {...}, "stats": {...}} after every processed frame.

Gemma can take ~1 s, so frames that arrive meanwhile are not processed. The newest frame is processed next,
and the skipped ones are still kept for the verify window. The coach only ever runs in one worker thread.
"""
import asyncio
import json
import struct
import time
from collections import deque
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch
from fastapi import WebSocket
from fastapi.concurrency import run_in_threadpool

from app.coach import Coach, Config
from app.models import embed
from app.vlm import verify


def p(sorted_vals, q):
    return sorted_vals[min(len(sorted_vals) - 1, int(q * len(sorted_vals)))] if sorted_vals else None


class Stats:
    """Benchmark panel numbers: what the AMD GPU is doing, live."""

    def __init__(self):
        self.siglip, self.gemma, self.ticks = deque(maxlen=200), deque(maxlen=200), deque(maxlen=100)
        self.gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU (no GPU found)"

    def timed_embed(self, jpegs):
        t0 = time.perf_counter()
        out = embed(jpegs)
        self.siglip.append(time.perf_counter() - t0)
        return out

    def timed_verify(self, *args):
        verdict, secs = verify(*args)
        self.gemma.append(secs)
        return verdict, secs

    def summary(self):
        now = time.perf_counter()
        recent = [t for t in self.ticks if now - t < 10]
        g = sorted(self.gemma)
        out = {"gpu": self.gpu, "fps": round(len(recent) / 10, 1),
               "siglip_ms": round(1000 * p(sorted(self.siglip), 0.5)) if self.siglip else None,
               "gemma_p50_ms": round(1000 * p(g, 0.5)) if g else None,
               "gemma_p95_ms": round(1000 * p(g, 0.95)) if g else None, "gemma_calls": len(self.gemma)}
        if torch.cuda.is_available():
            free, total = torch.cuda.mem_get_info()  # device-wide: includes the vLLM process
            out["vram_gb"] = f"{(total - free) / 2**30:.0f} / {total / 2**30:.0f}"
        return out


def load(proc_dir: Path):
    procedure = json.loads((proc_dir / "procedure.json").read_text())
    refs = np.load(proc_dir / "refs.npy")
    keyframes = {s["id"]: proc_dir / s["keyframe"] for s in procedure["steps"] if s.get("keyframe")}
    return procedure, refs, keyframes


def state(coach: Coach):
    return {"done": sorted(coach.done), "expected": coach.expected(), "complete": coach.completed,
            "guess": coach.ids[int(coach.probs.argmax())] if coach.probs is not None else None,
            "guess_p": round(float(coach.probs.max()), 2) if coach.probs is not None else None}


async def run_session(ws: WebSocket, proc_dir: Path):
    procedure, refs, keyframes = load(proc_dir)
    stats = Stats()
    cfg = Config.from_env()

    def new_coach():
        return Coach(procedure, refs, stats.timed_embed, stats.timed_verify, keyframes, cfg)

    session = {"coach": new_coach(), "latest": None, "skipped": [], "cmds": []}
    wake = asyncio.Event()

    async def receive():
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                return
            if msg.get("bytes"):
                b = msg["bytes"]
                if len(b) <= 8:
                    continue
                if session["latest"] is not None:
                    session["skipped"].append(session["latest"])
                session["latest"] = (struct.unpack("<d", b[:8])[0], b[8:])
            elif msg.get("text"):
                cmd = json.loads(msg["text"]).get("cmd")
                if cmd in ("advance", "reset"):
                    session["cmds"].append(cmd)
            wake.set()

    def step(coach, cmds, skipped, frame):
        """Runs in the worker thread: everything that touches the coach."""
        events = []
        for cmd in cmds:
            if cmd == "advance":
                events += coach.advance(frame[0] if frame else 0.0)
        for f in skipped:
            coach.remember(*f)
        if frame:
            events += coach.feed(*frame)
        return events

    async def process():
        while True:
            await wake.wait()
            wake.clear()
            cmds, session["cmds"] = session["cmds"], []
            if "reset" in cmds:
                session["coach"], session["skipped"] = new_coach(), []
                cmds = [c for c in cmds if c != "reset"]
                await ws.send_json({"type": "reset"})
            frame, session["latest"] = session["latest"], None
            skipped, session["skipped"] = session["skipped"], []
            coach = session["coach"]
            try:
                events = await run_in_threadpool(step, coach, cmds, skipped, frame)
            except Exception as e:  # e.g. vLLM down: tell the presenter, keep the session alive
                await ws.send_json({"type": "error", "message": f"{type(e).__name__}: {e}"})
                continue
            if frame:
                stats.ticks.append(time.perf_counter())
            await ws.send_json({"type": "tick", "t": frame[0] if frame else None,
                                "events": [asdict(e) for e in events], "state": state(coach), "stats": stats.summary()})

    await ws.send_json({"type": "hello", "procedure": procedure, "state": state(session["coach"]), "stats": stats.summary()})
    worker = asyncio.create_task(process())
    try:
        await receive()
    finally:
        worker.cancel()
