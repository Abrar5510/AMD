"""Authoring: expert video -> draft procedure, then the expert edits and approves it.

    draft:   Whisper transcript + SigLIP change points -> candidate segments -> Gemma groups them into steps
    approve: the expert's edited draft -> procedure.json + keyframes + refs.npy (what the coach runs on)

CLI (no UI): python -m app.author procedures/loto-filter          # needs expert.mp4 in that folder
             python -m app.author procedures/loto-filter --approve
"""
import argparse
import io
import json
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from app.models import embed, transcribe
from app.prompts import AUTHOR_SCHEMA, author_messages
from app.video import audio, duration, frames, grab
from app.vlm import chat_json, data_url

FPS = 2
CUES = ("next", "now", "then", "step", "first", "finally", "after that", "and then",
        "poi", "ora", "adesso", "passo", "quindi", "infine", "dopo")
MAX_SEGMENTS = 72  # 8 contact sheets x 9 tiles, within vLLM's 8 images per prompt


def change_points(embs, times, window=4, min_gap_s=3.0, z=1.5):
    """Times where the scene changes: cosine distance between the mean frame before and after, peak-picked."""
    n = len(embs)
    scores = np.zeros(n)
    for i in range(window, n - window + 1):
        a, b = embs[i - window:i].mean(0), embs[i:i + window].mean(0)
        scores[i] = 1 - a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
    thr = scores.mean() + z * scores.std()
    picks = []
    for i in np.argsort(-scores):
        if scores[i] <= max(thr, 0):
            break
        if all(abs(times[i] - times[j]) >= min_gap_s for j in picks):
            picks.append(i)
    return sorted(float(times[i]) for i in picks)


def transcript_cues(segments, pause_s=1.5):
    """Times where the narration signals a new step: a cue word ("next", "poi"...) or a pause."""
    out, prev_end = [], None
    for s in segments:
        cue = s["text"].lower().lstrip(" .,-").startswith(CUES)
        paused = prev_end is not None and s["start"] - prev_end >= pause_s
        if cue or paused:
            out.append(float(s["start"]))
        prev_end = s["end"]
    return out


def boundaries(points, total_s, min_gap_s=2.0):
    """Cut points -> [(start, end)] segments covering 0..total_s, none shorter than min_gap_s."""
    # ponytail: the earliest point in each 2 s cluster wins; visual and narration cues aren't weighted.
    cuts = [0.0]
    for p in sorted(points):
        if p - cuts[-1] >= min_gap_s and total_s - p >= min_gap_s:
            cuts.append(round(p, 2))
    return list(zip(cuts, cuts[1:] + [round(total_s, 2)]))


def to_steps(raw_steps, segments):
    """Gemma's segment groups -> contiguous steps covering every segment, with clips and linear order."""
    n, steps, nxt = len(segments), [], 1
    for r in sorted(raw_steps, key=lambda r: r["first_segment"]):
        if nxt > n:
            break
        last = min(max(r["last_segment"], nxt), n)  # start where the previous step ended: no gaps, no overlaps
        steps.append({**{k: r[k] for k in ("title", "instruction", "visual_check", "safety_critical", "common_mistake")},
                      "segments": [nxt, last]})
        nxt = last + 1
    if steps and nxt <= n:
        steps[-1]["segments"][1] = n  # Gemma stopped early: the last step absorbs the rest
    for i, s in enumerate(steps, 1):
        s["id"] = i
        s["must_come_after"] = [i - 1] if i > 1 else []
        s["expert_clip"] = [segments[s["segments"][0] - 1][0], segments[s["segments"][1] - 1][1]]
    return steps


def contact_sheets(jpegs, tile=298):
    """Numbered 3x3 grids of keyframes, so Gemma sees every segment within the per-prompt image limit."""
    font = ImageFont.load_default(size=28)
    sheets = []
    for start in range(0, len(jpegs), 9):
        sheet = Image.new("RGB", (tile * 3, tile * 3))
        draw = ImageDraw.Draw(sheet)
        for k, j in enumerate(jpegs[start:start + 9]):
            img = Image.open(io.BytesIO(j)).convert("RGB")
            img.thumbnail((tile, tile))
            x, y = (k % 3) * tile, (k // 3) * tile
            sheet.paste(img, (x, y))
            draw.rectangle((x, y, x + 56, y + 40), fill=(255, 210, 0))
            draw.text((x + 8, y + 4), str(start + k + 1), fill=(0, 0, 0), font=font)
        buf = io.BytesIO()
        sheet.save(buf, "JPEG", quality=85)
        sheets.append(buf.getvalue())
    return sheets


def draft(proc_dir):
    """expert.mp4 in proc_dir -> draft.json (+ frames.npz for refs, keyframes/ for the edit screen)."""
    proc_dir = Path(proc_dir)
    video = proc_dir / "expert.mp4"
    timings, t0 = {}, time.perf_counter()

    total_s = duration(video)
    fr = list(frames(video, FPS))
    times = np.array([t for t, _ in fr])
    embs = embed([j for _, j in fr])
    timings["siglip_s"] = time.perf_counter() - t0

    t1 = time.perf_counter()
    samples = audio(video)
    transcript = transcribe(samples) if len(samples) else []
    timings["whisper_s"] = time.perf_counter() - t1

    cps = change_points(embs, times)
    segments = boundaries(cps + transcript_cues(transcript), total_s)
    if len(segments) > MAX_SEGMENTS:
        raise ValueError(f"{len(segments)} segments, max {MAX_SEGMENTS}: the video is too long or too busy")
    texts = [" ".join(s["text"] for s in transcript if a <= (s["start"] + s["end"]) / 2 < b) for a, b in segments]
    keyjpegs = [fr[int(np.abs(times - (a + b) / 2).argmin())][1] for a, b in segments]

    t2 = time.perf_counter()
    sheets = [data_url(s, max_side=896) for s in contact_sheets(keyjpegs)]
    out, _ = chat_json(author_messages(segments, texts, sheets), AUTHOR_SCHEMA, max_tokens=3000)
    timings["gemma_s"] = time.perf_counter() - t2
    steps = to_steps(out["steps"], segments)
    if not steps:
        raise ValueError("Gemma returned no steps")

    np.savez(proc_dir / "frames.npz", times=times, embs=embs)
    d = {"id": proc_dir.name, "title": out["title"], "approved": False, "edits": 0, "duration_s": total_s,
         "segments": segments, "change_points": cps, "transcript": transcript, "steps": steps,
         "timings": {k: round(v, 1) for k, v in {**timings, "total_s": time.perf_counter() - t0}.items()}}
    save_keyframes(proc_dir, d["steps"])
    (proc_dir / "draft.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return d


def save_keyframes(proc_dir, steps):
    kf_dir = Path(proc_dir) / "keyframes"
    kf_dir.mkdir(exist_ok=True)
    for s in steps:
        a, b = s["expert_clip"]
        (kf_dir / f"step{s['id']}.jpg").write_bytes(grab(Path(proc_dir) / "expert.mp4", (a + b) / 2))
        s["keyframe"] = f"keyframes/step{s['id']}.jpg"


def step_refs(embs, times, steps):
    """Mean SigLIP embedding of the frames inside each step's expert_clip, normalized. Rows in step order."""
    refs = []
    for s in steps:
        a, b = s["expert_clip"]
        inside = embs[(times >= a) & (times < b)]
        if not len(inside):
            raise ValueError(f"step {s['id']}: no frames between {a}s and {b}s")
        # ponytail: one mean vector per step; switch to nearest-frame matching if steps look alike on average.
        m = inside.mean(0)
        refs.append(m / np.linalg.norm(m))
    return np.stack(refs)


def check_steps(steps, total_s):
    """The expert's edits are untrusted input: reject anything the coach can't run on."""
    if not steps:
        raise ValueError("no steps")
    for i, s in enumerate(steps, 1):
        if not str(s.get("title", "")).strip() or not str(s.get("visual_check", "")).strip():
            raise ValueError(f"step {i}: title and visual check are required")
        a, b = s.get("expert_clip") or (None, None)
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and 0 <= a < b <= total_s + 0.5):
            raise ValueError(f"step {i}: clip must be start < end inside the video (0 to {total_s:.1f}s)")


def approve(proc_dir):
    """draft.json (as edited) -> procedure.json + keyframes + refs.npy. Returns the procedure."""
    proc_dir = Path(proc_dir)
    d = json.loads((proc_dir / "draft.json").read_text())
    check_steps(d["steps"], d["duration_s"])
    steps = []
    for i, s in enumerate(d["steps"], 1):
        steps.append({"id": i, "title": s["title"].strip(), "instruction": s.get("instruction", "").strip(),
                      "visual_check": s["visual_check"].strip(), "safety_critical": bool(s.get("safety_critical")),
                      "must_come_after": [i - 1] if i > 1 else [], "common_mistake": s.get("common_mistake", ""),
                      "expert_clip": [round(float(x), 2) for x in s["expert_clip"]]})
    save_keyframes(proc_dir, steps)
    npz = np.load(proc_dir / "frames.npz")
    np.save(proc_dir / "refs.npy", step_refs(npz["embs"], npz["times"], steps))
    procedure = {"id": d["id"], "title": d["title"], "approved_edits": d.get("edits", 0), "steps": steps}
    (proc_dir / "procedure.json").write_text(json.dumps(procedure, indent=2, ensure_ascii=False))
    d.update(approved=True, steps=[{**s, "segments": None} for s in steps])
    (proc_dir / "draft.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return procedure


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("proc_dir")
    p.add_argument("--approve", action="store_true")
    args = p.parse_args()
    if args.approve:
        proc = approve(args.proc_dir)
        print(f"approved {len(proc['steps'])} steps -> {args.proc_dir}/procedure.json, refs.npy")
    else:
        d = draft(args.proc_dir)
        print(json.dumps(d["timings"]), f"{len(d['segments'])} segments -> {len(d['steps'])} steps")
        for s in d["steps"]:
            print(f"  {s['id']}. [{s['expert_clip'][0]:.1f}-{s['expert_clip'][1]:.1f}s]"
                  f"{' ⚠' if s['safety_critical'] else ''} {s['title']}: {s['visual_check']}")
