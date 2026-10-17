# 11 — Wow Ideas: What the Other Hundred Teams Won't Build

> Companion to [08-ideas-by-track.md](08-ideas-by-track.md), [09-idea-catalog.md](09-idea-catalog.md) and the hostile panel in [10-hostile-review-and-upgrades.md](10-hostile-review-and-upgrades.md).
> The bank in 08/09 was optimized for safe delivery. This file is optimized for the one thing hackathon judging actually rewards: **a 15-second moment the judges retell at dinner.** Every idea here is *grounded* (real user, real pain, real data path, real buyer) and *scarce* (no other team in the room will have it).

## Why the old ideas felt basic — and the bar for this set

The old set failed a simple test: **a teammate from another team could clone it in one evening** ("chat with the manual", "predict failures", "generate a campaign"). Defensible, forgettable.

The bar for everything below:

1. **One visceral moment.** The wow must be the first 15 seconds of the demo — something seen, heard, or watched happening, not explained.
2. **Not a pattern, an object.** It's not "LLM summarizes X". It's a thing: a camera for sound, a briefing that catches a cover-up, a spaceship for an MRI.
3. **Grounded, not random.** Every idea cites the real practice it replaces, the real data it runs on, and the person who pays.
4. **The GPU visibly sweats.** AMD judges need to see compute, not a wrapper: frames/sec, tokens/sec, seconds-per-asset on screen.
5. **Buildable with a fallback.** Each idea has a risk-first plan and a labeled fallback — wow dies from a broken demo, never from honesty.

Four kinds of wow recur — pick the one your team is best equipped to deliver:

| Kind | The feeling | Ideas |
|------|-------------|-------|
| **See the invisible** | "That was already there?!" | Sibilo, Turno |
| **Talk to what's gone / bring it back** | "It answered me." | Agorà, Rilancio |
| **Real-time, before your eyes** | "It's doing that *now*?" | Eco, Tondo |
| **The emotional helper** | "Oh. That's beautiful." | Countdown, Paziente A |
| **Money that was hiding** | "How much was I leaving on the table?" | Tesoro, La Trattativa |

---

## Track 1 — Intelligent Industry

### Sibilo — the camera for sound ⭐

**The 15-second wow:** A hiss plays from a corner of the room. On screen, a floorplan lights up — a red blob converges on the corner in two seconds. A card appears: *"compressed-air leak · €4,800/year · fix ~€90 · payback 6 days."* Then a second sound: a machine whine gets classified as *"bearing wear — ticket drafted,"* not a leak. The judges just watched the invisible become a map, live.

**Why it's scarce:** every industrial team in the room trains anomaly models on downloaded vibration datasets. Nobody works with **sound as an image**. This is the most physically impressive artifact anyone can put on screen this weekend.

**Grounded in:** compressed-air leaks are a classic industrial audit item (industry studies commonly put leak losses at 10–30% of compressed-air cost); professional ultrasound leak detectors are a real $3–10k instrument category rented for audit days. We're rebuilding that instrument with a cheap mic array and GPU beamforming — a real practice, radically cheaper.

**AMD runs:** batched FFT + GCC-PHAT beamforming across hundreds of directions per second + a sound-classification CNN — all on ROCm. On-screen counter: *directions scanned/sec, audio-frames/sec*. This is real compute, not a prompt.

**Build plan:** real beamforming + classifier + UI; audio source played from a Bluetooth speaker at a known position in the demo room (a real acoustic source is a legitimate test — label it); fallback = record one hiss and convolve it with virtual 8-mic delays (still real DSP on GPU). Let the demo *be* a blinded test: judges pick the corner, then the map finds it.

**Buyer + number:** energy consultants and compressed-air service companies (they sell leak audits); € found per session, payback weeks; per-site subscription or per-audit pricing.

**Track fit:** Track 1 — "use resources more efficiently", with object-level wow.
**Panel kill shot + answer:** *"Toy array, real instruments cost $10k."* → "We show localization accuracy against known source positions, and we're 100× cheaper; the last-mile calibration is the pilot."

> 📋 **Full build plan for this idea:** [12-sibilo-build-plan.md](12-sibilo-build-plan.md) — hardware decision tree, SRP-PHAT on ROCm, classifier, demo script, hour-by-hour schedule, risk register.

### Turno — the briefing that catches what the logbook hid

**The 15-second wow:** Shift change. The incoming foreman taps play and gets a 90-second audio briefing in their language. Mid-briefing the system stops him: *"The night log says 'all normal' — but bearing 3 rose 12°C above its band at 02:40, and a voice note at 03:52 mentions a 'rhythmic noise' that never made it into the logbook. Draft maintenance ticket attached."* The room goes quiet: the AI just caught the lie of omission.

**Why it's scarce:** everyone demos "summarize the logs." Nobody demos **contradiction between what people wrote, what the machines recorded, and what people actually said out loud** — delivered as a spoken briefing you'd play while walking the line.

**Grounded in:** shift handover is a documented top source of industrial incidents; voice notes are already used informally on many plant floors; "logbook optimism" is a real operations pathology. The product formalizes a ritual that exists everywhere and works nowhere.

**AMD runs:** Whisper-class ASR (voice notes in Italian/Romanian/English), LLM on vLLM for contradiction reasoning + briefing generation, TTS for the audio playback. Benchmark: audio-minutes processed/hour, tokens/sec.

**Build plan:** real pipeline end-to-end; corpus = generated sensor logs (AI4I/IMS-style) + **actually recorded** voice notes by the team in three languages (authenticity beats fake text). Two shifts, one buried contradiction, one drafted ticket, two languages in the demo.

**Buyer + number:** plant operations managers; metric: contradictions caught per 100 handovers, minutes-to-ready for the incoming shift; pilot on one line, price per asset.

**Track fit:** Track 1 — safety + uptime, with a story no chart can match.
**Panel kill shot + answer:** *"Another log summarizer."* → "Then why has no team here shown the briefing catching a contradiction? Ours does — watch it happen."

> One-line cousin for Track 1: **the no-new-hardware detector** — motor fault signatures (rotor bar, misalignment) read from the VFD's own current waveform, i.e., *"your machines already tell their health through the cables — we listen."* Cool for electrical judges; keep as a bullet on Sibilo's slide, not a second build.

---

## Track 2 — Health & Wellbeing

### Countdown — the rehearsal that turns the MRI into a spaceship ⭐

**The 15-second wow:** A 4-year-old is scared of the MRI tube. In sixty seconds the product generates *her* mission: "Giulia, you are the astronaut. The big camera is your rocket; your job is to stay still while it photographs your invisible superpowers." A second child (9, football-obsessed) gets a different mission. Then a live curveball: the parent types *"what if she sneezes?"* — and the mission script absorbs it in seconds. The room melts.

**Why it's scarce:** every health team builds documents (letters, summaries, intakes). Nobody builds **preparedness as an experience**. And nobody will — it looks like play, which is exactly why it wins.

**Grounded in:** procedural anxiety in children is real and measurable; preparation programs (child-life specialists use play, stories, and rehearsal daily) reduce distress and sometimes sedation needs — as an established care practice, not a medical claim. Hospitals have child-life teams doing this manually, one child at a time.

**AMD runs:** LLM + TTS + image generation on ROCm, with visible regeneration speed — "the mission for this child took 8 seconds; the re-write for the sneeze took 2."

**Build plan:** real pipeline, two personas, parent control screen with script editing, and a **child-life specialist approval gate** (the rehearsal is reviewed before use — human gate inherent to the product). No diagnosis, no treatment language anywhere: the product rehearses *what will happen*, it never says what anything means. Fallback: text story + TTS only; images as a bonus.

**Buyer + number:** children's hospitals and imaging centers; metric: pre-procedure distress, sedation rate (pilot measure, not a claim), child-life team hours saved per day. Price per department.

**Track fit:** Track 2, patient journey made *easier*, human review built in.
**Panel kill shot + answer:** *"Cute, but is it medicine?"* → "It's the practice child-life specialists already perform — play-based preparation — industrialized; a specialist approves every script."

### Paziente A — the training actor you can't book

**The 15-second wow:** A resident practices telling a simulated patient that the biopsy is positive. The voice-AI patient reacts like a person: asks "how long do I have?", goes silent, gets angry. After three minutes, the resident gets a feedback card: *"You delivered the news clearly. You said 'don't worry' three times — reassurance without acknowledgment. The patient went silent for 9 seconds — that was the moment to pause."* The judges all know this debrief; none of them have seen it without a human actor.

**Why it's scarce:** simulated patients are real practice — with **paid actors**, scarce and expensive; med schools ration them. A voice agent that reacts emotionally *and* scores communication behavior is a product nobody in this hackathon builds, and it's demo-able in a voice loop on stage.

**Grounded in:** breaking-bad-news and communication-skills training with simulated patients is standard in medical education; actor time is the bottleneck; structured feedback frameworks (e.g., acknowledge–pause–explore patterns) exist in the literature to build a defensible rubric.

**AMD runs:** real-time speech loop — ASR + LLM + TTS on ROCm; on-screen latency counter end-to-end ("600 ms — converses in real time"). This is one of the few ideas where *latency itself* is the visible tech.

**Build plan:** one scenario (bad news, oncology-adjacent), one expert-written rubric, push-to-talk voice or text fallback. Respect everywhere: the fictional patient is labeled as fictional, the scenario is fictional, the scoring is training feedback — never a clinical judgment.

**Buyer + number:** hospital education departments and medical schools; metric: practice reps per resident per year (10 → 100+), consistency of feedback, actor cost per session eliminated. Per-seat licensing.

**Track fit:** Track 2, staff side of the patient journey.
**Panel kill shot + answer:** *"Talking to an LLM isn't acting."* → "Watch the pause counter: it measures the interaction, not the prose. And the rubric is what educators already grade with."

---

## Track 3 — Reinvent Commerce

### Rilancio — the deadstock revivalist ⭐

**The 15-second wow:** A brand has 2,000 unsold jackets. On screen, the same garment gets **re-founded three times**: a Milan editorial story, a Berlin streetwear drop, a coastal-linen tourist story — each with its own imagery (conditioned on the actual garment photo), price point, channel, and forecast sell-through. Three markets, one jacket, three minutes. The judges just watched unsold inventory become sellable three different ways.

**Why it's scarce:** every other team pitches "campaign variants." The unit here is **the deadstock lot** — existing, already-produced, already-paid-for inventory — and the KPI is *sell-through of what exists*, not more content for new products. Sustainability + margin + taste in one artifact.

**Grounded in:** fashion overproduction is a documented industry problem (and EU textile-waste rules are tightening); deadstock marketplaces exist and clear lots at low prices precisely because "finding the story and the buyer" is manual work. This product automates the only step that recovers margin.

**AMD runs:** garment-conditioned image generation + style-signal embeddings + LLM copy on ROCm; on-screen: seconds per campaign, cost per campaign (cents), GPU utilization.

**Build plan:** one jacket, three market sketches, one price ladder with sell-through assumptions **labeled on the panel** ("simulated counterfactual; method shown"). Art direction locked to one visual reference so output looks designed, not generated. Fallback: two markets instead of three; images can become art-directed collages of the real product photo if generation quality wobbles.

**Buyer + number:** small brands and deadstock operators; sell-through uplift vs lot baseline, € recovered per garment, success fee per sold lot or subscription.

**Track fit:** Track 3 — action on real inventory — and Vibe Generation's taste criterion, deliberately.
**Panel kill shot + answer:** *"Another image generator."* → "The output isn't images; it's a plan: price, channel, and forecast per market. Images are how it's communicated."

### Tondo — the 3D showroom that builds itself

**The 15-second wow:** Three flat supplier photos of a chair go in; a fully spinnable 3D product comes out on the projector in ~90 seconds — judges drag it, rotate it, orbit it. Then a second item processes live while the first is still being admired. *"Your supplier sends flat photos. Your store shows 360°."*

**Why it's scarce:** ninety percent of the room is doing text. This is **visible 3D compute** — an asset factory, not a chat. It's also the single most AMD-shaped demo in the whole idea bank: reconstruction workloads that make the GPU sweat are literally what Instinct is built to do.

**Grounded in:** furniture and interiors e-commerce (an Italian specialty) gets terrible supplier photography as a matter of course; 3D/AR product views are a real conversion investment category; open single-image-to-3D models exist, are GPU-hungry, and run on a hackathon budget.

**AMD runs:** image-to-3D generation on ROCm; on-screen GPU utilization, seconds-per-asset, and a batch queue ("six chairs queued, done in eight minutes"). Attendees *see* the hardware working.

**Build plan:** 3 items from public product photos (or photograph a chair in the venue live — the honest wow). Web viewer with orbit controls. Label "prototype mesh quality; the pipeline is the point." Fallback: 2 items pre-rendered, 1 processed live; a quality gate chooses the best of two generations.

**Buyer + number:** furniture/interiors retailers and marketplace sellers; cost per 3D SKU vs studio photography (€200+/SKU → ~€2), days → minutes; conversion uplift as the pilot metric. Per-SKU pricing.

**Track fit:** Track 3 — product discovery, measurable commercial action.
**Panel kill shot + answer:** *"Proto meshes are rough."* → "We sell minutes and euros: 100× cheaper, 100× faster, pilot quality; the studio still handles hero shots."

---

## Track 4 — A New Kind of Experience

### Agorà — the piazza that talks back ⭐

**The 15-second wow:** Standing "in" the demo piazza, you ask a question and a 1750s fishmonger answers in dialect. Then you overhear **two characters argue** about the price of grain — and you can step in, take a side, change the outcome of the scene. Three voices, one place, sourced from real history — and they talk to each other, not just to you.

**Why it's scarce:** "chat with a historical figure" is a model-launch demo. **A place-anchored cast that argues, with memory of you, grounded in local sources** is an experience product: multi-agent, audio, geographically rooted. Nobody in the room will have the argument moment.

**Grounded in:** Italy's public squares are history-dense and every city monetizes them; location-based audio tours are an established spend category; the upgrade is obvious the moment you hear it — static tours become conversations.

**AMD runs:** 3 persona LLMs + TTS + ASR on ROCm, running concurrently; on-screen: three agents live, tokens/sec each. Multi-agent inference is a legitimate GPU demo.

**Build plan:** one piazza, three characters with source dossiers (published local histories, public domain), guardrails ("speak only what the dossiers support; otherwise say 'I couldn't know that'"), an argument scene that is scripted *in scenario* but responsive *in dialogue*. Fallback: two characters, text + TTS.

**Buyer + number:** tourism boards, tour operators, museum consortiums; per-visit pricing or license per city; metric: dwell time, second-question rate, languages launched.

**Track fit:** Track 4 — two audiences get two different experiences by construction (ask a merchant vs ask a magistrate).
**Panel kill shot + answer:** *"Historical characters have been done."* → "Individually, yes — as a cast that argues in place, no. And every line is source-grounded: ask it anything off-script."

### Eco — the stage that echoes in your language

**The 15-second wow:** A recorded Italian scene plays — and the English audience hears it in the actor's own voice, ~3 seconds behind, with a live latency counter on screen. Then someone on stage speaks a line **live** into the mic, and it comes out dubbed in English seconds later. The theater problem everyone recognizes, solved in front of them.

**Why it's scarce:** opera houses rent surtitle systems; conferences rent interpreter headsets *and interpreters*. Real-time, voice-preserving stage dubbing is rare because it was impractical — which is exactly the brief's "not practical before generative AI" clause, made literal.

**Grounded in:** Italy's theater and festival ecosystem programs heavily for international audiences; simultaneity is broken by surtitles and Chinese-whisper headsets; the production cost of a multilingual run is a real budget line.

**AMD runs:** streaming ASR → MT → TTS with voice conversion, all on ROCm; on-screen: latency (ms per segment), real-time-factor < 1 — "the pipeline runs faster than the play."

**Build plan:** one recorded scene + one live line moment; **consented teammate voices only** for conversion (say it on the slide — the ethics is part of the pitch); label latency honestly ("near-live; the last 300 ms is engineering, not magic").

**Buyer + number:** theaters, festivals, touring companies; per-production pilot, per-seat or per-run pricing; metric: cost per seat vs interpreter headsets, languages per production.

**Track fit:** Track 4 — same play, different experience per audience; accessible media adjacency.
**Panel kill shot + answer:** *"Voice cloning."* → "Consented performers' voices, owned by the production, deleted after the run — and the actors can revoke. The tech is the message here."

---

## Evolus Track — Business Agents on AMD

### Tesoro — the money you were leaving on the table ⭐

**The 15-second wow:** An SME wants to buy a €400k machine and re-lamp the plant. The agent finds three applicable incentives, **detects that two of them legally cannot be stacked** (citing the rule text, page and clause), computes the optimal legal stack — *"€146,000"* — checks each against the company profile and deadlines, and drops two application packs plus a calendar into the workflow. The judges realize this is the thing every SME in Italy pays an accountant for.

**Why it's scarce:** GaraBot looks at tenders a company must find. Tesoro looks at **money the company is entitled to but doesn't claim**, and — the killer feature — resolves the *stacking conflicts* that make SMEs give up. Nobody automates the legality of combinations; that's the actual expertise.

**Grounded in:** Italy's incentive landscape (national tax credits, regional bandi, ZES measures) is real, layered, and famously hard to navigate; SMEs routinely leave eligible money unclaimed; accountants bill for exactly this analysis. All source texts are public documents.

**AMD + Evolus:** own vLLM endpoint on AMD Developer Cloud; five visible blocks — document extractor (bando PDFs → structured rules), knowledge library (company profile, past applications), workflow (application drafting + deadlines), email MCP (submission reminders), AI Tool (eligibility + stacking reasoning). Usage stats show all of it.

**Build plan:** one investment plan, four public bando excerpts (shortlisted for scope), one stacking conflict detected, two application drafts, and a mini **golden checklist** evaluation (survives the Inspector): "requirements extracted vs human checklist — precision/recall shown." Every cell cites the source clause. Fallback: three incentives, one conflict.

**Buyer + number:** accountants (commercialisti) and SMEs; € identified per plan, hours per application (days → hours), success-fee or per-plan pricing. The human gate is the accountant: the agent prepares, the professional signs.

**Track fit:** Evolus — a real process run end-to-end, original, Italy-native.
**Panel kill shot + answer:** *"One misread clause = a fine."* → "Every claim cites its clause; the accountant approves; the product's output is a *prepared file*, not a filing."

### La Trattativa — the procurement agent that haggles (wildcard)

**The 15-second wow:** A live negotiation: the buyer-agent receives a quote, counters with two levers (volume + payment terms), the simulated supplier pushes back, and the agent extracts a better price by walking the line — all in a transcript the room can read in real time. *"Your 3% became 7% because we knew the two things it cares about."*

**Why it's scarce:** everyone builds agents that *read* and *write*. Nobody builds one that **negotiates** — zero-sum, adversarial, verifiable if you show both transcripts.

**Grounded in:** supplier negotiation is a real procurement task with real money per point of discount; the demo counterparty is a simulated supplier (label it), the mechanisms (BATNA, walk-away price, concession ladders) are textbook.

**AMD + Evolus:** two LLM roles over the same vLLM endpoint + workflow + email MCP; building blocks visible.

**Build plan:** one category (packaging or components), one fact sheet per side, three negotiation rounds; scoring: discount captured vs walk-away price. Fallback: scripted supplier with fixed concession rules — still real on the buyer side.

**Kill shot + answer:** *"You scripted the supplier."* → "Yes — labeled. The product is the buyer's agent; the supplier bot is the test harness. Swap in a real counterparty and nothing changes."

> Evolus one-liner if Tesoro and La Trattativa don't fit: **the memory of the house** — every property's maintenance history, warranties, and quirks mined from WhatsApp, email, and invoices into a living manual that answers the next tenant, buyer, or plumber. Boring, real, and the pain (handover) is universal.

> More one-liners in this spirit: **the exhibition of you** (your photos/music/books → a museum-grade personal exhibition, Track 4, emotional); **the dentist's cartoon** (your own teeth → the kid's cartoon, Track 2); **the no-new-hardware motor detector** (VFD currents → fault signatures, Track 1).

---

## Choosing: risk-first, or you'll have a beautiful corpse

Wow ideas carry a bigger demo risk: hardware (Sibilo), latency (Eco, Paziente A), generation quality (Rilancio, Tondo). Three rules to de-risk:

1. **Risk-first build order.** Hours 1–6 are the risky core — the beamformer, the voice loop, the 3D pipeline. The UI is cheap; the core is not.
2. **One-wow scoping.** The demo shows exactly one magical moment, twice, flawlessly. Everything else is support.
3. **Record the moment early.** As soon as the core works once, screen-record it. The video submission then exists even if the live demo has a bad Sunday morning.

And keep the panel's armor slide ([10-hostile-review-and-upgrades.md](10-hostile-review-and-upgrades.md)): state the kill shot first, then answer it live.

## Top picks if you want maximum wow per hour

| Rank | Idea | Why | Build risk |
|------|------|-----|------------|
| 1 | **Sibilo** (T1) | An artifact nobody has ever seen; visible GPU math; 20 seconds to explain | Medium (array fallback ready) |
| 2 | **Countdown** (T2) | The most human moment available to any team this weekend | Low-medium (text fallback = still great) |
| 3 | **Tesoro** (Evolus) | Clear money, real rules, strong prize stacking; survives the Inspector | Medium (corpus scoping) |
| 4 | **Agorà** (T4) | The argument moment is unrepeatable by other teams | Medium (dossier quality) |
| 5 | **Tondo** (T3) | The most AMD-shaped GPU demo in the bank; visually undeniable | Medium-high (model quality) |

Honest tiebreak: if your team has *one* strong engineer and no hardware, take **Countdown** or **Tesoro**. If you have two strong engineers and a prop budget, take **Sibilo**. If your team is design-led, take **Rilancio** or **Agorà**.
