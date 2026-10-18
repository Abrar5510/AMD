# Ghost Expert

**Your best technician retires next year, and everything she knows leaves with her. She films one job, once. Ghost Expert watches every new hire do it, coaches them out loud, flags the step they skip, and hands their supervisor a training record.**

Four models on one AMD Instinct GPU: Gemma 3 vision (vLLM on ROCm), SigLIP, Whisper, Kokoro. Full plan: [../docs/13-ghost-expert-build-plan.md](../docs/13-ghost-expert-build-plan.md).

## The 3-minute demo

1. **Author (0:15).** The expert's narrated video goes in. Whisper, SigLIP and Gemma cut it into 8 steps with keyframes, a visual check and a safety flag on each. The expert fixes what's wrong and approves. *The expert owns the procedure; the AI only drafts it.*
2. **Coach (0:35).** A judge does the lockout/tagout job under a top-down camera. Steps turn green as Gemma confirms them, and the voice says what's next.
3. **The stop (1:10).** The judge reaches for the cover screws without testing that the machine is dead. The whole screen goes red, the voice says *"Stop. Hold on, you skipped step 4"*, the banner says what the coach saw, and the expert's own hands doing step 4 fill half the screen until the judge does it.
4. **"Where does the filter go?" (1:40).** Hold to ask. The answer is spoken and the expert's clip of that moment plays.
5. **Training record (2:05).** Time per step against the expert, the mistakes caught, a *Competent* or *Needs another run* verdict, and a printable PDF.

If the live take misfires on stage, say "that's why we measure it" and switch to the replay: `/coach?id=loto-filter&src=/files/loto-filter/run.mp4`.

## Why it isn't "just a prompt"

A vision model is sometimes confidently wrong. If one wrong answer can stop a trainee, a correct trainee gets yelled at. So the model never decides alone:

- **SigLIP** (every frame, ~10 ms) only guesses which step this looks like, to decide *when* to ask Gemma.
- **Gemma 3** checks the guessed step and the newest skipped step *in parallel*: one round trip on the stop path.
- **A deterministic rule engine** owns the state. A STOP needs **two agreeing Gemma checks on different frames**. A safety-critical step counts as done only after two agreeing checks, so one wrong "done" can never clear the step the trainee skipped. Unsure → it asks ("can you show me the tag?") instead of accusing. Model down or slow → it stays quiet; it never accuses on a missing answer.

Stress test with a deliberately bad model, where Gemma is confidently wrong 5% of the time and SigLIP is wrong on 25% of frames ([eval/sim_results.md](eval/sim_results.md), `python -m scripts.sim_eval`):

| | Skipped step 4 caught | Correct trainees falsely stopped | Stop latency p50 |
|---|---|---|---|
| One Gemma answer decides | 98% | **14%** | 0.8 s |
| Ghost Expert rule engine | 92% | **0%** | 1.6 s |

The rule engine gives up 6 points of catch rate to remove every false stop, because a coach that wrongly stops correct trainees soon gets ignored. That's a simulation of the design, not a measurement of Gemma. The filmed numbers are below.

## Results

| Number | Value | How |
|---|---|---|
| Verify accuracy, 4 frames + keyframe (Gate 1) | _pending: run on the AMD box_ | `scripts.eval_verify` |
| Skip-4 caught / false alarms on clean runs (Gate 2) | _pending_ | `scripts.run_eval` |
| Gemma 3 12B verify latency p50 / p95, MI300X | _pending_ | `scripts.smoke_gemma` |
| Rule engine under a 5%-wrong model | 92% caught, 0% false stops | `scripts.sim_eval` |

Save each run's output for the slides, e.g. `... python -m scripts.run_eval eval/runs.csv | tee eval/results.md`.

> Status: **Phase 5** is built: authoring, live coaching with voice questions, bilingual coaching (English/Italian) and the training record. Next: film the props, then run Gates 1 and 2 on the GPU box.

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
- **Rule engine:** owns the state. A step is done only when Gemma confirms it (twice, on different frames, for a ⚠ step). Before accusing anyone, it re-checks the skipped steps, newest first, because they may be done but not yet confirmed. Skipping a ⚠ step → interrupt; otherwise → hint. Either fires only after `COACH_CONFIRM` (default 2) agreeing checks within `COACH_CONFIRM_S`. If Gemma is unsure, it asks instead of accusing. A failed or slow Gemma call (`VERIFY_TIMEOUT_S`) counts as unsure.

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

The rule engine has its own check with no GPU or models: `python -m tests.test_coach`. To see how a knob trades catch rate against false alarms before tuning at the venue, run `COACH_CONFIRM=1 python -m scripts.sim_eval`.

## Phase 3: authoring (expert video → procedure)

1. **Draft:** Whisper turns the narration into sentences with word-level timing. SigLIP finds scene changes. Together they cut the video into segments. Gemma sees the narration and numbered contact sheets, one frame per segment, and groups the segments into steps with a title, instruction, visual check, safety flag and common mistake. Code repairs any gaps or overlaps in Gemma's grouping, so steps always cover the whole video in order.
2. **Expert edit:** open `http://<box>:8080/?id=loto-filter`. Fix titles and checks, flip ⚠, move a boundary to the playhead, split, merge or delete steps. Every change is saved and counted ("Expert edits: 2"; that's the Gate 3 number).
3. **Approve:** writes `procedure.json`, keyframes and `refs.npy`, which is everything the coach needs. No separate `build_refs` step is required.

In the browser: pick an id, choose the video, click **Upload and draft** (or pick an existing draft below the form), then select a step to edit it and click **Approve**. **Open coach →** appears once it's approved.

**Try it yourself:** `/?try` (plus `&token=...` when `APP_TOKEN` is set) is the same flow for a visitor: it hides the id and other procedures and gives each visitor their own `try-…` id, so an investor can film anything on their phone and be coached through it.

From the command line on the box:
```bash
cp my-expert-video.mp4 procedures/loto-filter/expert.mp4
docker compose exec app python -m app.author procedures/loto-filter
docker compose exec app python -m app.author procedures/loto-filter --approve
```

**Narrate while you film.** Short sentences that start with "First / Next / Now / Then / Finally" (or "Poi / Ora / Infine") give the cleanest cuts.

**The app URL is public.** Set `APP_TOKEN` in `.env`: uploads, drafts, edits and approval then need it, and the page picks it up from `?token=...` in the URL. Uploads are capped at `MAX_UPLOAD_MB` (default 500).

**Gate 3 (plan Phase 3):** the LOTO video becomes a correct 8-step procedure after ≤3 edits.

Checks with no models: `python -m tests.test_author`.

**Kokoro on a Mac (local dev only):** the bundled espeak-ng has a broken data path on macOS. Run `brew install espeak-ng` and set `ESPEAK_DATA_PATH=/opt/homebrew/share/espeak-ng-data`. Kokoro also needs Python ≤ 3.12 and `python -m spacy download en_core_web_sm`. The Docker image handles all of this. If espeak is broken, the app logs "Kokoro unavailable" and uses browser speech: espeak exits instead of raising an error, so each language is tested in a child process first and the server stays up.

## Phase 4: the live coach

Open `http://<box>:8080/coach?id=loto-filter&token=<APP_TOKEN>` on the demo laptop, click **Start camera**, and point it top-down at the work area.

- The browser sends 4 frames/s over a WebSocket. The server runs the coach on the newest frame. Frames that arrive while Gemma is thinking are kept for the verify window but not processed, so the session never falls behind.
- **Setup screen** first: the procedure, the coaching language and **Start camera** (or *replay a recording*). Nothing else until the session starts.
- **Step bar** at the top (green done, yellow current, red triangle = safety-critical). The current step's instruction and the **expert keyframe** are on the right. The coach's spoken line shows as a subtitle on the live view.
- **Interrupt:** the whole screen gets a red frame, a STOP banner says which step was skipped and what the coach saw, the voice says it too, and the expert's clip of that step grows to half the screen and loops until the trainee does it.
- **What Gemma sees:** the top-right of the live view shows the model's latest observation ("Gemma · step 4: the hand is near the lamp…"), so the audience can watch it reason.
- **Voice:** Kokoro-82M on the AMD GPU (`af_heart` in English, `if_sara` in Italian). It warms up when the app starts and repeated lines are cached, so an interrupt you've heard before plays instantly. If Kokoro is missing, still warming up, slow (over 3 s) or broken, the page speaks that line with the browser's own voice and the session carries on. The benchmark strip shows `voice Kokoro N ms` or `voice browser`. Set `TTS=browser` in `.env` to skip Kokoro entirely.
- **Benchmark strip** along the bottom, kept quiet: GPU name, VRAM in use (including vLLM), frames/s, SigLIP ms, and Gemma p50/p95.
- **Presenter keys:** `Space` dismisses an interrupt, `N` marks the current step done, `R` resets the session.
- **Replay instead of the camera:** use the file picker, or put a recording at `procedures/<id>/run.mp4` and open `/coach?id=<id>&src=/files/<id>/run.mp4`. This is the stage fallback if the camera or lighting misbehaves.

**Gate 3 (plan Phase 4):** a teammate who hasn't seen the code does the task 3 times. The interrupt fires when they skip step 4, and never when they don't.

## Phase 5: "show me how", bilingual coaching, training record

- **Ask the expert:** hold **Hold to ask** (or hold `Q`) and ask out loud, e.g. "where does the new filter go?". Whisper transcribes the question. Gemma answers in at most two sentences, grounded in the procedure and the expert's narration from `draft.json`, and names the step whose clip shows the answer. The voice speaks the answer and the expert's clip of that step plays once (blue border). The text box next to the button is the fallback for a noisy room.
- **Bilingual:** pick **Italiano** before Start. Gemma translates the step texts once and caches them in `procedure.it.json` until the next approval. Spoken lines come from a small phrase table per language, so they never depend on a live model. Questions are answered in the coaching language.
- **Training record:** opens by itself when the procedure completes, or anytime via **Training record**. It shows the verdict (*Competent* only with zero safety stops and zero presenter overrides), trainee vs expert time per step, the mistakes caught, and the questions asked. The trainee's name goes at the top, and the verdict stays *Pending supervisor sign-off* until a supervisor signs it (the printout has a blank signature line if nobody has). **Print / PDF**, **Download JSON** and **Download xAPI** (statements for the plant's LMS: one per confirmed step and one for the procedure, with the supervisor as instructor) are on the record.
- **Phones and tablets:** the coach asks for the rear camera, so a phone propped over the work area is enough.

Endpoints: `POST /api/coach/<id>/ask?step=N&lang=en|it` (body: audio, or JSON `{"text": ...}`) and `POST /api/procedures/<id>/translate?lang=it`. Both need `X-App-Token` when `APP_TOKEN` is set.

## License

MIT
