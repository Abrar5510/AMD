"""The coach: fast tier (SigLIP, every frame) + slow tier (Gemma verify) + a deterministic rule engine.

The rule engine owns the truth. A step is done only when Gemma confirms it. The fast tier only decides
*when* to ask Gemma: a heartbeat confirms the expected next step, and whenever the fast tier thinks the
trainee has jumped ahead, Gemma checks that step and re-checks the skipped ones before anyone gets accused.

    coach = Coach(procedure, refs, embed, verify)
    for t, jpeg in stream:
        for event in coach.feed(t, jpeg): ...
"""
import os
from collections import deque
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Config:
    """Calibration knobs. Tune on the eval set at the venue, not on paper."""
    enter_t: float = 0.5        # fast-tier probability that counts as "looks like step k"
    confident_t: float = 0.6    # Gemma confidence needed to mark done or to accuse
    ask_t: float = 0.4          # between ask_t and confident_t: ask the trainee instead of accusing
    temp: float = 0.02          # softmax temperature over SigLIP similarities (all frames look alike, so small)
    ema: float = 0.6            # weight of the past in the fast-tier smoothing
    heartbeat_s: float = 2.0    # how often Gemma confirms the expected step
    cooldown_s: float = 8.0     # don't repeat the same interrupt/hint within this window
    n_frames: int = 4           # frames per verify call...
    gap_s: float = 0.5          # ...this far apart

    @classmethod
    def from_env(cls):
        return cls(**{k: type(v)(os.environ[f"COACH_{k.upper()}"])
                      for k, v in cls().__dict__.items() if f"COACH_{k.upper()}" in os.environ})


@dataclass
class Event:
    t: float                    # frame time that triggered the decision
    kind: str                   # done | interrupt | hint | ask | complete
    step: int                   # the step the event is about (for interrupt/hint: the skipped step)
    text: str
    secs: float = 0.0           # Gemma time spent on this decision
    at_step: int | None = None  # interrupt/hint: the step the trainee jumped to


@dataclass
class Coach:
    procedure: dict
    refs: np.ndarray            # [n_steps, d], rows in step order (scripts/build_refs.py)
    embed: callable             # list[jpeg] -> [n, d] normalized embeddings
    verify: callable            # (procedure, step_id, frames, keyframe) -> (verdict, secs)
    keyframes: dict = field(default_factory=dict)  # step_id -> image path
    cfg: Config = field(default_factory=Config)

    def __post_init__(self):
        self.steps = {s["id"]: s for s in self.procedure["steps"]}
        self.ids = [s["id"] for s in self.procedure["steps"]]
        assert len(self.refs) == len(self.ids), "refs.npy doesn't match the procedure, rebuild it"
        self.ancestors = {sid: sorted(self._ancestors(sid)) for sid in self.ids}
        self.done, self.asked = set(), set()
        self.buf = deque()
        self.probs = None
        self.last_beat = self.last_jump_check = float("-inf")
        self.last_guess = None
        self.last_warned = {}   # (kind, at_step) -> t
        self.completed = False

    def _ancestors(self, sid):
        out = set()
        for parent in self.steps[sid]["must_come_after"]:
            out |= {parent} | self._ancestors(parent)
        return out

    def expected(self):
        return next((sid for sid in self.ids if sid not in self.done), None)

    def window(self, t):
        """The n_frames frames closest to t - gap*(n-1) ... t."""
        targets = [t - self.cfg.gap_s * (self.cfg.n_frames - 1 - i) for i in range(self.cfg.n_frames)]
        return [min(self.buf, key=lambda f: abs(f[0] - x))[1] for x in targets]

    def _verify(self, sid, frames):
        return self.verify(self.procedure, sid, frames, self.keyframes.get(sid))

    def feed(self, t, jpeg):
        cfg = self.cfg
        self.buf.append((t, jpeg))
        while self.buf[0][0] < t - cfg.gap_s * cfg.n_frames - 1:
            self.buf.popleft()

        sims = self.refs @ self.embed([jpeg])[0]
        p = np.exp((sims - sims.max()) / cfg.temp)
        p /= p.sum()
        self.probs = p if self.probs is None else cfg.ema * self.probs + (1 - cfg.ema) * p

        events = []
        frames = self.window(t)
        guess = self.ids[int(self.probs.argmax())]
        expected = self.expected()
        jumped = (guess not in self.done and guess != expected and self.probs.max() >= cfg.enter_t)
        if jumped and (guess != self.last_guess or t - self.last_jump_check >= cfg.heartbeat_s):
            self.last_jump_check = t
            events += self._check_jump(t, guess, frames)
        self.last_guess = guess

        if t - self.last_beat >= cfg.heartbeat_s and (expected := self.expected()) is not None:
            self.last_beat = t
            v, secs = self._verify(expected, frames)
            if v["done"] and v["confidence"] >= cfg.confident_t:
                events.append(self._mark_done(t, expected, secs))

        if not self.completed and self.expected() is None:
            self.completed = True
            events.append(Event(t, "complete", self.ids[-1], "Procedure complete. Well done."))
        return events

    def _mark_done(self, t, sid, secs):
        self.done.add(sid)
        return Event(t, "done", sid, f"Step {sid} done: {self.steps[sid]['title']}.", secs)

    def _check_jump(self, t, sid, frames):
        cfg, events = self.cfg, []
        v, secs = self._verify(sid, frames)
        if not v["started"] or v["confidence"] < cfg.ask_t:
            return events  # fast tier was wrong, or Gemma can't see: say nothing
        if v["confidence"] < cfg.confident_t:
            if sid not in self.asked:
                self.asked.add(sid)
                events.append(Event(t, "ask", sid, f"I can't quite see. Can you show me: {self.steps[sid]['visual_check']}?", secs))
            return events

        # Ask before accuse: re-check skipped steps, newest first. They may be done but not yet confirmed.
        blocker = None
        for m in reversed([a for a in self.ancestors[sid] if a not in self.done]):
            vm, s2 = self._verify(m, frames)
            secs += s2
            if vm["done"] and vm["confidence"] >= cfg.confident_t:
                events.append(self._mark_done(t, m, 0.0))
            else:
                blocker = m
                break

        if blocker is not None:
            # Skipping a safety step stays an interrupt even if the trainee has moved on to a harmless step.
            critical = self.steps[sid]["safety_critical"] or self.steps[blocker]["safety_critical"]
            kind = "interrupt" if critical else "hint"
            if t - self.last_warned.get((kind, sid), float("-inf")) >= cfg.cooldown_s:
                self.last_warned[(kind, sid)] = t
                b = self.steps[blocker]
                text = (f"Stop. You haven't done step {blocker}: {b['title']}. {b['instruction']}" if kind == "interrupt"
                        else f"Before this, step {blocker}: {b['title']}.")
                events.append(Event(t, kind, blocker, text, secs, at_step=sid))
        elif v["done"]:
            events.append(self._mark_done(t, sid, secs))
        return events
