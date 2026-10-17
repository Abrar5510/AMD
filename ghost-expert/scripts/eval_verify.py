"""Gate 1: does the verify call get step state right on hand-labeled clips?

Labels CSV (video paths relative to the CSV):
    video,t,step,started,done
    runs/expert1.mp4,14.5,2,1,1
t = second of the newest frame (the 4 frames are t-1.5, t-1, t-0.5, t). started/done = 0 or 1.

    python -m scripts.eval_verify eval/verify_labels.csv
One clip, for debugging:
    python -m scripts.eval_verify --video eval/runs/skip4.mp4 --t 41 --step 5

Exits non-zero if fewer than 90% of clips are fully right (both started and done).
"""
import argparse
import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path

from app.vlm import MODEL, verify

N_FRAMES, GAP_S = 4, 0.5  # same window the live coach will send


def grab(video, t):
    """One JPEG frame at second t."""
    r = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(video),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-"],
        capture_output=True,
    )
    if r.returncode or not r.stdout:
        raise ValueError(f"no frame at {t:.1f}s in {video} (past the end?) {r.stderr.decode().strip()[-200:]}")
    return r.stdout


def clip(video, t):
    return [grab(video, t - GAP_S * (N_FRAMES - 1 - i)) for i in range(N_FRAMES)]


def keyframe(proc_dir, procedure, step_id):
    kf = next(s for s in procedure["steps"] if s["id"] == step_id).get("keyframe")
    return proc_dir / kf if kf else None


def pct(sorted_vals, q):
    return sorted_vals[min(len(sorted_vals) - 1, int(q * len(sorted_vals)))]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("labels", nargs="?")
    p.add_argument("--procedure", default="procedures/loto-filter/procedure.json")
    p.add_argument("--video")
    p.add_argument("--t", type=float)
    p.add_argument("--step", type=int)
    args = p.parse_args()
    proc_path = Path(args.procedure)
    procedure = json.loads(proc_path.read_text())

    if args.video:
        verdict, secs = verify(procedure, args.step, clip(args.video, args.t), keyframe(proc_path.parent, procedure, args.step))
        print(json.dumps(verdict, indent=2), f"\n{secs * 1000:.0f} ms")
        return
    if not args.labels:
        p.error("give a labels CSV, or --video/--t/--step")

    labels = Path(args.labels)
    per_step = defaultdict(lambda: [0, 0])  # step -> [right, total]
    latencies, unsure = [], 0
    with labels.open() as f:
        rows = list(csv.DictReader(f))
    print(f"model={MODEL} clips={len(rows)}")
    for row in rows:
        step = int(row["step"])
        want = {"started": row["started"] == "1", "done": row["done"] == "1"}
        verdict, secs = verify(procedure, step, clip(labels.parent / row["video"], float(row["t"])),
                               keyframe(proc_path.parent, procedure, step))
        ok = verdict["started"] == want["started"] and verdict["done"] == want["done"]
        per_step[step][0] += ok
        per_step[step][1] += 1
        latencies.append(secs)
        unsure += verdict["confidence"] < 0.4
        print(f"{'ok   ' if ok else 'WRONG'} {row['video']} t={row['t']} step={step} want={want} "
              f"got=started:{verdict['started']} done:{verdict['done']} conf={verdict['confidence']:.2f} "
              f"{secs * 1000:.0f}ms | {verdict['observed']}")

    right = sum(r for r, _ in per_step.values())
    acc = right / len(rows)
    lat = sorted(latencies)
    critical = {s["id"] for s in procedure["steps"] if s["safety_critical"]}
    print("\n| Step | Right | Total |\n|------|-------|-------|")
    for step in sorted(per_step):
        r, n = per_step[step]
        print(f"| {step}{' ⚠' if step in critical else ''} | {r} | {n} |")
    print(f"\naccuracy {right}/{len(rows)} = {acc:.0%} | unsure (conf<0.4) {unsure} | "
          f"p50 {pct(lat, 0.5) * 1000:.0f} ms | p95 {pct(lat, 0.95) * 1000:.0f} ms")
    print("GATE 1 PASS" if acc >= 0.9 else "GATE 1 FAIL: see the README's Phase 1 fixes")
    raise SystemExit(0 if acc >= 0.9 else 1)


if __name__ == "__main__":
    main()
