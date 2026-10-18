---
format: 1920x1080
duration: 90s
message: "Your expert films a job once; Ghost Expert coaches every new hire and stops them before they skip a safety step, on one AMD GPU."
arc: Hook → Author → Coach → The stop → Why it's safe → Ask + record → AMD → Close
audience: AMD Developer Hackathon judges, Track 1 Intelligent Industry
mode: autonomous
music: none
---

## Frame 1 — The expert leaves

- scene: Huge lowercase "she retires next year." on black; a 30-year counter ticks; the words fade like a ghost
- duration: 8.438s
- transition_in: cut
- status: animated
- voiceover: "Your best technician retires next year. Thirty years of knowing which step gets people hurt. When she leaves, that knowledge leaves with her."
- src: compositions/frames/01-hook.html

The problem, in human terms. No product yet.

## Frame 2 — Film it once

- scene: Author view: a video timeline splits into 8 numbered step cards; two carry a red safety triangle; an APPROVED stamp lands
- duration: 15.595s
- transition_in: crossfade
- status: animated
- voiceover: "With Ghost Expert, she films the job once and talks through it. Whisper, SigLIP and Gemma cut the video into eight steps, each with a visual check and a safety flag. She fixes what's wrong and approves. The expert owns the procedure. The AI only drafts it."
- src: compositions/frames/02-author.html

## Frame 3 — The coach

- scene: Coach view: top-down camera tile, step bar fills green 1→2→3, subtitle of the spoken next step, Gemma observation chip top-right
- duration: 7.967s
- transition_in: crossfade
- status: animated
- voiceover: "Now a new hire does the same job under a camera. Each step turns green as Gemma confirms it, and a voice says what comes next."
- src: compositions/frames/03-coach.html

## Frame 4 — The stop

- scene: Hand reaches for cover screws; the whole frame flashes fire-orange red; STOP banner "you haven't done step 4"; expert clip panel grows to half the screen
- duration: 11.886s
- transition_in: cut
- status: animated
- voiceover: "Here is the mistake that hurts technicians: opening the guard before testing that the machine is dead. The screen goes red. Stop. You haven't done step four. Her own hands show how, until the trainee does it."
- src: compositions/frames/04-stop.html

The hero moment. Orange register.

## Frame 5 — It never decides alone

- scene: Three-tier diagram SigLIP → Gemma ×2 → rule engine; then a two-bar compare: false stops 14% vs 0%, labelled SIMULATION
- duration: 24.111s
- transition_in: crossfade
- status: animated
- voiceover: "A vision model is sometimes confidently wrong, so it never decides alone. SigLIP watches every frame. Gemma checks two steps in parallel. A deterministic rule engine owns the state, and a stop needs two agreeing checks on different frames. In simulation, with a model that is wrong five percent of the time, false stops on correct trainees fall from fourteen percent to zero."
- src: compositions/frames/05-engine.html

Numbers from eval/sim_results.md only. Always labelled as a simulation.

## Frame 6 — Ask, then the record

- scene: Speech bubble "where does the filter go?" → expert clip; then the training record card: time per step bars vs expert, 1 safety stop caught, verdict NEEDS ANOTHER RUN
- duration: 10.188s
- transition_in: crossfade
- status: animated
- voiceover: "Ask out loud where the filter goes, and her clip answers. At the end, the training manager gets a record: time per step, mistakes caught, competent or not."
- src: compositions/frames/06-record.html

## Frame 7 — One AMD GPU

- scene: One big GPU block labelled AMD INSTINCT · ROCm · vLLM, four model tiles snap in: Gemma 3, SigLIP, Whisper, Kokoro
- duration: 9.3s
- transition_in: crossfade
- status: animated
- voiceover: "Four models, Gemma 3, SigLIP, Whisper and Kokoro, run together on one AMD Instinct GPU, served by vLLM on ROCm."
- src: compositions/frames/07-amd.html

## Frame 8 — Film them

- scene: Orange register, giant "film them." with the Ghost Expert wordmark and hackathon line
- duration: 3.448s
- transition_in: crossfade
- status: animated
- voiceover: "Every plant has someone about to retire. Film them."
- src: compositions/frames/08-close.html
