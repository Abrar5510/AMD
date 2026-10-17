# 09 — All the Ideas, Explained

> A readable catalog of every idea for the AMD Developer Hackathon, ACT III — what it is, who it's for, what the demo shows, where AMD runs, and the number that wins the room.

## How to read this

- [07-open-questions.md](07-open-questions.md) and the [tracks/](tracks/) briefs define the rules; this document is the **full explanation of every idea**.
- [08-ideas-by-track.md](08-ideas-by-track.md) is the same idea bank in quick-scan form (with "fast lane" build notes). This file is the longer, friendlier version.
- ⭐ marks the recommended pick in each track.
- Every idea follows the same five lines so you can compare quickly:
  - **For** — the user
  - **Demo** — what the judges actually see
  - **AMD runs** — the demo-visible AMD workload
  - **Measured number** — the impact you claim (and can explain)
  - **Why it wins** — the scoring angle

## Contents

1. [Track 1 — Intelligent Industry](#track-1--intelligent-industry)
2. [Track 2 — Health & Wellbeing](#track-2--health--wellbeing)
3. [Track 3 — Reinvent Commerce](#track-3--reinvent-commerce)
4. [Track 4 — A New Kind of Experience](#track-4--a-new-kind-of-experience)
5. [Evolus Track — Business Agents on AMD](#evolus-track--business-agents-on-amd)
6. [Stacking prizes](#stacking-prizes-with-any-idea)

---

## Track 1 — Intelligent Industry

> *Brief: help factories spot problems earlier and operate better — reduce downtime, improve quality, increase safety, or use resources more efficiently.*

The common trap in this track is building a dashboard. Judging rewards a working product that turns industrial data into an action someone can take — so every idea below ends in a decision, an alert, or a drafted task, not a chart.

### 1.1 Sentinel — failure prediction that speaks the operator's language ⭐

Factories already log vibration, temperature, and current from every critical machine. The problem is nobody watches it until something breaks. Sentinel watches the streams for you, predicts a failure 24–48 hours ahead with a real anomaly model, and then explains the alert like a senior engineer would: what is degrading, why, what to check first, which manual page covers it — and it drafts the work order.

- **For:** the maintenance planner and the line technician.
- **Demo:** replay a public machine dataset (NASA IMS bearings, AI4I 2020) as a live sensor feed; the model fires an alert; the LLM writes the explanation with manual references (RAG); a work-order card appears. Close with "caught X hours before failure."
- **AMD runs:** the anomaly model (autoencoder, LSTM, or gradient boosting on windowed features) on ROCm, plus an open LLM (e.g. Gemma) on vLLM for explanations and embeddings for manual search.
- **Measured number:** predicted lead time before failure, downtime hours and € avoided, false-alarm rate — and how you tuned the threshold.
- **Why it wins:** anyone can claim "AI predicts failures"; a real model with a measured threshold and an explanation a technician can act on is something judges can verify on the spot.

### 1.2 QCvision — defect detection with an automatic shift report

Quality control on many production lines is still a human staring at parts; even where cameras exist, nobody connects the day's defects into a story. QCvision detects defects from camera images, learns from the operator's accept/reject corrections, and then an LLM turns the day's data into a shift report: "class X defects up 3× after the material batch change."

- **For:** the QC operator and the shift manager.
- **Demo:** detection running on **MVTec AD** (a well-known real industrial anomaly dataset) with a defect heatmap; the operator corrects one false positive; the shift report is generated at the end.
- **AMD runs:** vision inference on ROCm; the LLM writes the report.
- **Measured number:** defect escape rate, inspection time per part, scrap cost — all shown on the demo dataset.
- **Why it wins:** defect heatmaps are the most demo-friendly artifact in this track, and the self-written shift report proves the loop closes.

### 1.3 Guardian — safety monitoring on the cameras the factory already has

Most factories have CCTV everywhere but no way to see a missing helmet or a person down in a dangerous zone until after an incident. Guardian turns existing cameras into a safety observer: PPE detection (helmet, vest, goggles), zone intrusion, person-down alerts — with faces blurred before any data leaves the camera — and a daily safety digest for the H&S manager.

- **For:** the health & safety manager; the plant as a whole.
- **Demo:** two scenarios from public PPE datasets (a missing-helmet alert in a restricted zone; a person-down alert), then the safety digest.
- **AMD runs:** detection plus a vision-language model (e.g. Gemma with vision) describing the scene, on ROCm.
- **Measured number:** near-miss reports captured per week (from roughly zero today) and time-to-intervention.
- **Why it wins:** safety, privacy, and no new hardware is a credible buyer story that non-technical judges immediately understand.

### 1.4 WattWatch — the energy waste detective for factories

Italian SMEs feel energy prices at board level, but nobody knows which machine wastes what. WattWatch reads per-machine energy data, separates idle/standby waste from productive draw, flags anomalies against production volume, ranks findings in €, and has the LLM write a one-page action plan with payback estimates.

- **For:** the plant manager and the energy manager.
- **Demo:** public or simulated meter data; expected consumption (forecast) vs. actual; top three waste findings with € attached and a drafted action plan.
- **AMD runs:** forecasting plus the LLM explanation on the GPU endpoint; embeddings to find similar past findings.
- **Measured number:** kWh and € saved per month, computed from the demo dataset.
- **Why it wins:** it converts a hard engineering topic into money a manager can act on — the definition of "useful result" for this track.

### 1.5 Mechanic's Copilot — multilingual guided troubleshooting

Italian factories run with multilingual workforces, and the knowledge lives in one senior engineer's head and a shelf of manuals. This copilot lets a technician ask in Italian, English, or Romanian and get a step-by-step guided procedure with manual page citations — and, crucially, a clean escalation to a human engineer when confidence is low. A resolved question can draft the work order automatically.

- **For:** floor technicians and the engineering team.
- **Demo:** two questions in two languages → cited procedures; one deliberately low-confidence case is escalated correctly.
- **AMD runs:** multimodal RAG (text and diagrams) with an open LLM on vLLM.
- **Measured number:** search time per issue (e.g. 20 minutes → 30 seconds) and first-time-fix rate.
- **Why it wins — with a warning:** "chat with the manual" is the most common idea in this track. Only pick it if the guided procedures, the escalation logic, and the multilingual coverage are genuinely built — otherwise it reads as a thin RAG demo.

> **Shortlist:** Sentinel is the safest with the strongest measurable; QCvision is the most visual; Guardian has the best story if you have PPE footage. **Fast lane:** Sentinel on one public bearing dataset, two assets, no live sensors — the action is a drafted work order you show end-to-end.

---

## Track 2 — Health & Wellbeing

> *Brief: make one part of the patient journey safer, clearer, or easier — with uncertainty visible and human review built in.*

This track's rules are strict: no autonomous diagnosis or treatment advice, and the demo must show how you handle wrong answers, sensitive data, uncertainty, high-risk decisions, and human takeover. Ideas where the human gate is **inherent to the product** score best, because you're demonstrating the safety design rather than bolting it on. Use synthetic data — it's sufficient and avoids privacy and credentialing delays.

### 2.1 Dimissioni Chiare — discharge instructions patients actually understand ⭐

Hospital discharge letters are written for doctors, not for the exhausted daughter taking grandpa home. Dimissioni Chiare turns a discharge letter into plain-language instructions in the patient's language: medication schedule, activity rules, and clear red flags for when to seek care. Every sentence carries a confidence badge, and a nurse reviews and approves everything before it reaches the patient.

- **For:** hospital discharge nurses; patients and family caregivers.
- **Demo:** two synthetic discharge letters (one chronic, one post-op), output in two languages; one item is flagged "needs nurse review" and one is refused as too uncertain to state.
- **AMD runs:** an open LLM on vLLM for the rewrite, plus medical-term embeddings — all on a private endpoint with synthetic data only.
- **Measured number:** nurse minutes per discharge (e.g. 40 → 15), follow-up calls avoided, share of sentences at the target reading level.
- **Why it wins:** the human review gate is an inherent part of the product, and multilingual patient communication is a real, local problem in Italy.

### 2.2 PreVisit — intake that flags, never diagnoses

Patients arrive with a story and ten minutes to tell it. PreVisit runs a conversational pre-visit intake (text, optionally voice) in the patient's language, turns it into a structured summary, flags urgency signals that route straight to a nurse, and prepares the question list the doctor will want.

- **For:** clinic staff and patients.
- **Demo:** an anxious, unstructured narrative → structured history with missing fields politely requested → one red flag routed to a human; everything else summarized for the visit.
- **AMD runs:** speech recognition (Whisper-style) and the LLM on ROCm; strict schema validation before anything enters a record.
- **Measured number:** intake completeness, nurse preparation time, no-show rate.
- **Why it wins:** triage-with-handoff is exactly the behavior the brief asks for — and the product explicitly refuses to diagnose.

### 2.3 ChartKeeper — record catch-up for family doctors

A GP reopening a patient's file faces years of scattered labs, referrals, and PDFs. ChartKeeper builds a clean timeline, shows what changed since the last visit, lists missing screenings, and attaches a source link and confidence level to every claim. The doctor approves or edits each item — nothing is taken on faith.

- **For:** general practitioners and their staff.
- **Demo:** one scrambled patient folder → timeline, three key changes, two care gaps; the doctor review UI with accept/edit actions.
- **AMD runs:** the LLM and embeddings on the GPU endpoint.
- **Measured number:** minutes per chart (e.g. 25 → 5) and completeness of the prevention checklist.
- **Why it wins:** every statement cites its source, which is a direct, visible answer to "how do you catch incorrect or unsupported responses?"

### 2.4 MedRec — medication reconciliation before it hurts someone

Medication errors cluster at care transitions, when the hospital list, the pharmacy list, and what the patient is actually taking don't match. MedRec compares the three, flags discrepancies by severity, and puts them in a review queue for a **pharmacist** to resolve. It never changes anything on its own.

- **For:** pharmacists and transition-of-care teams.
- **Demo:** seeded discrepancies (a duplicate therapy, a wrong dose) → severity-sorted review queue → resolution recorded with an audit trail.
- **AMD runs:** document extraction and comparison with the LLM on ROCm.
- **Measured number:** discrepancies caught per 100 patients, pharmacist minutes per review.
- **Why it wins:** it is a textbook patient-safety problem, and the review workflow *is* the demo — the human-in-the-loop requirement becomes the product's core screen.

### 2.5 CarePath — a navigator for family caregivers

Families managing chronic conditions drown in appointments, exam preparations, transport, and paperwork — often in a second language. CarePath walks caregivers through each step, in their language, with prevention information drawn only from public-health sources and an explicit "ask your clinician" boundary everywhere.

- **For:** family caregivers (Italy's aging population makes this concrete).
- **Demo:** a caregiver persona in two languages; an appointment preparation sheet, reminders, and an FAQ grounded in official sources.
- **AMD runs:** the LLM and document processing on the GPU endpoint.
- **Measured number:** missed appointments and caregiver hours saved.
- **Why it wins:** the wellbeing-and-prevention angle stays safely on the right side of the no-medical-advice line.

### The five safety questions — prepare all rows

| Risk | What your demo shows |
|------|----------------------|
| Incorrect / unsupported responses | Every statement cites a source or is flagged; unsupported output is quarantined, not shown |
| Sensitive information | Synthetic demo data, private AMD-hosted endpoint, no personal data in logs |
| Uncertain results | Confidence badges and "needs review" states visible in the UI |
| High-risk decisions | Fixed refusal templates for diagnosis or dosage questions; routes to a clinician instead |
| Human review | A real review gate (nurse, pharmacist, doctor) before anything reaches the patient, with an audit trail |

> **Shortlist:** Dimissioni Chiare has the best demo warmth and local relevance; MedRec has the strongest safety credibility. **Fast lane:** Dimissioni Chiare on two synthetic letters, Italian + English, with a genuine nurse-review UI state — not a mock.

---

## Track 3 — Reinvent Commerce

> *Brief: help a business understand its customers and take better action — attract, serve, convert, or retain.*

One rule shapes this whole track: if you predict demand, sales, or behavior, a language model cannot be the only method — you need a real statistical or ML forecast, and you must explain how it was calculated. The winning move is making that explanation a visible part of the product: a "how this number was computed" panel judges can click.

### 3.1 Saldi — markdown optimization for fashion retailers ⭐

Indie fashion retailers discount on instinct: "20% off after four weeks" for everything. Saldi forecasts demand per SKU, size, and week (seasonality, weather, promotion lift), simulates markdown scenarios, and recommends the margin-optimal plan — with the LLM explaining each recommendation in plain language and drafting the campaign copy.

- **For:** independent fashion retailers and e-commerce managers — a very Italian context.
- **Demo:** one store, ~50 SKUs; a backtest (MAPE) against the naive "20% off after four weeks" rule, plus the margin recovered by the recommended plan.
- **AMD runs:** the LLM for explanations and copy, plus embeddings — keep the GPU part load-bearing and say so on the slide; gradient-boosted forecasting itself is fine on CPU.
- **Measured number:** margin recovered (€), sell-through percentage, forecast error versus baseline.
- **Why it wins:** the forecasting rule is this track's filter, and a visible backtest plus a margin simulation turns it from a constraint into an originality point.

### 3.2 Never Run — replenishment and expiry for grocery and pharmacy

Small retailers alternate between empty shelves and expiring stock. Never Run forecasts demand per SKU per day, converts it into reorder points and quantities, watches expiry dates on perishables, and delivers a daily top-10 action list the owner can clear in five minutes.

- **For:** grocery and pharmacy owners.
- **Demo:** a demand forecast with reorder suggestions, an expiry alert, and the daily action digest.
- **AMD runs:** the LLM digest and embeddings on the GPU; forecasting on CPU or GPU, your choice.
- **Measured number:** stockout percentage, spoilage cost, working capital freed.
- **Why it wins:** two measurable pains (lost sales and waste) in one product, with an action list instead of a dashboard.

### 3.3 Voice of Customer — reviews and returns into a fix list

Reviews and return reasons contain the truth about a product, but they sit in different systems. This tool clusters reviews using embeddings, attaches sentiment to product aspects, combines them with return reasons, and produces a ranked fix list for the product team — plus drafted replies for support.

- **For:** e-commerce product managers and support leads.
- **Demo:** a public review dataset; one product where a hidden defect pattern surfaces only when returns and reviews are read together.
- **AMD runs:** GPU embeddings for the clustering; the LLM writes the findings and replies.
- **Measured number:** rating trend, return rate, support backlog.
- **Why it wins:** this is not forecasting, so the LLM rule doesn't bite — but the GPU embeddings keep AMD meaningful in the pipeline.

### 3.4 WISMO Copilot — customer support that knows the order

"Where is my order?" is most of a small shop's support load. This copilot answers from the actual order and CRM data plus policy documents, in the customer's language, drafts and sends replies, and hands genuinely tricky cases to a human with a draft attached.

- **For:** e-commerce support teams.
- **Demo:** two tickets in two languages — one auto-resolved from order data, one escalated with a prepared draft.
- **AMD runs:** the LLM on vLLM; embeddings over the policy library.
- **Measured number:** deflection rate and average handle time.
- **Why it wins — with a warning:** support agents are a crowded idea; the differentiator must be the real order-data integration and honest, measured deflection numbers.

### 3.5 Churn Radar — for subscription businesses

Gyms, clubs, and small subscription services lose members silently. Churn Radar scores each customer's risk from usage data, groups them into segments with playbooks, and has the LLM draft win-back offers in the brand's voice.

- **For:** subscription SMEs (gyms, local services, utilities-style).
- **Demo:** risk scores for a sample customer base → one segment playbook → two drafted win-back offers.
- **AMD runs:** the LLM drafts and explanations on the GPU.
- **Measured number:** retention percentage, customer value protected, offer cost per saved customer.
- **Why it wins:** the unit economics are clean — "we spend €X to keep €Y of revenue" is exactly the slide Vibe Generation's Hybrid criterion wants.

> **Bonus one-liners:** *catalogue enrichment* from supplier PDFs and images (measured by percentage of catalogue enriched and time saved); *personal shopper for a specialty retailer* (wine, specialty food) using a real recommender plus LLM explanations — a genuine two-tower or ALS model, not just a chatbot prompt.
>
> **Shortlist:** Saldi is distinctive and Italy-native; Churn Radar has the cleanest unit economics. **Fast lane:** Saldi on a public e-commerce dataset (e.g. UCI Online Retail), one store, one backtest chart, one margin simulation. Skip weather and promo features if time is short — keep the backtest.

---

## Track 4 — A New Kind of Experience

> *Brief: build a media, marketing, or entertainment experience that wasn't practical before generative AI — something that responds to its audience and is different for each person.*

Two hard rules: the demo must show the experience **changing for at least two audiences or inputs**, and you must explain five things — what the team made, what the models made, how you controlled quality, what each experience costs, and who pays. The ideas below were chosen because all five answers are natural for them.

### 4.1 Museo Vivo — an audio guide that reads the room ⭐

Museum audio guides say the same thing to everyone. Museo Vivo adapts: a seven-year-old hears the painting as a story, an art historian gets context and controversy, a tourist gets it in their own language — all grounded in a curator-approved fact base so the guide never invents provenance. Visitors can also ask questions live.

- **For:** museums and cultural sites; the visitor is the end user.
- **Demo:** the same artwork explained for two personas, plus one live question ("show me the details of the armor") — visibly different results in one run.
- **AMD runs:** the LLM on vLLM generating narration, a text-to-speech pipeline, and retrieval over curated texts with a no-invention guardrail.
- **Measured number:** cost per visit, dwell-time uplift, languages covered.
- **Why it wins:** taste, originality, and a hybrid human-AI workflow (curators define truth, AI adapts delivery) — precisely the Vibe Generation criteria — in the strongest cultural-heritage market there is.

### 4.2 Race Story — personal recap films for mass-participation events

After a marathon, every runner gets the same generic photo link. Race Story turns each runner's photos, GPS splits, and bib data into a cinematic 45–60 second film with real commentary: "she held 5:10/km until the hill at 32 km — then sprinted." Two runners, two completely different films.

- **For:** race organizers, who sell it as an upsell to each runner (the Rome Marathon is the pitch slide).
- **Demo:** two runners — a personal best and a first-timer — produce two films in Italian and English.
- **AMD runs:** the LLM writes the commentary on vLLM; image selection and TTS complete the pipeline.
- **Measured number:** cost per runner (target under €0.50), attach rate, margin per event.
- **Why it wins:** it forces good unit economics — exactly what this track's cost-per-experience requirement is testing.

### 4.3 Storie — bedtime stories children co-create

The child invents with voice ("a fox who is afraid of the dark"), and Storie builds the story around it — at the right reading level, with the values parents selected, keeping characters consistent night after night, with an illustration per scene.

- **For:** children and their parents; parents pay.
- **Demo:** two children with different profiles produce two different stories; the parent-control screen shows the guardrails.
- **AMD runs:** speech recognition, the LLM, and image generation on ROCm.
- **Measured number:** cost per story, subscription conversion, retention (do kids come back?).
- **Why it wins:** consistency across nights is the hard technical part, and it's visible in the demo.

### 4.4 AccessAll — captions, audio description, and dubbing from one clip

Accessibility is one of the clearest "not practical before generative AI" cases: audio description and dubbing at scale previously cost hours of human studio time per minute of video. AccessAll takes one clip in and produces timed captions, an audio-description track for blind viewers, and translated dubbing with consented voices.

- **For:** broadcasters, VOD platforms, and corporate communications teams; priced per finished minute.
- **Demo:** the same clip serving a deaf viewer (captions) and a blind viewer (description) — the two-audience requirement in one run.
- **AMD runs:** speech recognition, translation, and TTS on the GPU endpoint.
- **Measured number:** cost per finished minute versus today's manual cost; languages covered.
- **Why it wins:** an honest social-impact story with a straightforward per-minute business model.

### 4.5 Studio One — campaign variants with brand guardrails

One campaign, many segments — but brands fear losing control. Studio One generates a variant (copy, imagery, a short video) per audience segment, locks every output to the brand kit (palette, tone, legal lines), scores consistency, and routes everything through a human approval step before publishing.

- **For:** agencies and brand teams; the agency pays and resells.
- **Demo:** two segment variants plus one that gets auto-corrected or rejected by the guardrails — showing the safety net working.
- **AMD runs:** the LLM and image/video models on the GPU endpoint.
- **Measured number:** cost per variant and comparison against current agency cost per asset.
- **Why it wins:** the guardrail-and-approval workflow is the difference between "we generated images" and a product a brand would actually trust.

### The five required answers — one slide

| Question | Your slide |
|----------|------------|
| What did the team create? | The content spine, fact base, brand and curation rules, review workflow |
| What did the models generate or decide? | Variants, narration, imagery, adaptation choices |
| How did you control quality and consistency? | Fact base, style locks, banned-claims lists, review queue, similarity checks |
| What does each experience cost? | GPU-minutes × rate + API calls, shown as € per unit |
| Who would pay, and why? | Museum / race organizer / parents / agency — price versus value in one line |

> **Shortlist:** Museo Vivo has the taste and originality; Race Story has the cleanest unit economics. **Fast lane:** Museo Vivo with eight artworks, two personas, a curator-approved fact base, and one artwork measured end-to-end including cost per visit.

---

## Evolus Track — Business Agents on AMD

> *Brief: build an AI agent that runs a real business process end-to-end on Evolus, powered by an open model served on your own vLLM endpoint on AMD Developer Cloud.*

Warning first: the six sample use cases in the brief (invoice intake, support desk, lead qualification, contract review, multilingual documents, meeting follow-up) are traps for the originality score if you clone them. They are the floor, not the bar. These five go further — and the requirements are unforgiving, so read the checklist at the end.

### E.1 GaraBot — the public-tender bid/no-bid agent ⭐

Italian public procurement publishes thousands of tenders; SMEs either miss them or burn hours reading ones they can't win. GaraBot takes incoming tender documents, extracts requirements, deadlines, and certifications, matches them against the company profile and its past bids, and returns a bid/no-bid recommendation with a checklist and calendar entries. The bid manager approves the hand-off.

- **For:** the bid manager of a mid-sized Italian company.
- **Demo:** three real-format tender PDFs against one company profile → extraction → bid/no-bid scores → checklist → the approval email.
- **Building blocks used:** document extractor + knowledge library (past bids) + workflow + AI Tool + email MCP.
- **Measured number:** hours of bid screening per week saved; % of eligible tenders actually considered.
- **Why it wins:** a painful, Italy-specific process that nobody automates this way — originality is nearly free, and the value story writes itself.

### E.2 Supplier Compliance Sentinel — visura, DURC, insurance expiry watch

In Italian construction and industry, a supplier with an expired DURC or insurance certificate is a legal problem, and someone polices this with a spreadsheet. This agent extracts entity, document type, and validity dates from incoming supplier documents, alerts before expiry, escalates to procurement, and keeps a compliance dossier per supplier.

- **For:** procurement and compliance teams.
- **Demo:** documents arriving → extracted validity dates → an alert for one near-expiry and one blocked supplier.
- **Building blocks used:** extractor + workflow + AI Tool + MCP into email or the management system.
- **Measured number:** percentage of suppliers never expired; manual checks eliminated.
- **Why it wins:** compliance is binary and measurable — either the certificate was valid or it wasn't — which makes the business value impossible to dispute.

### E.3 8D Quality Agent — from customer complaint to draft CAPA

When an industrial customer complains, a quality engineer must assemble an 8D or CAPA report from emails, lot numbers, and QC records. This agent extracts the complaint, pulls the production context, drafts the report, and routes it to the QA manager for review — while tracking recurrence.

- **For:** QA managers in manufacturing.
- **Demo:** a complaint email → extracted product and lot → drafted 8D with the evidence attached → QA approval.
- **Building blocks used:** extractor + workflow + knowledge library + AI Tool.
- **Measured number:** time-to-8D, recurrence rate, complaint backlog.
- **Why it wins:** it pairs naturally with Track 1's factory story — the same customer, a second process — if you want one narrative across two tracks.

### E.4 Claim Intake — a front desk for insurance brokers

Brokers lose days collecting incomplete claim files. This agent reads the claim email and attachments, extracts the fields, validates the policyholder through an API or MCP connector, automatically requests missing documents in the client's language, and escalates to the broker with an SLA timer.

- **For:** insurance brokers and agencies.
- **Demo:** one complete claim auto-processed, one incomplete claim triggering a multilingual follow-up, one escalation.
- **Building blocks used:** extractor + workflow + MCP + AI Tool.
- **Measured number:** time-to-first-response; percentage of complete files at first touch.
- **Why it wins:** insurance back-office is a real spend category, and completeness percentages are clean, boastable metrics.

### E.5 Short-let Compliance Concierge — *(bonus idea; thinner business value)*

Property managers juggle guest messages in five languages plus Italian short-let rules (tourist tax, the national identification code). This agent answers from the property knowledge base, reminds guests and hosts about compliance steps, escalates urgent cases, and gives the host a dashboard.

- **For:** short-term rental managers.
- **Demo:** two guest conversations in two languages, one compliance reminder, one escalation.
- **Building blocks used:** knowledge library + workflow + chat widget + AI Tool.
- **Measured number:** response time, compliance steps completed on time.
- **Why it wins:** narrow but concrete; pick it only if the other four don't fit your team's domain knowledge.

### Make the workspace verifiable — the Evolus team inspects it

- [ ] Your **own vLLM endpoint on AMD Developer Cloud** connected to the event workspace (resolve open question #6 with the Evolus team first).
- [ ] **At least two building blocks visibly used — use four or more** (workflow, extractor, AI Tool, knowledge library, MCP connector, sub-agent, chat widget).
- [ ] All actions driven **through the Evolus APIs**, so the calls appear in the workspace usage statistics.
- [ ] Containerized app, public repo, README that runs; **every key in environment variables**.

> **Shortlist:** GaraBot is the most original with the clearest value; the 8D Quality Agent stacks nicely with Track 1. **Fast lane:** GaraBot with three tender PDFs and one company profile — extraction, bid/no-bid, checklist, approval email. Container and README from hour one.

---

## Stacking prizes with any idea

- **Google's $5,000:** run **Gemma** on your AMD endpoint inside the product. It drops into almost every idea above and costs you little extra to wire up.
- **Evolus (€1,011.50 + credits + showcase):** requires the full workspace checklist — own vLLM endpoint, four-plus building blocks, API-driven actions.
- **Vibe Generation special prize (AirPods 5):** quantified value (€ per unit, savings, margin), shipped execution, and taste — every shortlist above is aimed at this.
- **Imment incubation (€1,599 × 3):** pitch the idea as a startup — named user, market, pricing, first customer — not as a demo.
- **The universal checklist:** one dataset, one user, one number; a thin vertical slice (input → model → decision → human gate → output); the AMD workload visible in the video; the number explained inside the product, not only on a slide.

> Quick-scan version with build-fast notes: [08-ideas-by-track.md](08-ideas-by-track.md).
