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
from concurrent.futures import ThreadPoolExecutor
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
    confirm: int = 2            # agreeing Gemma checks, on different frames, before an interrupt/hint fires
                                # or a safety-critical step counts as done...
    confirm_s: float = 3.0      # ...within this window (a single disagreeing answer doesn't reset them)
    n_frames: int = 4           # frames per verify call...
    gap_s: float = 0.5          # ...this far apart

    @classmethod
    def from_env(cls):
        return cls(**{k: type(v)(os.environ[f"COACH_{k.upper()}"])
                      for k, v in cls().__dict__.items() if f"COACH_{k.upper()}" in os.environ})


@dataclass
class Event:
    t: float                    # frame time that triggered the decision
    kind: str                   # done | override (presenter) | interrupt | hint | ask | complete
    step: int                   # the step the event is about (for interrupt/hint: the skipped step)
    text: str
    secs: float = 0.0           # Gemma time spent on this decision
    at_step: int | None = None  # interrupt/hint: the step the trainee jumped to
    observed: str = ""          # what Gemma said it saw: the explanation shown with the alert


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
        self.strikes = {}       # jumped-to step -> times of agreeing "skipped a step" checks
        self.done_votes = {}    # safety-critical step -> times of agreeing "done" checks
        self.completed = False
        self.seen = None        # latest {"step", "text"} Gemma reported, for the screen
        self.error = None       # latest verify failure, for the presenter
        self.pool = ThreadPoolExecutor(2)

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
        try:
            v, secs = self.verify(self.procedure, sid, frames, self.keyframes.get(sid))
        except Exception as e:  # vLLM down or slow: an unsure verdict never accuses, and the tick's other events survive
            self.error = f"{type(e).__name__}: {e}"
            return {"observed": "", "started": False, "done": False, "confidence": 0.0}, 0.0
        self.seen = {"step": sid, "text": v["observed"]}
        return v, secs

    def remember(self, t, jpeg):
        """Keep a frame for the verify window without processing it (live mode drops frames while Gemma runs)."""
        self.buf.append((t, jpeg))
        while self.buf[0][0] < t - self.cfg.gap_s * self.cfg.n_frames - 1:
            self.buf.popleft()

    def advance(self, t):
        """Presenter override: mark the expected step done (the demo must never get stuck on stage)."""
        sid = self.expected()
        if sid is None:
            return []
        self.done.add(sid)
        return [Event(t, "override", sid, f"Step {sid} marked done by the presenter.")]

    def feed(self, t, jpeg):
        cfg = self.cfg
        self.remember(t, jpeg)

        sims = self.refs @ self.embed([jpeg])[0]
        p = np.exp((sims - sims.max()) / cfg.temp)
        p /= p.sum()
        self.probs = p if self.probs is None else cfg.ema * self.probs + (1 - cfg.ema) * p

        events = []
        frames = self.window(t)
        guess = self.ids[int(self.probs.argmax())]
        expected = self.expected()
        jumped = (guess not in self.done and guess != expected and self.probs.max() >= cfg.enter_t)
        unsure = self._recent(self.strikes.get(guess), t) or any(self._recent(self.done_votes.get(a), t) for a in self.ancestors[guess])
        if jumped and (guess != self.last_guess or t - self.last_jump_check >= (cfg.gap_s if unsure else cfg.heartbeat_s)):
            self.last_jump_check = t
            events += self._check_jump(t, guess, frames)
        self.last_guess = guess

        expected = self.expected()
        beat_s = cfg.gap_s if self._recent(self.done_votes.get(expected), t) else cfg.heartbeat_s  # confirm a "done" on the next fresh frame
        if expected is not None and t - self.last_beat >= beat_s:
            self.last_beat = t
            v, secs = self._verify(expected, frames)
            events += self._done_vote(t, expected, v, secs)

        if not self.completed and self.expected() is None:
            self.completed = True
            events.append(Event(t, "complete", self.ids[-1], "Procedure complete. Well done."))
        return events

    def _recent(self, times, t):
        return bool(times) and t - times[-1] < self.cfg.confirm_s

    def _done_vote(self, t, sid, v, secs):
        """-> [done event] or []. A safety-critical step needs `confirm` agreeing checks on different frames:
        one confidently wrong "done" must never clear the step the trainee skipped."""
        if not (v["done"] and v["confidence"] >= self.cfg.confident_t):
            return []
        votes = [x for x in self.done_votes.get(sid, []) if t - x < self.cfg.confirm_s]
        self.done_votes[sid] = votes = votes if votes and votes[-1] == t else votes + [t]
        if self.steps[sid]["safety_critical"] and len(votes) < self.cfg.confirm:
            return []
        return [self._mark_done(t, sid, secs, v["observed"])]

    def _mark_done(self, t, sid, secs, observed=""):
        self.done.add(sid)
        return Event(t, "done", sid, f"Step {sid} done: {self.steps[sid]['title']}.", secs, observed=observed)

    def _check_jump(self, t, sid, frames):
        cfg, events = self.cfg, []
        skipped = [a for a in reversed(self.ancestors[sid]) if a not in self.done]  # newest first
        # The jumped-to step and the newest skipped one go to Gemma together (vLLM batches them):
        # one round trip on the interrupt path instead of two. Wasted only when the fast tier was wrong.
        first = list(self.pool.map(lambda s: self._verify(s, frames), [sid] + skipped[:1]))
        (v, secs), rechecks = first[0], first[1:]
        secs = max(s for _, s in first)
        if not v["started"] or v["confidence"] < cfg.ask_t:
            return events  # fast tier was wrong, or Gemma can't see: say nothing
        if v["confidence"] < cfg.confident_t:
            if sid not in self.asked:
                self.asked.add(sid)
                events.append(Event(t, "ask", sid, f"I can't quite see. Can you show me: {self.steps[sid]['visual_check']}?",
                                    secs, observed=v["observed"]))
            return events

        # Ask before accuse: re-check skipped steps, newest first. They may be done but not yet confirmed.
        blocker = None
        for m in skipped:
            if rechecks:
                vm, _ = rechecks.pop()
            else:
                vm, s2 = self._verify(m, frames)
                secs += s2
            if done := self._done_vote(t, m, vm, 0.0):
                events += done
            elif not self._recent(self.done_votes.get(m), t):
                blocker = m
                break
            else:
                return events  # looks done, waiting for its confirmation: don't accuse meanwhile

        if blocker is not None:
            # Skipping a safety step stays an interrupt even if the trainee has moved on to a harmless step.
            critical = self.steps[sid]["safety_critical"] or self.steps[blocker]["safety_critical"]
            kind = "interrupt" if critical else "hint"
            # One confidently wrong answer must not stop a trainee who is doing it right: wait for `confirm` agreeing checks.
            strikes = self.strikes[sid] = [x for x in self.strikes.get(sid, []) if t - x < cfg.confirm_s] + [t]
            if len(strikes) >= cfg.confirm and t - self.last_warned.get((kind, sid), float("-inf")) >= cfg.cooldown_s:
                strikes.clear()
                self.last_warned[(kind, sid)] = t
                b = self.steps[blocker]
                text = (f"Stop. You haven't done step {blocker}: {b['title']}. {b['instruction']}" if kind == "interrupt"
                        else f"Before this, step {blocker}: {b['title']}.")
                events.append(Event(t, kind, blocker, text, secs, at_step=sid, observed=v["observed"]))
        else:
            events += self._done_vote(t, sid, v, secs)
        return events
