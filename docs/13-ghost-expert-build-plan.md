# 13 — Ghost Expert Build Plan: the master technician who never retires

> Full engineering + demo plan for **Ghost Expert** (Track 1 — Intelligent Industry, + Google prize via Gemma).
> An expert films a procedure **once**. Ghost Expert turns it into a step-by-step procedure, then watches a trainee do the same job live through a camera and **coaches them out loud** — and stops them before a safety-critical mistake.
> Written to survive the [hostile review](10-hostile-review-and-upgrades.md): the AI is never the only judge, every claim has an eval number, and the GPU does visible work.

## 0. Definition of done

| Tier | Deliverable | Proof artifact |
|------|------------|----------------|
| **MUST** | **Authoring:** one expert video (with narration) → procedure JSON with 6–8 steps, keyframes, order rules — expert can edit and approve it | screen recording of authoring (time-lapse) |
| **MUST** | **Live coaching:** trainee does the task on camera; screen shows current step, completed steps, expert keyframe side-by-side | live demo + video |
| **MUST** | **The interrupt:** trainee skips a safety-critical step → voice + red banner stop them within ~1.5 s, with the expert's clip of the step they skipped | video segment, latency logged |
| **MUST** | **Eval:** ≥20 recorded trainee runs with injected errors → catch rate, false-alarm rate, p50/p95 interrupt latency | `eval/results.md` + slide |
| **MUST** | Everything runs on **one AMD Instinct GPU** (Gemma + Whisper + SigLIP + TTS loaded together) with a live benchmark panel | panel screenshot: device name, VRAM, latency, tokens/s |
| **SHOULD** | **"Show me how":** trainee asks by voice → answer + the expert's hands at exactly that moment replay | video segment |
| **SHOULD** | **Session report:** time per step vs expert, mistakes caught, hints given → training record (PDF/JSON) | screenshot |
| **SHOULD** | Bilingual coaching (trainee speaks Italian, expert recorded in English or vice versa) | video segment |
| **NICE** | N concurrent coaching streams on one GPU → cost per trainee-hour | benchmark table |
| **CUT LIST** | AR glasses, multiple cameras, CMMS/LMS integration, hand-pose skeletons, user accounts | say "roadmap" |

**One-sentence demo:** *"Your best technician retires next year and everything she knows leaves with her. She filmed one job, once. Now she watches every new hire do it — and stops them before they get hurt."*

---

## 1. First steps (before writing any code)

- [ ] **GPU + serving smoke test** — this is the #1 risk, do it first:
  - Get an AMD Developer Cloud instance (MI300X class). `python -c "import torch; print(torch.cuda.get_device_name(0))"` → screenshot for slides.
  - Run vLLM's ROCm Docker image and serve **Gemma 3 12B-it** (vision). Send one request with 4 images. Measure latency. Then try **27B-it**. Write both numbers down.
  - Confirm the tokenfactory API is *not* your hot path — live coaching needs your own endpoint for latency. (Tokenfactory is fine for offline authoring if your own endpoint is not available.)
- [ ] **Pick and buy the props** (§2). Build the "machine" before the software — the software is tuned to it.
- [ ] **Record the expert video on day one**, in the demo setup, with the demo camera. Narrate every step out loud. Record it three times; keep the best.
- [ ] Repo public from the start, MIT license, `.env.example`, no keys.

---

## 2. The demo task — choose it like a stage prop

The task decides whether the vision model succeeds. Rules: **table-top, top-down camera, big colored parts, order matters, one step that kills people if skipped.**

### Primary: bench-top Lockout/Tagout + filter change ("the machine")

Lockout/Tagout (LOTO) is the real industrial procedure for isolating energy before servicing a machine — consistently among OSHA's most-cited safety standards, and mandatory training in every plant. Skipping "verify zero energy" is the classic fatal error.

**Props (~€40, hardware store):** a lamp or small fan plugged into a switched power strip (= the machine and its isolator) · a **bright red** plug lockout box or padlock · a **yellow** "DO NOT OPERATE" tag · a plastic project box with a cover held by 4 big screws (= the guard) · a colored filter/sponge inside · a screwdriver. Matte dark tablecloth. Phone or USB webcam on a desk arm, top-down.

| # | Step | Visual check (what the model looks for) | Safety-critical | Must come after |
|---|------|-----------------------------------------|-----------------|-----------------|
| 1 | Switch the machine off at the strip | strip switch light off, lamp off | — | — |
| 2 | Unplug and lock the plug in the red box | plug inside red lockout box, closed | ✅ | 1 |
| 3 | Hang the yellow tag | yellow tag attached to box | ✅ | 2 |
| 4 | **Verify zero energy: press the machine's own switch** | hand presses lamp switch, lamp stays off | ✅ | 3 |
| 5 | Remove the 4 cover screws, lift the cover | cover off, screws on tray | ✅ | 4 |
| 6 | Swap the filter (old out, new in) | new filter color visible inside | — | 5 |
| 7 | Cover on, 4 screws back | cover on, tray empty | — | 6 |
| 8 | Remove tag + lock, plug in, switch on | lamp on | — | 7 |

**The planted mistake:** a judge removes the cover (step 5) without doing step 4. That is the interrupt.

### Backup task: LEGO build of a small "gearbox" (8 steps, colored bricks)

Zero hardware risk, everybody understands it. Use it as a fallback, or as the "second procedure" that proves authoring is general: *"We taught it this one in 90 seconds, here."*

---

## 3. Architecture

```
 BROWSER (demo laptop)                       AMD INSTINCT GPU SERVER (one box, docker compose)
 ┌──────────────────────────┐   WebSocket   ┌───────────────────────────────────────────────────┐
 │ getUserMedia camera+mic  │──JPEG 4 fps──►│ FastAPI app                                       │
 │ Coach UI / Author UI     │──audio (PTT)─►│  ├─ fast tier: SigLIP embeddings → step tracker   │
 │ plays TTS audio + clips  │◄─events/audio─│  ├─ rule engine (deterministic state machine)     │
 └──────────────────────────┘               │  ├─ slow tier: Gemma 3 vision verify (via vLLM)   │
                                            │  ├─ Whisper (ASR)    ├─ Kokoro (TTS)              │
                                            │  └─ procedures/ (JSON + keyframes + expert mp4)   │
                                            │ vLLM server: Gemma 3 12B/27B-it, OpenAI API       │
                                            └───────────────────────────────────────────────────┘
```

**The key design decision:** the LLM never decides alone. Three layers:

1. **Fast tier (every frame, ~10 ms):** SigLIP image embedding vs each step's reference embeddings from the expert video → smoothed "which step does this look like" scores. Cheap, always on, can be wrong.
2. **Slow tier (on trigger, ~0.5–1 s):** Gemma 3 gets the last 4 frames + the expert keyframe + that step's visual check → strict JSON verdict. Triggered when the fast tier sees a step change, plus a heartbeat every ~2 s.
3. **Rule engine (deterministic Python):** owns the state. A step is *done* only when Gemma confirms it. If the trainee is starting step *k* while a `must_come_after` step is not confirmed **and** *k* is safety-critical → **INTERRUPT**. Non-critical → gentle hint. This is the "not just a prompt" answer for the judges.

### Repo layout (keep it this small)

```
ghost-expert/
├─ docker-compose.yml        # vllm (rocm image) + app
├─ .env.example              # VLLM_URL, MODEL, thresholds
├─ app/
│  ├─ main.py                # FastAPI: routes + WebSocket
│  ├─ models.py              # load SigLIP, Whisper, Kokoro once, on the GPU
│  ├─ author.py              # expert video → procedure.json
│  ├─ coach.py               # fast tier + rule engine + slow tier calls
│  ├─ prompts.py             # the 3 prompts + JSON schemas
│  └─ report.py              # session → training record
├─ web/
│  ├─ index.html             # author / coach / report views
│  └─ app.js
├─ procedures/loto-filter/   # procedure.json, keyframes/*.jpg, expert.mp4, refs.npy
├─ eval/
│  ├─ runs/                  # recorded trainee runs + labels.json
│  └─ run_eval.py            # replays runs through coach.py → results.md
└─ README.md
```

---

## 4. Models and algorithms

### 4.1 Model lineup (all on one GPU)

| Job | Model | Why | Fits? |
|-----|-------|-----|-------|
| See + reason (verify steps, write procedure, answer questions) | **Gemma 3 12B-it** (or 27B-it if latency allows) via **vLLM on ROCm** | vision + multilingual + structured JSON; unlocks the Google prize | 27B in bf16 ≈ 55 GB |
| Fast frame embeddings | **SigLIP so400m** (PyTorch) | same family as Gemma 3's vision encoder; ~10 ms/frame | ~2 GB |
| Speech to text (expert narration, trainee questions) | **Whisper large-v3-turbo** (HF transformers on ROCm) | timestamps for authoring; robust Italian/English | ~2 GB |
| Text to speech (coach voice) | **Kokoro-82M** | tiny, fast, natural | <1 GB |

Everything fits on one MI300X-class GPU with room to spare — that is a slide: *"four models, one GPU, no swapping."* Pick 12B vs 27B by the eval (§5.4), not by vibes.

### 4.2 Authoring pipeline (`author.py`) — expert video → procedure

1. `ffmpeg`: frames at 2 fps (512 px) + audio track.
2. Whisper → transcript with word timestamps.
3. SigLIP embedding per frame → **change points** (cosine distance between rolling windows spikes) → candidate step boundaries. Merge with transcript cues ("next", "now", "then", pauses > 1.5 s).
4. Gemma 3 gets: transcript + a contact sheet of one keyframe per candidate segment → returns the procedure with **structured outputs (JSON schema)** so it can't return junk:

```json
{
  "id": "loto-filter",
  "title": "Lockout/tagout + filter change",
  "steps": [
    {
      "id": 4,
      "title": "Verify zero energy",
      "instruction": "Press the machine's own switch. It must stay off.",
      "visual_check": "a hand presses the lamp's switch and the lamp stays off",
      "safety_critical": true,
      "must_come_after": [3],
      "common_mistake": "Opening the cover without testing the switch",
      "expert_clip": [41.5, 47.0],
      "keyframe": "keyframes/step4.jpg"
    }
  ]
}
```

5. **Expert review screen:** the expert edits titles, flips `safety_critical`, fixes boundaries by dragging. Approve → `refs.npy` (mean SigLIP embedding of each step's frames) is saved. This human gate is part of the product: *the expert owns the procedure, the AI drafts it.*

**Bonus output for free:** the approved procedure renders as a printable work instruction (steps + keyframes). Writing those by hand takes hours — mention it, it's real business value.

### 4.3 Live coaching loop (`coach.py`)

```python
# per frame (fast tier)
emb = siglip(frame)
scores = ema(cosine(emb, refs))          # one score per step, smoothed
guess = argmax(scores)

# rule engine — owns the truth
if guess != state.current and scores[guess] > ENTER_T:     # looks like a new step
    verdict = gemma_verify(last_frames(4), step=guess)     # slow tier
    blockers = [s for s in steps[guess].must_come_after if s not in state.done]
    if steps[guess].safety_critical and blockers and verdict.started:
        interrupt(blockers[0])     # voice + red banner + expert clip of the skipped step
    elif verdict.done and verdict.confidence > DONE_T:
        state.done.add(guess)
every ~2 s: gemma_verify(last_frames(4), step=state.current)   # heartbeat confirms completions
```

- **Two-confirmation rule:** interrupt only when the fast tier *and* Gemma agree the trainee is in the forbidden step. False alarms are worse than a half-second delay.
- **Ask, don't accuse, when unsure:** if confidence is in the grey zone → *"Can you show me the tag?"* instead of an alarm. That is the visible uncertainty.
- **Calibration knobs** in `.env`: `ENTER_T`, `DONE_T`, `INTERRUPT_CONFIRMATIONS`, frame rate. Tune them on the eval set, at the venue.

### 4.4 The verify prompt (`prompts.py`) — short, strict, cached

System prompt + procedure + expert keyframes are **identical across calls** → vLLM's automatic prefix caching makes every verify call only pay for the 4 new frames. Order the prompt so the constant part comes first.

```
You are checking one step of an industrial procedure from a top-down camera.
Step: {title}. It is done when: {visual_check}.
Image 1 is the expert doing it. Images 2–5 are the trainee, oldest to newest.
Return JSON: {"started": bool, "done": bool, "confidence": 0-1,
              "observed": "<one short sentence of what you see>"}
If you cannot see the relevant parts, set confidence below 0.4.
```

Output is a handful of tokens → latency is dominated by image prefill (Gemma 3 uses 256 tokens per image), which is exactly where the big GPU helps.

### 4.5 "Show me how" (voice Q&A)

Push-to-talk → Whisper → Gemma with {procedure, current step, transcript slice of the expert} → short answer → Kokoro voice **+ the app jumps the expert video to `expert_clip` of the relevant step**. The moment: the trainee asks *"where does the filter go?"* and the expert's own hands answer.

### 4.6 UI spec (`web/`) — one page, three views

- **Coach view (the stage):** left = live camera; right = expert keyframe of the current step; top = step rail (✓ done · ● current · ○ to do; safety steps marked ⚠); bottom = coach caption (what it just said) + confidence chip. Interrupt = whole frame goes red, expert clip of the skipped step plays.
- **Author view:** expert video with a timeline of detected steps; editable step cards; Approve.
- **Report view:** time per step vs expert, mistakes caught, hints given, "competent / needs another run" — the training manager's screen.
- **Benchmark panel (always visible, small):** GPU name, VRAM used, frames/s, verify latency p50/p95, tokens/s.

---

## 5. Demo production

### 5.1 Recordings you need

- `expert.mp4` ×3 takes (keep best), in the demo setup.
- **Eval runs:** 20–30 trainee runs, ~60–90 s each. ~Half clean, half with one injected error each: skip step 4, skip step 3, wrong order 6↔5, forgot a screw, didn't remove the lock. Label each in `labels.json` (`{run, error_type, error_frame_time}`). Use different people, sleeves, lighting if possible.

### 5.2 The demo script (~3 minutes)

| Time | What happens | What you say |
|------|--------------|--------------|
| 0:00 | Black screen, then expert video | *"This is our expert servicing a machine. Thirty years of experience. When she retires, it's gone."* |
| 0:15 | Author view, time-lapse: video → 8 steps with keyframes | *"She filmed it once. In 90 seconds, on an AMD GPU, it became this — and she approved it."* |
| 0:35 | Hand a judge the screwdriver. Coach view live | *"Your first day. Just do the job."* |
| 0:50 | Coach guides steps 1–3 by voice, rail fills with ✓ | (stay quiet — let the machine talk) |
| 1:10 | Judge reaches for the cover screws without testing the switch → **red screen, voice: "Stop. You haven't checked the machine is dead. Press its switch first — here's how she does it."** Expert clip plays | *"That's the mistake that kills technicians every year."* |
| 1:40 | Judge asks *"where does the new filter go?"* → expert clip + answer | *"Her hands, answering your question."* |
| 2:05 | Report view | *"The training manager gets this: time per step, mistakes caught."* |
| 2:20 | Eval slide | *"20 recorded runs: caught X of Y mistakes, Z false alarms, median 0.9 seconds."* (your real numbers) |
| 2:35 | Benchmark panel + cost slide | *"Four models on one AMD GPU. N trainees at once. €X per trainee-hour."* |
| 2:50 | Close | *"Every plant has someone who's about to retire. Film them."* |

**If the live interrupt misfires:** say *"that's why we measure it"*, cut to the recorded run, keep going. Never debug on stage.

### 5.3 What gets recorded, when

- The first time the interrupt works end-to-end → **screen-record it immediately**. That clip is your insurance.
- The final video = the §5.2 script, with the live take if clean, recorded take otherwise.

### 5.4 Benchmarks to capture (`eval/run_eval.py` + a benchmark script)

| Number | How |
|--------|-----|
| Catch rate per error type | replay labeled runs through `coach.py` at real speed |
| False alarms per clean run | same |
| Interrupt latency p50/p95 | from error frame to interrupt event |
| Verify latency, 12B vs 27B | 200 calls each, with prefix caching on/off |
| Concurrent streams per GPU | N synthetic replays at once until p95 latency > 1.5 s |
| Authoring time | wall clock, video in → procedure out |

---

## 6. Build order (dependency-ordered, no clock)

Advance only when the gate passes. Every phase leaves something demo-able behind.

### Phase 0 — Serving + props + expert video
§1 checklist. **Gate:** Gemma 3 answers a 4-image request on your AMD box; you know the 12B and 27B latency; the props exist; `expert.mp4` is recorded.

### Phase 1 — The verify call (the risky core)
`prompts.py` + a CLI: take 4 frames from a recording + a step → JSON verdict. Run it on frames you labeled by hand.
**GATE 1: the model correctly says done/not-done on ≥90% of hand-labeled step clips, especially step 4 (switch press) and step 2 (plug in box).** If it fails: make the props bigger and more colorful, raise the resolution, crop to the work area, add a second keyframe. **Do not build UI before this passes.**

### Phase 2 — Fast tier + rule engine, offline
`models.py` (SigLIP) + `coach.py`, run on recorded runs (no camera yet).
**GATE 2: `run_eval.py` catches the skip-step-4 error in recorded runs with zero false alarms on 5 clean runs.**

### Phase 3 — Authoring
`author.py` → procedure JSON → expert edit view. It's fine if the first draft needs edits — the edit screen is the feature.
**Gate:** the LOTO video becomes a correct 8-step procedure after ≤3 edits.

### Phase 4 — Live app
WebSocket camera stream, coach view, TTS, interrupt with expert clip. Run the app on the AMD box, open the port or tunnel, so the submission URL is live.
**GATE 3: a teammate who hasn't seen the code does the task 3 times; the interrupt fires when they skip step 4, and never when they don't.**

### Phase 5 — "Show me how", report, bilingual
Small pieces on top of what exists. Drop any of them freely.

### Phase 6 — Eval + benchmarks + film
Record the 20–30 runs, run the eval, capture benchmarks, film the §5.2 script.

### Phase 7 — README, slides, submission
README with the eval table and a `docker compose up` that works. Cover image = the red interrupt frame. **After submitting, only polish the video and slides.**

### Cut list — drop in this order
1. Concurrent streams benchmark (use one measured number). 2. Bilingual. 3. Report view (show it in a slide). 4. Voice Q&A (keep the clip replay on a button). 5. Authoring UI (edit the JSON by hand, show the pipeline output in the video). 6. Live stage demo — the video carries the entry.

---

## 7. Submission and armor

### 7.1 Track 1 checklist mapping

| Track 1 asks | Ghost Expert shows |
|--------------|-------------------|
| Realistic industrial data | a real LOTO + service procedure, filmed |
| Alert / explanation / action | the interrupt + the expert clip + the step to do instead |
| Who uses it | trainee (coach view), expert (author view), training manager (report) |
| What improves | mistakes caught before harm, expert hours per trainee, time to competency |

### 7.2 Armor slide — expected kill shots, answered

| Kill shot | Answer |
|-----------|--------|
| *"It's just a vision model with a prompt."* | "The model never decides alone — a deterministic state machine owns safety, two signals must agree, and here's the eval." |
| *"What if it misses a mistake?"* | "It's a trainer, not a safety system — the lock is still the safety system. We show the miss rate instead of hiding it." |
| *"A camera filming workers? In Italy?"* | "Correct concern — worker monitoring is restricted (Statuto dei Lavoratori, art. 4). This is training-only, started by the trainee, frames processed in memory and not stored by default. A coach, not surveillance." |
| *"Works on your toy box, not a real plant."* | "The authoring is general — we taught it a second procedure in 90 seconds (LEGO). A pilot means filming one real procedure at one plant." |
| *"Why does this need a big GPU?"* | "Four models live, sub-second verify on 4 frames, N trainees per GPU — here's the benchmark and the cost per trainee-hour." |

### 7.3 Who pays

Plant training managers and EHS (health & safety) managers — training is mandatory (in Italy, D.Lgs. 81/2008) and today it means a senior technician standing next to every new hire. Price per procedure authored + per trainee seat per month. Metric to pitch: **expert hours saved per trainee, and mistakes caught before they happen.** Any market-size or injury statistic on the slides needs a cited source — don't invent one.

---

## 8. What could break (risk register)

| # | Risk | You'll notice it when… | Mitigation | Fallback |
|---|------|------------------------|------------|----------|
| 1 | **vLLM + Gemma 3 vision won't run on the ROCm image** | Phase 0 smoke test fails | try the official ROCm vLLM image + a different vLLM version; serve with HF transformers as a slower backup | Qwen2.5-VL on vLLM (works, but loses the Google prize angle) |
| 2 | **Verify too slow (>1.5 s)** → interrupt arrives after the cover is off | latency p95 in Phase 2 | 12B instead of 27B, 3 frames not 4, 384 px crops of the work area, prefix caching, trigger earlier (when the hand approaches the screws) | interrupt on fast-tier + rule engine alone for the one critical transition |
| 3 | **False alarms** — coach nags a correct trainee | clean eval runs fire interrupts | two-confirmation rule, higher thresholds, "ask, don't accuse" grey zone | narrow interrupts to step 4 only, hints elsewhere |
| 4 | **Model can't see small things** (tag on, plug in box, lamp on/off) | Gate 1 fails on those steps | big saturated props, top-down fixed camera, dark cloth, crop to the work area, include the expert keyframe | rework the step so it's visible (e.g., a big lamp the model can't miss) |
| 5 | **Venue looks different from the expert video** (light, table, sleeves) | fast-tier scores flat or wrong | record the expert video at the venue; refs re-record in 3 minutes; Gemma is the authority, SigLIP only triggers | heartbeat-only mode (Gemma every 1.5 s, no fast tier) |
| 6 | **Network jitter** laptop ↔ AMD cloud | frames arrive in bursts, latency spikes | 4 fps small JPEGs, drop stale frames server-side, phone hotspot as backup network | play the recorded perfect run |
| 7 | **Authoring segments the video wrong** | wrong step count | narrate clearly ("step four…") — transcript cues dominate; expert edit screen | hand-written procedure.json (still show the pipeline in the video) |
| 8 | **Audio chaos on stage** (coach voice + room noise) | Whisper mishears | push-to-talk, a cheap lapel mic for the judge, captions on screen | typed question box |
| 9 | **Judge does something nobody predicted** | step tracker gets lost | "I lost you — which step are you on?" fallback line; manual step-advance key for the presenter | presenter hotkey to reset the session |
| 10 | **GPU instance unavailable on demo day** | instance won't start | keep the instance alive, docker image pushed, a second region/account noted | recorded video + eval numbers carry the entry |

---

## 9. Confirm with the organizers

- Can you run your **own vLLM server** on the AMD Developer Cloud instance for the whole event, and expose a public port (for the live app URL)?
- Is **Gemma 3 vision** (12B/27B) available or downloadable on the instance? (Gemma needs its license accepted on Hugging Face — do it early.)
- Will there be **stable internet** for a live camera stream at the venue, or should you plan for a hotspot?
- Is a **live physical demo** allowed in the judging slot, or video only?

---

## 10. The number on the slide

Pick the one number the judges remember, and make it real from your eval:

> **"Caught X of Y safety mistakes in under a second — on one AMD GPU."**
