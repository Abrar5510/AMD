"""Gate 2: replay recorded trainee runs through the full coach (SigLIP + Gemma + rule engine).

Runs CSV (video paths relative to the CSV):
    video,expect,error_t
    runs/clean1.mp4,,
    runs/skip4.mp4,interrupt:4,41.0
expect = the event that should fire, and for which skipped step (interrupt:N or hint:N); empty for clean runs.
error_t = second when the trainee starts the step they shouldn't (e.g. reaches for the cover screws).

    python -m scripts.run_eval eval/runs.csv

Gate 2 passes when every interrupt run is caught and clean runs have zero false alarms.
Latency = decision time after error_t, counting Gemma time (replay runs the slow tier inline).
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

from app.coach import Coach, Config
from app.models import embed
from app.video import frames
from app.vlm import MODEL, verify

FPS = 4  # what the live camera stream will send


def replay(video, procedure, refs, keyframes, cfg):
    coach = Coach(procedure, refs, embed, verify, keyframes, cfg)
    events = []
    for t, jpeg in frames(video, FPS):
        for e in coach.feed(t, jpeg):
            events.append(e)
            print(f"  {t:6.1f}s {e.kind:<9} step {e.step} ({e.secs * 1000:.0f} ms) {e.text}")
    return coach, events


def score(events, expect, error_t):
    """-> (caught or None, latency_s or None, false_alarms)"""
    stops = [e for e in events if e.kind == "interrupt"]
    if not expect:
        return None, None, len(stops)
    kind, step = expect.split(":")
    hit = next((e for e in events if e.kind == kind and e.step == int(step) and e.t >= error_t - 1), None)
    # Repeats about the truly skipped step (trainee kept going) are correct, not false alarms.
    false_alarms = len([e for e in stops if e.step != int(step) or e.t < error_t - 1])
    return hit is not None, (hit.t + hit.secs - error_t) if hit else None, false_alarms


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("runs", nargs="?", default="eval/runs.csv")
    p.add_argument("--procedure", default="procedures/loto-filter/procedure.json")
    args = p.parse_args()
    proc_path = Path(args.procedure)
    procedure = json.loads(proc_path.read_text())
    refs = np.load(proc_path.parent / "refs.npy")
    keyframes = {s["id"]: proc_path.parent / s["keyframe"] for s in procedure["steps"] if s.get("keyframe")}
    cfg = Config.from_env()
    runs_csv = Path(args.runs)
    with runs_csv.open() as f:
        rows = list(csv.DictReader(f))
    print(f"model={MODEL} runs={len(rows)} cfg={cfg}")

    results = []
    for row in rows:
        print(f"\n{row['video']} expect={row['expect'] or 'clean'}")
        coach, events = replay(runs_csv.parent / row["video"], procedure, refs, keyframes, cfg)
        error_t = float(row["error_t"]) if row["error_t"] else None
        caught, latency, fa = score(events, row["expect"], error_t)
        results.append((row, caught, latency, fa, len(coach.done)))

    print("\n| Run | Expect | Caught | Latency s | False alarms | Steps done |\n|---|---|---|---|---|---|")
    for row, caught, latency, fa, n_done in results:
        print(f"| {row['video']} | {row['expect'] or 'clean'} | {'' if caught is None else 'yes' if caught else 'NO'} | "
              f"{'' if latency is None else f'{latency:.2f}'} | {fa} | {n_done}/{len(procedure['steps'])} |")

    must_catch = [r for r in results if r[0]["expect"].startswith("interrupt")]
    clean = [r for r in results if not r[0]["expect"]]
    caught_all = all(r[1] for r in must_catch)
    clean_fa = sum(r[3] for r in clean)
    lat = sorted(r[2] for r in must_catch if r[2] is not None)
    print(f"\ninterrupts caught {sum(bool(r[1]) for r in must_catch)}/{len(must_catch)} | "
          f"false alarms on clean runs {clean_fa} | all false alarms {sum(r[3] for r in results)}"
          + (f" | latency median {lat[len(lat) // 2]:.2f}s worst {lat[-1]:.2f}s" if lat else ""))
    if not (must_catch and clean):
        raise SystemExit("GATE 2 FAIL: needs at least one interrupt run and one clean run")
    ok = caught_all and clean_fa == 0
    print("GATE 2 PASS" if ok else "GATE 2 FAIL")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
