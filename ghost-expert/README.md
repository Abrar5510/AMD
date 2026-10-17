# Ghost Expert

An expert films a procedure once. Ghost Expert turns it into steps, then watches a trainee do the job live through a camera and coaches them out loud. It stops them before a safety-critical mistake.

Everything runs on one AMD Instinct GPU: Gemma 3 (vision) served by vLLM on ROCm. Full plan: [../docs/13-ghost-expert-build-plan.md](../docs/13-ghost-expert-build-plan.md).

> Status: **Phase 1**: the verify call (does Gemma see which step the trainee is on?). No live coaching yet.

## Run it on the AMD Developer Cloud box

1. Accept the Gemma license on Hugging Face ([gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it), and [27b-it](https://huggingface.co/google/gemma-3-27b-it) if you'll compare) and create a read token.
2. Configure:
   ```bash
   cp .env.example .env   # set HF_TOKEN
   ```
3. Start (the first start downloads about 24 GB of weights for 12B):
   ```bash
   docker compose up -d && docker compose logs -f vllm
   ```
4. GPU proof for the slides (take a screenshot):
   ```bash
   docker compose exec vllm python3 -c "import torch; print(torch.cuda.get_device_name(0))"
   ```
   `rocm-smi` on the host shows VRAM in use.
5. Check the app can reach the model:
   ```bash
   curl localhost:8080/health
   ```
6. Smoke test (4 images per call, strict JSON, latency):
   ```bash
   docker compose exec app python scripts/smoke_gemma.py --url http://vllm:8000 --runs 20
   ```
7. Repeat with `MODEL=google/gemma-3-27b-it` in `.env` (`docker compose up -d` again) and add both rows below.

From your laptop, vLLM stays private behind an SSH tunnel: `ssh -L 8000:localhost:8000 <user>@<box>`, then run the smoke test locally with `pip install pillow` and `--url http://localhost:8000`.

## If it breaks

- **`rocm/vllm:latest` won't start, or Gemma 3 vision errors:** try a tagged image from [hub.docker.com/r/rocm/vllm/tags](https://hub.docker.com/r/rocm/vllm/tags) via `VLLM_IMAGE` in `.env`. Once one works, pin that tag.
- **`--limit-mm-per-prompt` rejected:** older vLLM wants `image=8` instead of the JSON form. Edit it in `docker-compose.yml`.
- **Permission denied on `/dev/dri`:** add `render` under `group_add`.
- **Out of memory:** lower `MAX_MODEL_LEN` or raise `GPU_MEM_UTIL`.

## Phase 0 results

Gate: accuracy ≥ 90% and the p95 latency number is known. Under about 1500 ms keeps the live interrupt viable.

| Model | Runs | Accuracy | p50 ms | p95 ms | Prompt tok/call |
|-------|------|----------|--------|--------|-----------------|
| _fill in from `smoke_gemma.py`_ | | | | | |

## Phase 1: the verify call (Gate 1)

The risky core: given 4 frames and a step, Gemma returns `{observed, started, done, confidence}` as strict JSON. Don't build any UI until this passes.

1. **Build the props and film** (plan §2) with the top-down camera you'll demo with. Put the videos in `eval/runs/` (gitignored):
   - `expert1.mp4`: the expert doing all 8 steps in order, narrating.
   - 3 to 5 trainee runs, each with one mistake: skip step 4, skip step 3, steps 5 and 6 swapped.
2. **Label clips.** Watch each video and write down moments: the second of the newest frame, the step, and whether it is started/done at that moment. Copy `eval/verify_labels.example.csv` to `eval/verify_labels.csv`. Aim for at least 40 rows, covering every step in both done and not-done states, and lots of steps 2 and 4.
3. **Optional expert keyframes:** save one frame per step, then set that step's `"keyframe"` to `"keyframes/step2.jpg"` in [procedures/loto-filter/procedure.json](procedures/loto-filter/procedure.json):
   ```bash
   ffmpeg -ss 14.5 -i eval/runs/expert1.mp4 -frames:v 1 procedures/loto-filter/keyframes/step2.jpg
   ```
   Run the eval with and without keyframes and keep whichever scores higher.
4. **Run:**
   ```bash
   docker compose exec app python -m scripts.eval_verify eval/verify_labels.csv
   ```
   Debug one clip with `--video eval/runs/skip4.mp4 --t 41 --step 5`.

**Gate 1:** at least 90% of clips right, and steps 2 and 4 (marked ⚠) right. If it fails, try these in order: bigger and more saturated props, a dark tablecloth, moving the camera closer to the work area, adding keyframes, and `gemma-3-27b-it`. Re-run after each change.

## License

MIT
