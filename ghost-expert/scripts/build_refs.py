"""Build the fast tier's reference embeddings: one mean SigLIP embedding per step of the expert video.

Needs "expert_clip": [start_s, end_s] on every step of procedure.json (set by hand). Authoring (app/author.py) builds refs.npy itself on approve; use this after hand edits.

    python -m scripts.build_refs --procedure procedures/loto-filter/procedure.json
Writes refs.npy next to procedure.json, rows in step order.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from app.author import FPS, step_refs
from app.models import embed
from app.video import frames


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--procedure", default="procedures/loto-filter/procedure.json")
    p.add_argument("--video", help="default: expert.mp4 next to procedure.json")
    args = p.parse_args()
    proc_path = Path(args.procedure)
    procedure = json.loads(proc_path.read_text())
    video = Path(args.video) if args.video else proc_path.parent / "expert.mp4"

    missing = [s["id"] for s in procedure["steps"] if not s.get("expert_clip")]
    if missing:
        raise SystemExit(f"set expert_clip [start_s, end_s] in {proc_path} for steps {missing}")

    fr = list(frames(video, FPS))
    refs = step_refs(embed([j for _, j in fr]), np.array([t for t, _ in fr]), procedure["steps"])
    print(f"{len(fr)} frames embedded")

    # How separable are the steps? Off-diagonal similarity close to 1.0 means the fast tier can't tell them apart.
    sims = refs @ refs.T
    np.fill_diagonal(sims, -1)
    worst = np.unravel_index(sims.argmax(), sims.shape)
    print(f"most similar pair: steps {procedure['steps'][worst[0]]['id']} and "
          f"{procedure['steps'][worst[1]]['id']} at {sims.max():.3f}")
    np.save(proc_path.parent / "refs.npy", refs)
    print(f"wrote {proc_path.parent / 'refs.npy'} {refs.shape}")


if __name__ == "__main__":
    main()
