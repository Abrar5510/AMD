# Ghost Expert

An expert films a procedure once. Ghost Expert turns it into steps, then watches a trainee do the job live through a camera and coaches them out loud. It stops them before a safety-critical mistake.

Everything runs on one AMD Instinct GPU: Gemma 3 (vision) served by vLLM on ROCm. Full plan: [../docs/13-ghost-expert-build-plan.md](../docs/13-ghost-expert-build-plan.md).

> Status: **Phase 4**: live coaching in the browser (camera → AMD GPU → voice + interrupt with the expert's clip). Authoring and replay evals work too.

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
- **Permission denied on `/dev/dri`:** add `render` under `group_add` in the `x-amd-gpu` block of `docker-compose.yml`.
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

## Phase 2: the coach, replayed (Gate 2)

How it decides ([app/coach.py](app/coach.py)):
- **Fast tier:** SigLIP embeds every frame and compares it with the expert's steps, to guess which step this looks like. It's cheap and can be wrong.
- **Slow tier:** Gemma verifies on a heartbeat (confirm the expected step), plus whenever the fast tier thinks the trainee jumped ahead.
- **Rule engine:** owns the state. A step is done only when Gemma confirms it. Before accusing anyone, it re-checks the skipped steps, newest first, because they may be done but not yet confirmed. Skipping a ⚠ step → interrupt; otherwise → hint. If Gemma is unsure, it asks instead of accusing.

Steps:
1. Copy the expert video to `procedures/loto-filter/expert.mp4` (gitignored). Set each step's `"expert_clip": [start_s, end_s]` in `procedure.json` to the seconds where the expert does it.
2. Build the reference embeddings (commit the resulting `refs.npy`):
   ```bash
   docker compose exec app python -m scripts.build_refs
   ```
   It prints the most similar pair of steps. Close to 1.0 means the fast tier will confuse them: make those steps look more different, or accept that Gemma does the work there.
3. Record trainee runs in `eval/runs/`: at least 5 clean runs and at least 3 that skip step 4. List them in `eval/runs.csv`:
   ```
   video,expect,error_t
   runs/clean1.mp4,,
   runs/skip4-a.mp4,interrupt:4,41.0
   ```
   `error_t` = the second the trainee starts the step they shouldn't (reaching for the cover screws).
4. Replay:
   ```bash
   docker compose exec app python -m scripts.run_eval eval/runs.csv
   ```

**Gate 2:** every skip-4 run is caught and the clean runs have zero false alarms. Tune the `COACH_*` knobs in `.env` (see `.env.example`), re-run, and write down the knobs that pass.

The rule engine has its own check with no GPU or models: `python -m tests.test_coach`.

## Phase 3: authoring (expert video → procedure)

1. **Draft:** Whisper turns the narration into sentences with word-level timing. SigLIP finds scene changes. Together they cut the video into segments. Gemma sees the narration and numbered contact sheets, one frame per segment, and groups the segments into steps with a title, instruction, visual check, safety flag and common mistake. Code repairs any gaps or overlaps in Gemma's grouping, so steps always cover the whole video in order.
2. **Expert edit:** open `http://<box>:8080/?id=loto-filter`. Fix titles and checks, flip ⚠, move a boundary to the playhead, split, merge or delete steps. Every change is saved and counted ("Expert edits: 2"; that's the Gate 3 number).
3. **Approve:** writes `procedure.json`, keyframes and `refs.npy`, which is everything the coach needs. No separate `build_refs` step is required.

In the browser: pick an id, choose the video, click **Upload & draft**, then edit and click **Approve**. From the command line on the box:
```bash
cp my-expert-video.mp4 procedures/loto-filter/expert.mp4
docker compose exec app python -m app.author procedures/loto-filter
docker compose exec app python -m app.author procedures/loto-filter --approve
```

**Narrate while you film.** Short sentences that start with "First / Next / Now / Then / Finally" (or "Poi / Ora / Infine") give the cleanest cuts.

**The app URL is public.** Set `APP_TOKEN` in `.env`: uploads, drafts, edits and approval then need it, and the page picks it up from `?token=...` in the URL. Uploads are capped at `MAX_UPLOAD_MB` (default 500).

**Gate 3 (plan Phase 3):** the LOTO video becomes a correct 8-step procedure after ≤3 edits.

Checks with no models: `python -m tests.test_author`.

## Phase 4: the live coach

Open `http://<box>:8080/coach?id=loto-filter&token=<APP_TOKEN>` on the demo laptop, click **Start camera**, and point it top-down at the work area.

- The browser sends 4 frames/s over a WebSocket. The server runs the coach on the newest frame. Frames that arrive while Gemma is thinking are kept for the verify window but not processed, so the session never falls behind.
- **Step rail** at the top (✓ done, ● current, ⚠ safety-critical). The **expert keyframe** and instruction for the current step are on the right.
- **Interrupt:** the live view turns red with a STOP banner, the voice says what was skipped, and the expert's clip of that step loops on the right until the trainee does it.
- **Voice:** the browser's built-in speech (Web Speech API). Pick a good system voice on the demo laptop (macOS "Premium" voices sound best).
- **Benchmark strip** at the bottom: GPU name, VRAM in use (including vLLM), frames/s, SigLIP ms, and Gemma p50/p95.
- **Presenter keys:** `Space` dismisses an interrupt, `N` marks the current step done, `R` resets the session.
- **Replay instead of the camera:** use the file picker, or put a recording at `procedures/<id>/run.mp4` and open `/coach?id=<id>&src=/files/<id>/run.mp4`. This is the stage fallback if the camera or lighting misbehaves.

**Gate 3 (plan Phase 4):** a teammate who hasn't seen the code does the task 3 times. The interrupt fires when they skip step 4, and never when they don't.

## License

MIT
