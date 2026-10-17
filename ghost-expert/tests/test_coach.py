"""Rule-engine check with a fake world: no GPU, no models. Run: python -m tests.test_coach

A frame is JSON {"doing": k, "done": [...]}. The fake embedder says exactly which step a frame looks
like (one-hot); the fake Gemma reads the newest frame's truth. So any wrong event is the rule engine's fault.
"""
import json

import numpy as np

from app.coach import Coach, Config

PROC = json.load(open("procedures/loto-filter/procedure.json"))
IDS = [s["id"] for s in PROC["steps"]]
FPS = 4


def fake_embed(jpegs):
    doing = json.loads(jpegs[0])["doing"]
    return np.eye(len(IDS), dtype=np.float32)[[IDS.index(doing)]]


def fake_verify(confidence=0.9):
    def verify(procedure, sid, frames, keyframe):
        now = json.loads(frames[-1])
        return {"observed": "", "started": sid == now["doing"] or sid in now["done"],
                "done": sid in now["done"], "confidence": confidence}, 0.3
    return verify


def run(order, verify=None, cfg=None, secs_per_step=3):
    """Trainee does the steps in `order`, each for secs_per_step, then holds the final state 2 s."""
    coach = Coach(PROC, np.eye(len(IDS), dtype=np.float32), fake_embed, verify or fake_verify(), cfg=cfg or Config())
    events, done, t = [], [], 0.0
    for k in order:
        for _ in range(secs_per_step * FPS):
            events += coach.feed(t, json.dumps({"doing": k, "done": done}).encode())
            t += 1 / FPS
        done = done + [k]
    for _ in range(2 * FPS):
        events += coach.feed(t, json.dumps({"doing": order[-1], "done": done}).encode())
        t += 1 / FPS
    return coach, events


def kinds(events, *names):
    return [e for e in events if e.kind in names]


def test_clean_run_no_alarms():
    coach, events = run(IDS)
    assert not kinds(events, "interrupt", "hint", "ask"), kinds(events, "interrupt", "hint", "ask")
    assert coach.done == set(IDS) and kinds(events, "complete")


def test_skip_verify_zero_energy_interrupts_once_fast():
    _, events = run([1, 2, 3, 5, 6, 7, 8])
    stops = kinds(events, "interrupt")
    assert stops and stops[0].step == 4 and stops[0].at_step == 5, stops
    assert all(e.step == 4 for e in stops), "every later interrupt must still be about the skipped step 4"
    assert len([e for e in stops if e.at_step == 5]) == 1, "one interrupt per step, not one per frame"
    assert not kinds(events, "hint"), "a skipped safety step never downgrades to a hint"
    step5_start = 3 * 3.0
    assert stops[0].t - step5_start <= 1.0, f"interrupt {stops[0].t - step5_start:.2f}s after the mistake"


def test_unconfirmed_steps_are_rechecked_not_accused():
    # Heartbeat effectively off: every completion must be found by the re-check, never as an accusation.
    coach, events = run(IDS, cfg=Config(heartbeat_s=1e9))
    assert not kinds(events, "interrupt", "hint"), kinds(events, "interrupt", "hint")
    assert coach.done == set(IDS[:-1])  # the last step has no later step to trigger a re-check; heartbeat's job


def test_unsure_model_asks_instead_of_accusing():
    _, events = run([1, 2, 3, 5], verify=fake_verify(confidence=0.5))
    assert not kinds(events, "interrupt") and kinds(events, "ask")


def test_non_critical_skip_is_a_hint():
    _, events = run([1, 2, 3, 4, 5, 7, 8])
    assert not kinds(events, "interrupt")
    hints = kinds(events, "hint")
    assert hints and hints[0].step == 6 and hints[0].at_step == 7, hints


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
