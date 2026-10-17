#!/usr/bin/env python3
"""Phase 0 smoke test: can Gemma 3 on our AMD vLLM server see 4 images, return strict JSON, and how fast?

Each call has the shape of one live coach "verify" call: 4 frames in, a few tokens of JSON out.
The frames are synthetic with a known answer (count the red circles in each), so we check the
model really sees them, not just that it replies.

    python scripts/smoke_gemma.py --url http://localhost:8000 --runs 20

Exits non-zero if accuracy is under 90%. Prints a markdown row to paste into the README.
"""
import argparse
import base64
import io
import json
import os
import random
import time
import urllib.request

from PIL import Image, ImageDraw

PROMPT = (
    "You will see 4 images. In each image, count only the RED circles (ignore blue squares). "
    'Return JSON: {"counts": [n1, n2, n3, n4]}, one count per image, in order.'
)
SCHEMA = {
    "type": "object",
    "properties": {"counts": {"type": "array", "items": {"type": "integer"}, "minItems": 4, "maxItems": 4}},
    "required": ["counts"],
}


def frame(n_red, rng, size=512):
    """A 4x4 grid frame with n_red red circles and a couple of blue squares as distractors."""
    img = Image.new("RGB", (size, size), (40, 40, 40))
    draw = ImageDraw.Draw(img)
    cell, r = size // 4, size // 12
    cells = rng.sample(range(16), n_red + 2)
    for i, c in enumerate(cells):
        x, y = (c % 4) * cell + cell // 2, (c // 4) * cell + cell // 2
        if i < n_red:
            draw.ellipse((x - r, y - r, x + r, y + r), fill=(220, 30, 30))
        else:
            draw.rectangle((x - r, y - r, x + r, y + r), fill=(30, 60, 220))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def ask(url, model, api_key, images):
    content = [{"type": "text", "text": PROMPT}] + [{"type": "image_url", "image_url": {"url": u}} for u in images]
    body = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0,
        "max_tokens": 40,
        "response_format": {"type": "json_schema", "json_schema": {"name": "counts", "schema": SCHEMA}},
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(f"{url.rstrip('/')}/v1/chat/completions", json.dumps(body).encode(), headers)
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    return time.perf_counter() - t0, data


def pct(sorted_vals, q):
    return sorted_vals[min(len(sorted_vals) - 1, int(q * len(sorted_vals)))]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default=os.environ.get("VLLM_URL", "http://localhost:8000"))
    p.add_argument("--model", default=os.environ.get("MODEL", "google/gemma-3-12b-it"))
    p.add_argument("--runs", type=int, default=20)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    api_key = os.environ.get("VLLM_API_KEY")
    rng = random.Random(args.seed)

    print(f"model={args.model} url={args.url}")
    ask(args.url, args.model, api_key, [frame(1, rng)] * 4)  # warmup: first call compiles/caches, not counted

    latencies, correct, prompt_toks, out_toks = [], 0, [], []
    for i in range(args.runs):
        truth = [rng.randint(1, 4) for _ in range(4)]
        secs, data = ask(args.url, args.model, api_key, [frame(n, rng) for n in truth])
        text = data["choices"][0]["message"]["content"]
        try:
            got = json.loads(text)["counts"]
        except (json.JSONDecodeError, KeyError, TypeError):
            got = None
        ok = got == truth
        correct += ok
        latencies.append(secs)
        prompt_toks.append(data["usage"]["prompt_tokens"])
        out_toks.append(data["usage"]["completion_tokens"])
        print(f"run {i + 1:>2}: {secs * 1000:6.0f} ms  truth={truth} got={got if got is not None else text!r} {'ok' if ok else 'WRONG'}")

    lat = sorted(latencies)
    acc = correct / args.runs
    p50, p95 = pct(lat, 0.5), pct(lat, 0.95)
    out_tps = sum(out_toks) / sum(latencies)
    print(f"\naccuracy {correct}/{args.runs} = {acc:.0%} | p50 {p50 * 1000:.0f} ms | p95 {p95 * 1000:.0f} ms | "
          f"prompt {sum(prompt_toks) // len(prompt_toks)} tok/call | out {out_tps:.1f} tok/s end-to-end")
    print("\nREADME row:")
    print(f"| {args.model} | {args.runs} | {acc:.0%} | {p50 * 1000:.0f} | {p95 * 1000:.0f} | {sum(prompt_toks) // len(prompt_toks)} |")
    raise SystemExit(0 if acc >= 0.9 else 1)


if __name__ == "__main__":
    main()
