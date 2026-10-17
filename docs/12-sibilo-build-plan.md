# 12 — Sibilo Build Plan: an acoustic camera on AMD, in one weekend

> Full engineering + demo plan for **Sibilo** (idea in [11-wow-ideas.md](11-wow-ideas.md)): a camera that takes pictures of sound — locating compressed-air leaks and machine faults in a factory, live, on an AMD GPU.
> Read the [hostile review](10-hostile-review-and-upgrades.md) first; this plan is written to survive that panel.

## 0. Definition of done

By submission time, all of these exist and are true:

| Tier | Deliverable | Proof artifact |
|------|------------|----------------|
| **MUST** | Blinded localization: judges pick a position from 3–4 taped spots, a hiss plays, the screen map peaks on that spot | video segment + archived session |
| **MUST** | Classification: hiss → "compressed-air leak" card; whine → "bearing wear" card; nothing mislabeled | confusion matrix + live demo |
| **MUST** | €-card with a "show the math" panel (assumptions visible, ±error stated) | screenshot |
| **MUST** | Everything runs through one GPU pipeline (real-time scan + CNN) on ROCm | benchmark panel: scans/sec, frames/sec |
| **SHOULD** | Two simultaneous sounds → two peaks (multi-source scan) | video segment |
| **SHOULD** | Leak workflow: candidate → confirmed → fixed → € verified (session log) | session state screen |
| **NICE** | Always-on puck concept slide with per-site pricing | slide |
| **CUT LIST** | 3D room, mobile app, live ultrasonic, real CMMS integration, multi-user | say "roadmap" |

> **Solo build:** the SHOULD tier demotes to NICE — the MUST tier is the whole plan. Everything is ordered by dependency in §6, not by clock.

**One-sentence demo:** *"A factory loses 10–30% of its compressed air through leaks, and every audit needs a €10,000 camera. We built the camera for ~€100 of mics and a GPU — pick a corner, we'll find the hiss."*

---

## 1. First 60 minutes (do this before writing any code)

- [ ] **Confirm the exact submission deadline** (open question #1 in [07-open-questions.md](07-open-questions.md)) — then work in the dependency order of §6, not against the clock.
- [ ] **Verify the GPU:** get on the AMD Developer Cloud instance; `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` (ROCm uses the `cuda` API in PyTorch — it's a naming convention, not CUDA). Run one matmul; screenshot the device name for the slides.
- [ ] **Hardware recon — ask the room.** In priority order:
  1. Any **multichannel USB audio device**: ReSpeaker 4/6-mic USB array, any UAC-compliant conference puck that exposes >1 channel, a Zoom/Tascam field recorder in USB-interface mode (4+ inputs).
  2. Any **USB interface + 2 cheap mics** from a music/AV person.
  3. Laptop built-in mic (assume **mono** — verify: `ffmpeg -f avfoundation -list_devices true -i ""` on macOS or `arecord -l` on Linux; record and inspect channels with `sox --i`).
- [ ] **Test the demo room acoustics:** clap test, listen for HVAC rumble, pick the taped-position corners (near walls, not the center — echoes are worse mid-room).
- [ ] **Hunt for a real compressed-air source on the venue** (loading dock, maintenance room, a lab). Recording a real leak is worth ten minutes of walking. **Do not touch equipment without permission.**
- [ ] Create the repo, push an empty README — **public from hour one** (submission rule), MIT license file.

---

## 2. Hardware decision tree

The code is identical in every plan: everything downstream consumes an array tensor `X[mics, samples]`. Only the source changes.

| Plan | What you have | Demo mode | Risk |
|------|---------------|-----------|------|
| **A — Real array** | ReSpeaker-class mic array (4–8 ch, USB) | Fully live blinded test | Low; sync quirks |
| **B — Two-device array** | Laptop + phone as 2 mics | Live, coarse: source among 3 taped zones left/right/center | Sync via clap at record start; drift over <10 s is tolerable |
| **C — Virtual array** *(default fallback)* | Mono recordings only | Speaker plays at taped spot → helper selects spot 1–4 → **replay pre-generated array capture through the live pipeline** | Zero live risk; must label as virtual array |
| **D — Sibilo Solo** | One mic, no array at all | "Hot/cold hunt": walk with the mic, app says *getting warmer*; classifier still names the sound | Least wow; last resort |

**Plan C is not a fake demo — it is a real pipeline on a simulated sensor.** The array signals are produced from a real recording by convolving it with per-mic propagation delays + light reverb, then the *same* GPU beamformer runs, live, on the result. Say it plainly on the slide: *"The prototype hardware is a €60 4-mic puck that ships in a week; until then we simulate the array from real recordings. The DSP and AI are the product."* Judges forgive honest simulation; they punish discovery of hidden simulation.

**Plan A/B rig, if available:** mic spacing 20–40 cm (aperture sets angular resolution), mics taped to a rigid bar (a book, a plank), bar marked on the floor so its exact position is known (geometry must match reality — measure it).

---

## 3. Architecture

```
 capture (array / wav / virtual)
        │  X[mics, samples] @ 16 kHz
        ▼
 framing (2048 win, 1024 hop, Hann)
        │
        ▼
 rfft ─► PHAT-normalize ──┐
        │                 ▼
        │        SRP-PHAT scan over room grid   ◄── precomputed delays
        │        (GPU, batched, chunked)             geometry.py
        │                 │
        │                 ▼
        │        temporal EMA + peak extraction
        │                 │  (x, y, confidence, radius)
        │                 ▼
        │        beamform-at-peak → mono signal
        │                 │
        │                 ▼
        │        log-mel → CNN classifier (ROCm)      models/classifier.pt
        │                 │
        ▼                 ▼
 money.py ◄──── leak intensity → size → kWh → € → payback
        │
        ▼
 FastAPI + websocket ─► web UI: map, sweep, blob, card, session log, benchmark
```

### Repo layout

```
sibilo/
  README.md                  # what/why/how-to-run/benchmarks/limits (the judged artifact)
  LICENSE                    # MIT
  requirements.txt           # torch, torchaudio, numpy, scipy, soundfile, fastapi, uvicorn
  sibilo/
    geometry.py              # array + room grid + precomputed delays
    capture.py               # ArraySource | WavSource | VirtualArraySource
    beamform.py              # SRP-PHAT (GPU), batched + chunked
    detect.py                # EMA, peak pick, confidence, radius
    classify.py              # log-mel + CNN inference
    money.py                 # leak table + cost model + sensitivity
    pipeline.py              # orchestration, session state, events
    api.py                   # FastAPI endpoints + /ws/scan
  web/
    index.html  app.js  style.css   # map, sweep, blob, cards
  scripts/
    record_sources.py        # build the demo sound library
    make_dataset.py          # MIMII/DCASE + own recordings → mel dataset
    train.py                 # trains on ROCm; saves models/classifier.pt
    validate_dsp.py          # synthetic source at known position → error table
    benchmark.py             # GPU vs CPU scan throughput (slides evidence)
    replay.py                # deterministic video takes through the real pipeline
  data/recordings/           # the sound library (own recordings)
  data/sessions/             # archived demo runs (evidence)
  docs/demo-script.md  docs/slides.md  docs/findings.md
```

---

## 4. Signal processing — the actual algorithms

### 4.1 Geometry (`geometry.py`)

- Mic positions `r_m` (meters, in room coordinates), array origin marked on the floor.
- Room grid: candidate source points `p` on a plane at fixed height (1.2 m), e.g., **64×64 points** over the demo room (≈10–15 cm resolution), extensible to 128×128 for the "high-res" benchmark.
- Precompute propagation delays `tau[p, m] = |p - r_m| / c`, `c = 343 m/s`.

### 4.2 SRP-PHAT (`beamform.py`) — the core

Per frame (2048 samples @ 16 kHz = 128 ms), per mic: `X_m(f) = rfft(x_m)`.
PHAT-normalize to the reference mic: `X̂_m(f) = X_m(f)/|X_m(f)|` (epsilon 1e-9), band-limited to **300–7000 Hz** (hiss lives here; kills HVAC rumble and aliasing junk).

Steered response power per candidate point:

```
P(p) = Σ_f | Σ_m X̂_m(f) · exp(+j·2π·f·tau[p,m]) |²
```

Peak of `P` = estimated source position. SRP-PHAT is the standard robust choice in reverberant rooms — cite it, and say so when a judge asks about echoes.

Implementation notes (make the GPU *matter*):
- Tensors on GPU: `X̂` shaped `[B, M, F]` (batch of frames); phases `exp(...)` built per frame from `tau` — compute in **chunks over grid points** to bound memory (e.g., 16k points/chunk, fp16 phases).
- One forward pass = batch 32 frames × 64×64 grid × 8 mics × ~430 bins ≈ 4.5 G multiply-accumulates — trivial for an Instinct, painful in Python/CPU. Show both numbers (that's the benchmark).
- **2-stage scan** (ship if time): coarse 64×64 everywhere → top-8 regions × 32×32 refinement. Same math, finer blob, better story.
- Temporal smoothing: `P_ema = α·P + (1-α)·P_ema`, α ≈ 0.3 → stable blob at 4–8 UI updates/sec.

### 4.3 Detection (`detect.py`)

- Peak = argmax of smoothed `P`; confidence = `(Pmax − μ)/σ` of the map; radius = smallest disk holding 80% of above-threshold mass.
- Gate: confidence threshold tuned in rehearsal (record the value; that's your "how the threshold was tuned" answer — keep it honest: "8 positions, 40 runs, threshold that gives 100% hit with no false peaks").
- Beamform-at-peak: align all mics' **raw** spectra to the peak and sum → clean mono `y(t)` for the classifier (SNR boost, and it ties the two halves of the pipeline together in one sentence for judges).

### 4.4 Classifier (`classify.py`, `train.py`) — the AI half

**Classes (7):** `leak_hiss`, `bearing_whine`, `electrical_hum`, `machine_normal`, `speech`, `music`, `other_noise`.

**Data:**
- **MIMII / DCASE (public, real factory machine audio: fans, pumps, valves, slide rails)** → `machine_normal` + anomalous machinery sounds. Download a subset only.
- **Own recordings (the most important 30 minutes of the build):** air duster hiss, bike-valve hiss, spray bottle, squeaky hinge, hand blender/drill whine, charger hum, speech, room tone — **including the exact sounds and speaker you'll use in the demo**. The demo sounds must be in the training set.
- Augment: random gain, noise mixes from MIMII backgrounds, light synthetic reverb (a few conv filters). Keep it modest.

**Features/model:** 16 kHz, n_fft 1024, hop 256, 64 mel bands, ~1.5 s context (~96 frames). CNN: conv 3×3 (32→64→128) + BN + ReLU + maxpool, global average pool, dropout, linear(7) — <500k params. Train on ROCm, AdamW, minutes not hours. Hold out 20% + a **"demo sounds" holdout** to quote the number that matters.

**Fallback (if training misbehaves):** frozen audio embeddings + linear probe / kNN. Also acceptable: 3 classes only (leak / machine / other).

### 4.5 Money layer (`money.py`) — the card judges remember

**Flow estimate from table** (empirical, at 7 bar(g), free-air liters/sec — put the source in the README):

| Hole | ≈ l/s | ≈ m³/h |
|------|-------|--------|
| 1 mm | 1.2 | 4.3 |
| 2 mm | 4.5 | 16 |
| 3 mm | 10 | 36 |
| 6 mm | 40 | 144 |

**Energy & €:** compressor specific power ≈ **0.10 kWh per m³ of free air** (7 bar; state the assumption); run hours *H*; industrial tariff *p*:

```
kWh/yr = m³/h × 0.10 × H
€/yr   = kWh/yr × p

Example: 2 mm leak, 3 shifts (7,500 h), €0.25/kWh
       = 16 × 0.10 × 7,500 × 0.25 ≈ €3,000/yr
Fix:    €90 (fitting + 1 h labor)  →  payback ≈ 11 days
```

**Mapping sound → size:** calibrate against reference recordings: play sources at each taped position, record band energy at 1–2 m, fit initial estimates (start with the table above; store a JSON calibration). State **±50% size accuracy** and the confirmation step (soap test / ultrasonic check) *in the card itself* — "candidate leak" language, never "certified measurement."

**Sensitivity panel (the "show the math" screen):** sliders for run hours and €/kWh updating €/yr live. Hostile judges get to break it themselves — the attack dies in their hands.

### 4.6 UI spec (`web/`)

Single page, dark, data-viz aesthetic (it's a "camera" — look like one):

- **Map panel:** top-down SVG of the demo room with the tape marks A–D shown and labeled, mic array icon, **sweep animation** (rotating/radial scan line), heatmap blob (soft radial gradients), peak pin, confidence ring. On-screen map must visibly mirror the room the judges are sitting in — same corners, same geometry.
- **Status strip:** `scanning… · 64×64 @ 18 Hz · AMD Instinct · ROCm` + live counters (scans/sec, frames/sec). Screenshot-ready at all times.
- **Event card:** class badge, confidence bar, position ("near corner C"), €/yr, payback, **Show the math** expander, **Draft ticket** button.
- **Session log:** found / confirmed / fixed / € verified — the product's loop as a live list.
- **Benchmark button:** runs the fixed workload on GPU; optional CPU comparison (use a recorded CPU number if live compare is flaky — never gamble the demo on a CPU benchmark running *slow enough* to be dramatic).
- **Replay mode:** `?replay=session_X` drives the same UI from `data/sessions/` for deterministic video takes.

**API (FastAPI):** `WS /ws/scan` (map + counters, ~6 fps), `POST /detect` (run N sec → event), `POST /ticket` (mock work order JSON + id), `GET /session`, `GET /benchmark`. No keys anywhere; `env.example` empty-by-default (submission rule).

### 4.7 Benchmarks to capture (`scripts/benchmark.py`) — for the slide, not for the vanity

| Number | How | Why it matters |
|--------|-----|----------------|
| Localization accuracy | `validate_dsp.py`: synthetic sources at 8 known positions × 5 runs → mean error (cm) + hit rate | "The DSP works" |
| Scan throughput | fixed workload: 64×64 grid, 32-frame batch, 8 mics | GPU vs CPU — the AMD answer |
| End-to-end latency | sound onset → blob + class on screen | "it's live" |
| Training time | `train.py` wall-clock on ROCm | "the GPU trained the model" |
| Demo dry-run success | 10 blinded runs, recorded | "it works when you try it" |

---

## 5. Demo production

### 5.1 Sound library (`scripts/record_sources.py`)

Record everything at 48 kHz, keep raw; downsample to 16 kHz for the pipeline. Sources:

1. **Leak hiss** — air duster (best), bike tire valve, spray bottle. *If a real compressed air leak is found on venue: gold — record 3 distances.*
2. **Bearing whine** — hand blender, drill at low speed, a squeaky chair dragged; add from public recordings if needed.
3. **Hum** — phone charger, fluorescent ballast.
4. Room tone, speech, music, footsteps — the "everything else" that makes the classifier's no-false-alarm claim real.

Speaker check: play each through the **actual demo Bluetooth speaker**, re-record, verify the spectrum survives (small speakers eat high frequencies — if the hiss dies, boost or pick another speaker; test *before* the demo, not during).

### 5.2 The demo script (verbatim, ~3 minutes live)

> **Setup:** 4 tape marks A–D on the floor at corners; the same marks drawn on the on-screen map; speaker in your bag; laptop driving the projector. **Solo staging:** the "pick a corner" moment is a **coin flip on camera** — heads = A, tails = D, or a 4-way pick from a phone RNG shown on screen. No second person needed, and it reads as a randomized test.

1. **Hook (15 s).** "Factories lose 10–30% of their compressed air through leaks. Finding them means a €10,000 acoustic camera or a rented auditor. Today, we found one with a €60 puck and this AMD GPU. The corner gets chosen without telling the software — live judges pick, or if it's just us and the camera, a coin decides: A, B, C, or D."
2. **Blinded test (45 s).** Place the speaker on the chosen mark; hiss plays. Screen: sweep starts, counters tick, blob converges. Card: **compressed-air leak · near corner C · €3,000/yr · fix €90 · payback 11 days.** "Check with your own ears — that's where the sound is."
3. **Judgment, not just location (30 s).** Second sound (whine) from another corner: different class — **bearing wear**, not a leak — ticket drafted. "Same camera, different diagnosis."
4. **The loop (20 s).** Mark the leak *confirmed*; session log updates: found → confirmed; € counter; "this is leak debt — the product is driving it to zero."
5. **Benchmark close (20 s).** Benchmark panel: scans/sec, GPU vs CPU, training time. "Every one of those numbers ran on the AMD cloud GPU through ROCm."
6. **Business close (20 s).** "€99–299/month per site replaces the yearly audit; service companies get the tool that closes more fix-jobs. Thanks."

**Staging checklist (solo):** tape marks visible on screen *and* floor; the coin flip captured on camera (it's rigor, and it entertains); speaker volume set in rehearsal (mark it with tape on the volume wheel); speaker placement + play-start done by you in one fluid movement; the video uses the best take from `replay.py` (same pipeline, deterministic).

### 5.3 What gets recorded, when

- The **first time the blob converges correctly on real or virtual audio — record immediately** (phone video is fine). That's your insurance; get it the first day it works, not the last.
- Every full dry-run. Keep `data/sessions/` as evidence (timestamps, positions, results).

---

## 6. Build order — solo edition (dependency-ordered, no clock)

One builder. Advance only when the current phase's gate passes; every phase leaves a demo-able artifact behind. Effort shape, not schedule: **Phase 1 is roughly a third of the whole build, Phase 4 the second biggest** — everything else is small on purpose.

### Phase 0 — Recon and repo (keep it short)

§1 checklist → hardware decision written down (Plan A/B/C/D); GPU verified (device-name screenshot); repo up (README skeleton + MIT); first recording session done.
**Gate:** decision written, repo public, sounds on disk.

### Phase 1 — Sound library → geometry → SRP-PHAT → validation (the risky core)

`record_sources.py` (§5.1) · `geometry.py` · `beamform.py` · `validate_dsp.py`.
Deliverable: a CLI that takes recordings + mic geometry → heatmap PNG + peak position + error table.
Validate on **synthetic arrays built from your real recordings at known positions** — this tests the DSP independently of any hardware.
**GATE 1: ≥90% of validation runs within ~30 cm.** If it doesn't pass: simplify to 3–4 taped zones (corner-level accuracy is all the demo needs) and move on. **Do not build UI before this passes.**

### Phase 2 — Classifier (small; training on GPUs is cheap)

Start with **3 classes** (`leak_hiss`, `machine_whine_hum`, `other`); expand to 7 only if it's smooth. Log-mel + small CNN, trained on ROCm in minutes. If training fights back: frozen audio embeddings + linear probe — same story ("a model trained on ROCm"), less drama.
Rule, repeated because it's the one that saves the demo: **the exact demo sounds are in the training set.**
**GATE 2:** demo sounds classified correctly; confusion matrix saved to `docs/findings.md`.

### Phase 3 — Money layer (small, high value)

`money.py`: leak table, kWh, €/yr, payback, ±50% note, slider data for the sensitivity panel. Hand-check one worked example.
**Gate:** the €3,000 example computes correctly with a pen and paper.

### Phase 4 — The app (second biggest block)

FastAPI + **one** `index.html`: canvas heatmap, sweep animation, blob, counters, event card, "show the math" expander, benchmark panel. Wire `pipeline.py` end-to-end.
If you're not comfortable with HTML/JS: Streamlit + plotly heatmap — half the polish, half the time, still acceptable.
Deploy where the GPU is: run the app **on the AMD instance** and expose the port per the cloud docs (or a tunnel) so the submission's app URL is real and live.
**GATE 3:** play a sound → blob + class + €-card on screen, repeatably.

### Phase 5 — Film the demo (the primary artifact)

Record in `replay.py` mode for determinism; keep a live take only if it's rock solid. Solo script = §5.2 with the coin flip. Two takes, same script, pick the calmer one. If the UI misbehaves on camera, the matplotlib-rendered sweep+blob (precomputed frames → mp4) is a fully deterministic fallback.
**GATE 4:** watch your own video as a judge — if you're bored by 0:30, re-cut it. You are the entire test audience.

### Phase 6 — README, slides, submission

Benchmark table in the README (real numbers from `benchmark.py`), 9 slides including the armor slide, cover image = the heatmap blob (it's your logo now), submit. **After submitting: polish video/slides only. No code changes.**

### Solo cut list — drop in this order

1. Multi-source scanning (two peaks). 2. The 2-stage fine scan. 3. Live CPU-vs-GPU compare (use one recorded number). 4. Session workflow beyond a simple event list. 5. Ticket flow (one button, mock JSON). 6. Streamlit replacing the canvas. 7. The live stage demo — the video carries the entry.

### If you're ahead of plan (rare, but plan for it)

128×128-grid benchmark number · two simultaneous sources · the always-on puck slide — slides are cheap, code is not. **Never add a new pipeline component late.**

---

## 7. Submission artifacts

### 7.1 README (judges read this after the video)

What it is (one paragraph + architecture diagram) → how to run (`pip install -r requirements.txt; uvicorn sibilo.api:app; open localhost:8000`) → AMD/ROCm note + benchmark table → dataset provenance (MIMII/DCASE source + our recordings) → **honest limitations** (visible-band mics vs 40 kHz field units; array simulation in this prototype; ±50% size estimate; confirmation step) → roadmap (mic puck, ultrasonic MEMS, always-on units) → MIT.

### 7.2 Video (3 min, script = §5.2)

Edit rhythm: hook by 0:15, demo by 0:25, numbers by 1:30, business by 2:20, close by 2:50. Subtitles. Show the AMD name in the terminal/panel **twice**. Record in replay mode; cut to live-demo B-roll from the dry-runs.

### 7.3 Slides (8 + armor)

1. Title + one-liner. 2. Problem (10–30% waste; audit cost; the €10k instrument). 3. **Live demo** (screenshot + QR to the app). 4. How it works (pipeline diagram; one equation). 5. **AMD matters** (benchmark table: scans/sec GPU vs CPU, training time, device name). 6. Accuracy & honesty (hit error, confusion matrix, limits). 7. Business (buyer = compressed-air service cos + energy managers; €99–299/site/mo; payback math). 8. Roadmap (puck → ultrasonic → always-on). 9. **Armor slide** (below).

### 7.4 Armor slide — expected kill shots, answered

| Kill shot | Answer (say it first, on the slide) |
|-----------|-------------------------------------|
| "Just DSP, where's the AI?" | "The classifier — trained on ROCm — names the sound; the DSP finds it. Both run on the GPU, numbers on slide 5." |
| "Consumer mics can't hear leaks." | "Voice band in a quiet room yes; field units use 40 kHz MEMS to beat noise. Our pipeline is frequency-agnostic; the puck is €60." |
| "You simulated the array." | "Correct, labeled on slide 3 — the DSP and AI are real and run live on real recordings; the hardware ships in a week." |
| "One demo is not a product." | "The product is the loop: found → confirmed → fixed → € verified, per site, monthly — the last slide is the pricing." |
| "Echoes will blur it." | "SRP-PHAT is built for reverberant rooms; confidence ring shows uncertainty; small rooms and corner sources in rehearsal." |

---

## 8. Risk register

| Risk | Likelihood | Mitigation | Trigger to act |
|------|-----------|------------|----------------|
| No multichannel hardware | High | Plan C (virtual array) — pipeline identical, labeled | Phase 0 recon result |
| DSP doesn't localize at GATE 1 | Medium | Reduce to 3 taped zones (coarse angular); raise band limits; Plan C live | Phase 1 |
| Classifier confuses demo sounds | Medium | Demo sounds in training set; 3-class fallback | Phase 2 |
| Speaker kills the hiss spectrum | Medium | Re-record through the actual speaker; spectral check script | Phase 4 |
| Room noise at demo time | Medium | Gain calibration per session; headphones backup for judges in video | rehearsal |
| GPU instance hiccup | Low | Replay mode for video; benchmark screenshots archived | ongoing |
| Time overrun | High | Cut rules §6; video-first policy | GATE 3 |
| Judges inspect repo for honesty | Always | Limits in README; simulation labeled on slide; every number reproducible | submission |

---

## 9. Confirm on-site (before Phase 1)

1. Submission deadline exact time (open question #1).
2. Who has a multichannel mic/recorder (ask organizers + Discord + neighbors).
3. Any compressed-air source on the venue (maintenance/loading area).
4. Whether the demo room has a projector + audio output for the speaker test.

---

## 10. The number on the slide

Everything above exists to make this line true, verifiable, and retold:

> **"We found a €3,000/year compressed-air leak in this room in 15 seconds, with a €100 prototype and an AMD GPU — the €10,000 camera is an audit fee nobody should pay per site ever again."**

Fill the € with your calibrated card; fill the seconds with your benchmark; then let the judges pick the corner.
