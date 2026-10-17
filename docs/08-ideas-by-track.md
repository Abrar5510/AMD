# 08 — Idea Bank: What to Build in Each Track

> Companion to the track briefs in [tracks/](tracks/). Every idea here is filtered through what the judges actually reward: **Application of Technology · Business Value · Originality · Presentation** — plus the Vibe Generation special prize (Hybrid / Becreatives / Vibe Generation) and the partner prizes (Google Gemma, Evolus).

## Reading guide

- Each track gets **5 ideas**, then a **shortlist** and a **fast lane** (what to build if hours are short).
- ⚙️ = where AMD runs · 🎯 = the measurable claim for the slide · 🪝 = partner-prize hook.
- Recurring AMD split that works for almost every idea: an open LLM (**Gemma 3 / Qwen / Llama on vLLM + ROCm**) for reasoning and language, plus **one non-LLM model** (vision, anomaly, forecast, embeddings) also on the GPU. Slide line: *"the models are AMD's job; the product logic is ours."*

## Ground rules for every idea

- Pick **one public dataset** — demoed-with-realistic-data beats an unfinished live integration.
- Ship the thin vertical slice first: **input → model → decision → human review gate → output**. Judges want a working product, not a platform.
- Put **one number, explained** on the slide: "we measured X, computed by Y" beats ten vague claims.
- The six Evolus **sample use cases are traps for originality** if cloned — go beyond them (see Evolus section).

---

## Track 1 — Intelligent Industry

> Factories have data everywhere; the hard part is knowing what matters and what to do next.

### 1.1 Sentinel — failure prediction with an operator-friendly explanation ⭐

- **Pitch:** Predict failures 24–48 h ahead from sensor windows, then explain the alert like a senior engineer: what is degrading, why, what to check, which manual page, and a draft work order.
- **User:** maintenance planner / line technician.
- **Demo:** replay a sensor stream (public sets: NASA IMS bearings, AI4I 2020 predictive maintenance), anomaly model fires at t → LLM writes the alert with manual references (RAG) → a work-order card is created. End on "caught X h before failure".
- **AMD:** anomaly model (autoencoder / LSTM / gradient boosting on windowed features) on ROCm + Gemma via vLLM for explanation + GPU embeddings over the manuals. 🪝 Gemma; Evolus (work-order workflow) to stack tracks.
- **🎯:** predicted lead time, downtime hours and € avoided, false-alarm rate, and **how the threshold was tuned** (say it — this is the credibility moment).
- **Why it wins:** anyone can prompt "predict failures"; a real model + a real explanation + a tuned threshold is the differentiator.

### 1.2 QCvision — visual defect detection + automatic shift report

- **Pitch:** Defect detection on a production line, with an operator loop (accept/reject corrections) and an LLM that turns the day's data into a shift report: "defect class X up 3× after the material batch change".
- **Demo:** train/run on **MVTec AD** (real industrial anomaly dataset) with PatchCore/PaDiM or YOLO-style detection on ROCm; operator UI with heatmap; report generated at end.
- **User:** QC operator + shift manager.
- **AMD:** vision inference on ROCm + LLM for the report; retraining job also on GPU if you show it.
- **🎯:** defect escape rate, inspection time per part, scrap € — measured on the demo dataset.
- **Fast visual win:** defect heatmaps are the most demo-friendly artifact in this track.

### 1.3 Guardian — safety monitoring on the CCTV the factory already has

- **Pitch:** PPE detection (helmet, vest, goggles), zone intrusion, person-down; incidents become a daily safety digest for the H&S manager; faces blurred before anything leaves the camera (privacy story).
- **Demo:** public PPE detection datasets; two scenarios (missing helmet in a zone; person down) shown as alerts + digest.
- **AMD:** detection + VLM (Gemma vision) for scene description on ROCm.
- **🎯:** near-miss reports captured per week (from ~0 today), time-to-intervention.
- **Why it wins:** safety + privacy + existing cameras = a credible buyer (plant H&S) and a strong pitch.

### 1.4 WattWatch — energy waste detective for SMEs

- **Pitch:** Per-machine energy data → detect idle/standby waste and anomalies vs. production volume → rank waste in € → LLM writes a one-page action plan with payback estimates.
- **Demo:** public or simulated per-machine meter data (NILM-style); forecast expected draw (Prophet/GBM) vs. actual; top-3 waste findings with € attached.
- **User:** plant manager / energy manager. Italy context: energy costs are a board-level topic for SMEs.
- **AMD:** forecasting + LLM explanation via vLLM; embeddings for similar historical findings.
- **🎯:** kWh and € per month saved, from the demo dataset.

### 1.5 Mechanic's Copilot — multilingual guided troubleshooting

- **Pitch:** Technicians ask in Italian/English/Romanian (real multilingual workforce in Italian factories); answers are step-by-step procedures with manual page citations and **escalation to a senior engineer when confidence is low**; success drafts the work order.
- **Demo:** two questions in two languages → cited procedure → one low-confidence case correctly escalated.
- **AMD:** multimodal RAG (text + diagrams) + Gemma on vLLM.
- **🎯:** search time per issue (e.g., 20 min → 30 s), first-time-fix rate.
- **⚠️ Note:** "chat with the manual" is the most common idea in this track — only pick it if the guided-procedure + escalation + multilingual parts are genuinely built.

> **Track 1 shortlist:** **Sentinel** (safest, strongest measurable) · **QCvision** (most visual demo) · **Guardian** (best story if you have PPE footage).
>
> **Fast lane:** Sentinel on one public bearing dataset, two assets, no live sensors; the "action" is a drafted work order you show being created end-to-end.

---

## Track 2 — Health & Wellbeing

> Make one part of the patient journey safer, clearer, or easier — with uncertainty visible and human review built in.

### 2.1 Dimissioni Chiare — discharge instructions patients actually understand ⭐

- **Pitch:** Hospital discharge letters → plain-language + multilingual (IT/EN/AR…) instructions: medication schedule, activity rules, **red-flag symptoms ("seek care if…")**, all with confidence badges; a nurse reviews and approves before anything reaches the patient.
- **Demo:** two synthetic discharge letters (one chronic, one post-op), output in two languages, one item flagged "needs nurse review" and one deliberately refused as too uncertain to translate.
- **User:** hospital discharge nurse + patient/caregiver.
- **AMD:** Gemma on vLLM for rewriting + medical-term embeddings; everything on your private endpoint, synthetic data only.
- **🎯:** nurse minutes per discharge (e.g., 40 → 15), follow-up calls avoided, comprehension proxy (percentage of sentences at target reading level).
- **Why it wins:** the human review gate is *inherent* to the product, not bolted on; Italyʼs multilingual population is a real, local problem.

### 2.2 PreVisit — intake that flags, never diagnoses

- **Pitch:** Conversational (text + optional voice) pre-visit intake in the patient's language → structured summary + **urgency flags routed to a nurse** + question list for the doctor.
- **Demo:** anxious narrative input → structured history with missing fields requested → one red-flag routed to human, everything else summarized.
- **AMD:** Whisper-style ASR + LLM on ROCm; pydantic-style schema validation before anything enters the record.
- **🎯:** intake completeness, nurse prep time, no-show rate.

### 2.3 ChartKeeper — record catch-up for GPs

- **Pitch:** Messy history (scanned labs, referrals, PDFs) → timeline + "what changed since the last visit" + missing screening checklist; every claim carries a **source link + confidence**; the doctor approves or edits.
- **Demo:** one scrambled patient folder → timeline, 3 changes, 2 gaps; doctor review UI with accept/edit.
- **🎯:** minutes per chart (e.g., 25 → 5), completeness of the disease-prevention checklist.

### 2.4 MedRec — medication reconciliation before it hurts someone

- **Pitch:** Compare three lists — discharge letter, pharmacy record, patient interview — and flag discrepancies by severity for a **pharmacist** to resolve. Never auto-changes anything.
- **Demo:** seeded discrepancies (duplicate therapy, wrong dose) → severity-sorted review queue → resolution recorded with audit trail.
- **🎯:** discrepancies caught per 100 patients, pharmacist minutes per review.
- **Why it wins:** medication errors at care transitions are a textbook patient-safety problem; the demo *is* the review workflow.

### 2.5 CarePath — caregiver navigator for chronic care

- **Pitch:** Families managing chronic conditions get help with appointments, exam preparation, transport, and paperwork; multilingual; prevention tips only from public-health sources, always with "ask your clinician".
- **Demo:** caregiver persona in two languages; appointment prep sheet + reminders + FAQ grounded in official sources.
- **User:** family caregivers (Italy: aging population, caregiver shortage).
- **🎯:** missed appointments, caregiver hours saved.

### Mandatory safety table — put all five rows on the slide

| Risk | Mechanism to demo |
|------|-------------------|
| Incorrect / unsupported responses | Every statement cites a source or is flagged; unsupported output is quarantined, not shown |
| Sensitive information | Synthetic demo data, private AMD-hosted endpoint, no PII in logs, on-prem story |
| Uncertain results | Confidence badges + "needs review" states visibly in the UI |
| High-risk decisions | Fixed refusal templates for diagnosis/dosage; routes to clinician instead |
| Human review | A real review gate (nurse/pharmacist/doctor) before anything reaches the patient, with audit trail |

> **Track 2 shortlist:** **Dimissioni Chiare** (best demo warmth + local relevance) · **MedRec** (strongest safety credibility).
>
> **Fast lane:** Dimissioni Chiare on two synthetic letters, IT + EN, and a genuine nurse-review UI state — not a mock.
>
> ⚠️ Avoid **MIMIC-style credentialed datasets** — they add days of paperwork. Synthetic letters are sufficient for the demo and safer.

---

## Track 3 — Reinvent Commerce

> Turn disconnected customer data into a useful recommendation or action — with forecasts that are real models, not vibes.

### 3.1 Saldi — markdown optimization for Italian fashion SMEs ⭐

- **Pitch:** Forecast demand per SKU/size/week (seasonality, weather, promo lift) → simulate markdown scenarios → recommend margin-optimal plan → LLM explains each recommendation and drafts the campaign copy.
- **Demo:** one store, ~50 SKUs; show **backtest (MAPE) vs. the naive "20% off after 4 weeks" rule** and margin recovered.
- **User:** indie fashion retailer / e-commerce manager. Italy = fashion district context judges know.
- **AMD:** LLM + embeddings on GPU; forecasting via gradient boosting is fine on CPU — keep the GPU part load-bearing (explanations, copy, embeddings) and say so.
- **🎯:** margin recovered €, sell-through %, forecast error vs. baseline.
- **Why it wins:** the track's ⚠️ forecasting rule is *the* filter — a visible "how this number was computed" panel is an easy Originality + Tech win.

### 3.2 Never Run — replenishment + expiry for grocery/pharmacy

- **Pitch:** Per-SKU/day demand forecast → reorder points and quantity suggestions → expiry watch for perishables → daily "top 10 actions" digest the owner can act on in 5 minutes.
- **🎯:** stockout %, spoilage €, working capital freed.

### 3.3 Voice of Customer — reviews and returns into a fix list

- **Pitch:** Embedding-cluster reviews + return reasons → aspect-level sentiment → ranked product/ops fixes → drafted support replies.
- **Demo:** real public review set; one product with a hidden defect pattern surfaced from returns + reviews together.
- **🎯:** rating trend, return rate, support backlog. (Not forecasting, so the LLM rule doesn't bite — but GPU embeddings do the clustering.)

### 3.4 WISMO Copilot — order-aware customer support

- **Pitch:** "Where is my order" resolved with real order/CRM context + policy RAG; multilingual; drafts (then sends) replies; hands tricky cases to a human.
- **Demo:** two tickets in two languages, one auto-resolved, one escalated with a draft.
- **🎯:** deflection rate, handle time. Pose common — differentiate with the *order data* integration and honest deflection numbers.

### 3.5 Churn Radar — subscriptions (gyms, telco-style SMEs)

- **Pitch:** Churn model on usage data → segment playbooks → LLM drafts win-back offers in brand voice.
- **🎯:** retention %, CLV protected, offers per saved customer vs. discount cost.

> **Bonus one-liners:** catalogue enrichment from supplier PDFs/images (measurable: % enriched, time saved); two-tower/A L S personal shopper for a specialty retailer (wine, food) explaining trade-offs — real recommender, not just a chatbot.
>
> **Track 3 shortlist:** **Saldi** (distinctive, nails the forecasting rule, Italy-native) · **Churn Radar** (cleanest unit economics).
>
> **Fast lane:** Saldi on a public e-commerce dataset (e.g., UCI Online Retail); one store; one backtest chart; one margin simulation. Skip weather/promo features if time is short — but keep the backtest.

---

## Track 4 — Create a New Kind of Experience

> Something that responds to its audience and is different for each person — not a one-off generated asset.

### 4.1 Museo Vivo — adaptive audio guide that reads the room ⭐

- **Pitch:** An audio guide that adapts to the visitor: a 7-year-old gets a story, an art historian gets context and controversy, a tourist gets it in their language — grounded in a **curator-approved fact base** so it never invents provenance.
- **Demo:** same artwork, two personas (child + historian), plus one live question ("show me the details of the armor") — visibly different experiences.
- **Buyer:** museums (per-ticket upsell or license). Italy = the strongest cultural-heritage market on earth.
- **AMD:** Gemma on vLLM for on-the-fly narration + TTS pipeline + RAG over curated texts (no-hallucination guardrail).
- **🎯:** cost per visit, dwell time uplift, languages covered. Quality control = curators + fact base + banned-claims list.

### 4.2 Race Story — personal recap films for mass-participation events

- **Pitch:** Runner photos + GPS splits + bib → a cinematic 45–60 s recap narrated in IT/EN ("she held 5:10/km until the hill at 32 km — then sprinted"). Two runners, two very different films.
- **Buyer:** race organizers (upsell per runner) — the Rome Marathon is the pitch slide.
- **🎯:** cost per runner (target < €0.50), attach rate, margin. This idea *forces* good unit economics — exactly what the track asks.

### 4.3 Storie — bedtime stories children co-create

- **Pitch:** The child invents with voice ("a fox who is afraid of the dark"), the story adapts to their reading level and the values parents chose, characters stay consistent across nights (memory), illustrations per scene.
- **Demo:** two children, two profiles → two different stories; parent control screen.
- **Buyer:** parents, subscription. Safety: content filters + parent-approval mode.

### 4.4 AccessAll — captions + audio description + dubbing from one clip

- **Pitch:** One video in → timed captions, audio-description track for blind viewers, translated dubbing (consented voices) out. Demo the same clip serving a deaf viewer and a blind viewer.
- **Buyer:** broadcasters / VOD platforms / corporate comms; per-minute pricing.
- **🎯:** cost per finished minute vs. today's manual cost; languages covered. "Wasn't practical before GenAI" = audio description at scale, honestly.

### 4.5 Studio One — campaign variant engine with brand guardrails

- **Pitch:** One campaign, N audience segments → each variant (copy, imagery, short video) locked to the brand kit (palette, tone, legal lines), a **consistency score**, and a human approval step before publish.
- **Demo:** two segment variants + the rejected/auto-fixed variant showing the guardrails working.
- **Buyer:** agencies / brand teams; cost per variant + CPM comparison.

### The five required answers — prepare one slide

| Question | Your slide |
|----------|------------|
| Team created | The content spine, fact base, brand/curation rules, review workflow |
| Models generated/decided | Variants, narration, imagery, adaptation choices |
| Quality & consistency | Fact base + style locks + banned-claims lists + review queue + similarity checks |
| Cost per experience | GPU-minutes × rate + API calls, shown as € per unit |
| Who pays, why | Museum / race organizer / parents / agency — price vs. value in one line |

> **Track 4 shortlist:** **Museo Vivo** (taste, originality, Italy, hybrid curators) · **Race Story** (cleanest unit economics).
>
> **Fast lane:** Museo Vivo with 8 artworks, 2 personas, curator-approved fact base; measure one artwork end-to-end including cost per visit.

---

## Evolus Track — Business Agents on AMD

> An agent that runs a real business process end-to-end. **Do not clone the six sample use cases** — they are the floor, not the bar.

### E.1 GaraBot — public-tender bid/no-bid agent ⭐

- **Pitch:** Tender PDFs (gare d'appalto) arrive by email/portal → extract requirements, deadlines, and certifications → match against the company profile and **past bids (knowledge library)** → bid/no-bid recommendation, checklist, and calendar entries; the bid manager approves the hand-off.
- **Why it wins:** public procurement is a huge, painful, Italy-specific process nobody automates with an agent like this; Originality is nearly free here.
- **Building blocks (4+):** document extractor (tender) + knowledge library (past bids) + workflow + AI Tool + email MCP.
- **🎯:** hours of bid screening per week, tenders considered vs. missed.

### E.2 Supplier Compliance Sentinel — visura/DURC/insurance expiry watch

- **Pitch:** Supplier compliance documents arrive → extract entity, document type, validity dates → alert before expiry → escalate to procurement; a compliance dossier per supplier.
- **Why it wins:** construction/industrial buyers in Italy must police DURC validity constantly; measurable = zero-expired-supplier %.
- **Blocks:** extractor + workflow + AI Tool + email/managing-system MCP.

### E.3 8D Quality Agent — customer complaint to draft CAPA

- **Pitch:** Complaint email → extract product/lot/defect → pull QC context from documents → draft an 8D/CAPA report → QA manager reviews and sends; recurrence tracking.
- **Combo play:** pairs with Track 1 (the same factory story end-to-end). 🪝
- **🎯:** time-to-8D, recurrence rate, complaint backlog.

### E.4 Claim Intake — insurance broker front desk

- **Pitch:** Claim email + attachments → extract fields → validate the policyholder (API/MCP) → auto-request missing documents in the client's language → escalate to the broker; SLA timer per claim.
- **🎯:** time-to-first-response, % complete files at first touch.

### E.5 Short-let Compliance Concierge *(bonus — thinner business value)*

- **Pitch:** Guest messages in any language → answers from the property knowledge base → tourist-tax and national-ID-code reminders → escalate urgent cases; host dashboard.
- **Buyer:** property managers; Italian short-let rules make it concrete.

### Make the workspace verifiable (they inspect it)

- [ ] Your **own vLLM endpoint on AMD Developer Cloud** connected to the workspace — resolve Open Question #6 with the Evolus team first.
- [ ] **≥2 building blocks visibly used — use 4+** (workflow, extractor, AI Tool, library, MCP, sub-agent).
- [ ] All actions driven **through the Evolus APIs**; the calls show up in usage stats.
- [ ] Container + public repo + README that runs; **all keys in env vars**.

> **Evolus shortlist:** **GaraBot** (original + clear value) · **8D Quality Agent** (stacks with Track 1).
>
> **Fast lane:** GaraBot with 3 tender PDFs and one company profile: extract → bid/no-bid → checklist → approval email. Container + README from hour one.

---

## Cross-cutting: how to stack prizes

| Prize | What unlocks it |
|-------|-----------------|
| AMD main prizes | Working product + demo-visible AMD workload (all shortlists above) |
| Google $5,000 | Run **Gemma** on your AMD endpoint inside the product — nearly free to add to any idea above 🪝 |
| Evolus (€1,011.50 + credits + showcase) | Full Evolus workspace requirements (own vLLM endpoint, ≥2 blocks, API-driven) |
| Vibe Generation special (AirPods 5) | Quantified value (€ per unit, savings, margin) + shipped execution + taste — every shortlist aims at this |
| Imment incubation (€1,599 × 3) | Frame the pitch as a startup: named user, market size, pricing, first customer |

## The 0 → demo checklist (any track)

- [ ] One dataset, one user, one number.
- [ ] Thin vertical slice: input → model → decision → human gate → output.
- [ ] AMD workload visible in the video (model card, endpoint log, or terminal running the GPU job).
- [ ] The number is explained in-product ("how this was computed" panel), not only on a slide.
- [ ] Demo video recorded early as rehearsal — re-record with the same script every time it improves.
