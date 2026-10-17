# 10 — The Hostile Panel: Every Idea, Killed and Rebuilt

> Stress test companion to [08-ideas-by-track.md](08-ideas-by-track.md) and [09-idea-catalog.md](09-idea-catalog.md).
> This document appoints a panel of judges whose only job is to make sure your idea **does not win** — then rebuilds every idea so their favorite attack stops working.

## How to read this

- It's Sunday morning. Twenty projects. Six minutes each. One demo laptop. No mercy.
- This panel does **not** want reasons to say yes. It wants the fastest reason to say no.
- For every idea: the **kill shot** (the sentence that eliminates it), **the charges**, a **verdict**, then **V2** — the same idea with its structure changed, not its adjectives.
- Scores are out of 10 and intentionally brutal. `v1` is the idea as written in docs 08/09. `v2` is the rebuilt version.

## The panel (may they never judge you)

| Judge | Their lens | Their reflex |
|-------|-----------|--------------|
| **"Seen It" Sofia** | Originality | "Which tutorial is this from? I've judged 40 hackathons." |
| **"Show Me" Marco** | Application of Technology | "If the GPU part could be a CPU part, it doesn't exist. Curl the endpoint or it didn't happen." |
| **"Who Pays" Giulia** | Business Value | "Name the person who signs the invoice and the budget line it comes from." |
| **Professor Rossi** | Presentation + responsibility | "What happens when it's wrong, and who explains that to the person harmed?" |
| **The Inspector** | Rules & verification (Evolus) | "I read the workspace usage stats. Decorative building blocks are fraud." |

**The panel's manifesto:** we don't read past slide 2. We compare you to the five other teams with the same idea. We trust only what re-runs in front of us. If a number can't be recomputed, we assume it was invented. If a demo depends on one famous public dataset, we grade you against the forty teams who used it before you. Benefit of the doubt is not on the menu.

## The universal kill list — how any idea dies

1. **Decorative AMD** — the GPU does something a laptop would do.
2. **The mock gate** — the "human review" is a button labeled *Approved*.
3. **Numbers from imagination** — € saved, hours avoided, computed from data you invented.
4. **Tutorial cosplay** — the famous dataset *is* the story (MVTec, AI4I, UCI Retail).
5. **Sample-use-case clone** — Evolus sample #1 with nouns swapped.
6. **The broke buyer** — museums, hobbyists, or "exposure" as a revenue model.
7. **Prompt-only tech** — remove the LLM and nothing remains.
8. **The feature pile** — six half-features, one working path.
9. **The liability blind spot** — health claims, kids, surveillance, voice cloning, no answer for "when it's wrong."
10. **The one-run wonder** — the demo works exactly once, on the golden path.

Every V2 below is engineered against at least the four or five of these that its v1 triggered.

---

## Track 1 — Intelligent Industry

> Track-specific reflex: "factories have bought dashboards for 30 years. Why would they buy yours?"

### 1.1 Sentinel — v1

**Kill shot:** *"Anomaly detection on NASA bearings — the demo of every industrial hackathon since 2018. I can predict your slide."*

**Charges:**
- Predictive maintenance is a mature commercial category (Augury and friends). Your addition is asking an LLM to word the alert.
- The "24–48 h lead time" is hindsight: you replay data where you already know when the failure happened. No prospective test, no honest lead time.
- You list "how the threshold was tuned" as your credibility moment — that's an admission, not an answer. What's the cost of a false alarm vs a miss, in euros?
- The work-order card is a button. No CMMS, no schedule, no consequence — a prop.
- Marco: an autoencoder on a few MB of vibration data trains on a laptop. Where is AMD load-bearing, and where is the benchmark?

**Verdict:** 🔴 KILL — hostile score **3/10**. "A 2018 demo with a 2024 LLM stapled to the alert box."

### Sentinel V2 — the € of waiting

The product stops being an alarm and becomes a **decision engine**: not "bearing degrading," but **"replace it during Friday's planned stop — waiting past Tuesday costs €X/day in expected failure."**

- **Cost model at the core.** P(failure in next N hours) × (unplanned-stop €/h, parts lead time, night/weekend multiplier, expected damage) vs planned-replacement cost. The output is a **scheduled window with a price tag**, and the threshold is chosen by minimizing expected cost, shown as a cost curve over thresholds — the "how this number was computed" panel, in one chart.
- **Calibrated uncertainty, not binary alarms.** A degradation curve with bands that narrow as evidence accumulates; the calibration plot (predicted vs actual lead time on held-out run-to-failure experiments) kills the "hindsight" attack — you prospectively scored held-out failures.
- **Generalization table.** Validate across ≥3 public run-to-failure datasets (IMS, C-MAPSS FD001–004, AI4I). One table, and "tutorial cosplay" dies.
- **Make the LLM falsifiable.** Every alert cites manual pages (RAG), plus a judge-testable toggle: same alert explained *without* retrieval (generic) vs *with* (grounded). Then the loop closes: technician resolves → 60-second debrief → embedded → next similar alert recalls "last time, this fix worked" — the plant's memory, a second real GPU workload.
- **AMD on the scoreboard.** Sensor-window scoring throughput on ROCm (windows/sec, 90 days scored in seconds, shown live) + tokens/sec on vLLM. Numbers a hostile judge can re-run.
- **Adapt the metric:** expected-cost reduction per asset per year, plus the *cost of the chosen threshold* — you now own the attack instead of dodging it.

**Feasibility guard:** two assets, one dataset table, one cost model. Skip CMMS integration; ship the work-order + a "defer simulator" (slider: defer N days → expected cost moves).
**Residual attack to rehearse:** C-MAPSS is simulated data — answer: "we demonstrate method transfer; field calibration is the pilot."

### 1.2 QCvision — v1

**Kill shot:** *"MVTec AD plus PatchCore — you're running someone else's repository and asking the LLM to narrate the README."*

**Charges:**
- The "operator retraining loop" is a claim you cannot show working in a 36-hour build; a judge will ask to see it and you'll show a button.
- The shift report's insight ("X up 3× after the batch change") needs batch/line data you do not have — the LLM will invent the causality or say nothing.
- Defect escape rate and inspection time: your dataset has no production context. The numbers will be invented.
- Marco: inference on 15 images doesn't prove AMD matters.

**Verdict:** 🔴 KILL — **3/10**. "A repo with a heatmap and a summary paragraph."

### QCvision V2 — five-click onboarding

The painful, real, *unautomatable-today* moment on a line is not known defects — it's a **new** defect class with no labels and no time to retrain. That becomes the product.

- **The demo arc, before/after:** a defect class held out of training appears → the system **misses it** (show the miss honestly) → the operator boxes 5 examples on screen → the memory bank updates (GPU-visible, embeddings/sec on the panel) → the line now catches it. "Days of engineering → five clicks."
- **The report becomes traceability:** every flagged defect is stamped with time, line, and batch tag **at capture time**. The shift report answers "which batch, which shift" because the data was recorded, not inferred. No invented causality; the LLM only narrates facts that were captured.
- **The metric changes to something you can measure in the demo:** minutes to onboard a new defect class, and escaped defects within the demo window. Both exist inside the screen; no production data required.
- **AMD is load-bearing and visible:** the few-shot adaptation runs against a GPU memory bank; the panel shows embeddings/sec and bank size. The "running a repo" attack dies because the 5-click adaptation is *your* mechanic.

**Feasibility guard:** one defect family staged before/after; skip retraining theater — coreset/memory-bank update only.
**Residual attack to rehearse:** "five examples is still small" — answer: threshold and confidence are shown, the operator decides the operating point; it's assistive, not autonomous.

### 1.3 Guardian — v1

**Kill shot:** *"You built worker surveillance and called it safety. The face blurring is a promise nobody in this room can verify."*

**Charges:**
- CCTV + AI on workers is a political object. A judge from the labor side kills it in one question; "privacy story" as a slide makes it worse, not better.
- Helmet detection is the most cloned safety demo there is; YOLO + a PPE dataset, seen it.
- Person-down detection is a medical emergency claim on a system that will miss cases. Ross: "who explains a missed collapse?"
- Three products in one (PPE, intrusion, person-down) = feature pile.
- "Runs on existing cameras" cannot be demonstrated from a laptop; deployment story is asserted, not shown.

**Verdict:** 🔴 KILL — **2/10**. "Technology that should be illegal, demoed as a feature."

### Guardian V2 — safety engineering, not surveillance

The fix is structural: **the product cannot identify people, by design, and the data flow proves it.**

- **Product constitution on one screen:** only counts and zone states leave the camera; a data-flow diagram (frame in → count out) is a *demo artifact*, not a promise. No identity, no gait, no work-rate analytics — "ever" is a policy page a works council can read.
- **Compounding-risk scoring instead of event spam:** alerts fire only when conditions stack (no helmet × forklift zone × shift change), each alert showing its three conditions. Ten times fewer alerts; alert-fatigue attack dies; the output is a **near-miss density heatmap by zone** that drives physical fixes (move the barrier), not people-punishment.
- **Person-down becomes the incident-response loop:** detection → safety-officer escalation → response timer → outcome logged. The metric is *time to response*, not diagnosis. Nobody makes medical claims.
- **Deployment honesty:** recorded public footage, labeled as such, with the retrofit architecture (on-prem box, counts-only to cloud) drawn once. Pretending it's live is how v1 died.
- **Metric:** near-miss reports captured (from ~0) and median response time — both computable inside the demo.

**Feasibility guard:** PPE + zone only; person-down as scenario 2 on recorded footage.
**Residual attack to rehearse:** "still surveillance" — answer with the constitution screen and the works-council policy, and mean it.

### 1.4 WattWatch — v1

**Kill shot:** *"You will show me euros saved, computed from numbers you generated. That's fan fiction with a forecast."*

**Charges:**
- Simulated meter data means the € number is fiction; Giulia asks who billed whom.
- "Waste detection" on per-machine data mostly detects weekends and holidays. Production-normalized baselines are the hard part — and you show none.
- NILM (attribution from a single meter) is a research problem; what SMEs actually have is exactly the case where it doesn't work.
- Plant managers don't buy dashboards; energy audits are bought from consultants — your buyer is wrong.
- An LLM "explaining" a number it didn't compute is the exact anti-pattern the commerce track bans, one track over.

**Verdict:** 🔴 KILL — **3/10**. "A euro figure with no auditor."

### WattWatch V2 — the savings verification bench

The product stops claiming savings and starts **proving** them: an **M&V (Measurement & Verification) copilot** built the way energy auditors actually work (IPMVP-style baseline regression).

- **Every claim survives cross-examination.** Baseline model (working hours + production + weather) → intervention (idle-off policy, VFD, schedule) → savings **with a confidence interval**, and a "show the math" panel: regression, residuals, assumptions, one slider to break it. The hostile judge's recomputation *is* the demo.
- **Honesty as design:** real public energy-consumption series for the baseline mechanics; the counterfactual is synthesized — **labeled on screen, up front** — with the promise: "this is the method; here is the checklist to run it on your plant's data." A labeled assumption is not a lie; hidden simulation is.
- **Buyer switch:** energy consultants and ESCOs — they sell audits; this cuts audit time and makes their savings claims defensible (their liability, their budget). SMEs meet the product through the consultant.
- **LLM's job:** the audit report and the ESCO proposal — the actual deliverables of the industry — drafted from computed numbers with source citations.
- **AMD:** the forecast model benchmarked on ROCm + LLM on vLLM; state which part is CPU and why; benchmark in the video.

**Feasibility guard:** one site, one intervention, one CI, one report. NILM is banned from the scoping doc.
**Residual attack to rehearse:** "your baseline could be confounded" — answer: that's what the CI and the assumption panel are for; show it widening when you feed it bad data.

### 1.5 Mechanic's Copilot — v1

**Kill shot:** *"'Chat with the manual' is a genre. This is the fourth one I've seen before lunch."*

**Charges:**
- RAG over PDFs is a tutorial; multilingual is one prompt line.
- "Escalate when confidence is low" — LLM confidence is vibes; you will script the low-confidence case and it will show.
- Sofia: what will you do that the team next door cannot copy by Sunday morning?
- Giulia: factories don't buy chatbots. The knowledge that costs money lives in a senior engineer's head, not in the PDFs — and your RAG structurally cannot reach it.
- Marco: an embedding call is not a workload.

**Verdict:** 🔴 KILL — **2/10**. "A PDF chatbot wearing a hard hat."

### Mechanic's Copilot V2 — the factory's memory

The core loop flips from **retrieval** to **capture**: the product grows the knowledge that documents don't contain.

- **The loop:** technician fixes something → 60-second voice debrief at the machine → structured procedure linked to the asset, parts, and torque values → embedded into the plant's own procedure base. The demo arcs across one day: *morning* — empty memory, a technician resolves a job with generic manual help; *evening* — the next question is answered from **the plant's own captured procedure**, with the actual part number and photo.
- **Escalation becomes real:** route up when there is **no procedure and no citation** — a retrieval-evidence gap, not a confidence score. Demonstrable live: delete the captured procedure → the escalation fires. Add it back → the answer returns.
- **Multilingual becomes proof of capture:** a Romanian technician's question answered from an Italian-captured procedure — translation layered on *owned* knowledge, not on vendor PDFs.
- **The WTP story is an aging workforce:** the senior engineer retires; this converts 30 years of head into a plant asset. Metrics: time-to-productive for new hires; share of questions answerable without the senior engineer.
- **AMD load-bearing:** Whisper-style ASR + LLM + embeddings, benchmarked; the debrief-in, procedure-out loop is genuinely GPU work.

**Feasibility guard:** one asset class, three captured procedures staged; whole demo ≈ six minutes.
**Residual attack to rehearse:** "capture quality" — answer: the structured procedure is reviewed by the technician before saving; garbage in is visible, not silent.

> **Track 1 shortlist after the panel:** **Sentinel V2** (owns the cost decision), **QCvision V2** (the five-click moment), **Mechanic's Copilot V2** (owns undocumented knowledge). Guardian V2 is a good pitch with a hard political tail; pick it only with conviction.

---

## Track 2 — Health & Wellbeing

> Track-specific reflex: "one wrong sentence about a medication and you're on the news. Show me you know that."

### 2.1 Dimissioni Chiare — v1

**Kill shot:** *"You are generating patient-facing medical instructions, you can't prove patients understand them, and your 'human review' is doing the work your metric pretends you saved."*

**Charges:**
- Producing patient-facing medical information is regulated territory (MDR-style questions). "A nurse approves" does not dissolve accountability — Rossi wants the sentence a hospital's legal office would sign, and v1 has none.
- Comprehension claim is unprovable: a reading-level proxy is not understanding, and you graded yourself with letters you wrote yourself.
- "40 → 15 nurse minutes" is asserted, not shown — and you may have *added* review work to the nurse's day.
- Confidence badges from an LLM's self-reported confidence are fake-calibrated; you will hardcode the threshold and Marco will ask how.
- "Google Translate plus hospital templates exist" — the delta is never demonstrated.

**Verdict:** 🔴 KILL — **4/10**. "A sweet idea graded by its own author."

### Dimissioni Chiare V2 — understanding is the product

- **Close the loop with teach-back.** After generation, the patient answers three questions in their language ("when do you take the blood thinner?"). Failed items → re-explained simpler → still failing → flagged to the nurse. Teach-back is a real clinical technique, and **the pass rate is the metric** — the patient's own answers, not your proxy. The demo persona can actually be played live.
- **Traceability weapon:** every output sentence links to the highlighted source span in the original letter (click → highlight). The model *cannot* introduce clinical content because there is nowhere to cite it from. Dosage invention → fixed refusal template — show the red-team attempt live.
- **Nurse review redesigned as edit-by-exception:** auto-accepted sections collapsed; only flagged spans open; count "nurse touches per letter" with a stopwatch in the video. The review step *is* the product's core screen, not a tax on it.
- **The legal sentence:** "rephrases and translates existing letter content only; every sentence traceable; a nurse approves before release; no new clinical content." One sentence a hospital legal office can sign — say it on the slide.
- **Demo:** two letters, two languages, one refusal, one teach-back round.

**Feasibility guard:** no voice dubbing, no AVS; synthetic letters with public-system-style formats.
**Residual attack to rehearse:** "MDR?" — answer with the scope sentence and the pilot framing (a hospital's own supervised pilot).

### 2.2 PreVisit — v1

**Kill shot:** *"You say 'never diagnoses' — but sorting by urgency is triage. Pick one: clinical judgment or admin form."*

**Charges:**
- If it flags urgency, it is making a clinical call; symptom checkers have a decade of over/under-triage literature and several were pulled. Rossi leads with this.
- Voice intake on anxious elderly non-native speakers with background noise — your studio-clean demo will read as staged.
- Schema validation is engineering vocabulary; judges don't score pydantic.
- The genuinely hard part — chasing missing information until the file is complete — appears nowhere in v1.
- Nobody in the demo is accountable when the red flag is wrong.

**Verdict:** 🔴 KILL — **3/10**. "A triage tool that says it isn't one."

### PreVisit V2 — the admin fixer, not the triage nurse

- **Boundary in one sentence: extraction, not inference.** Urgency routing is a **deterministic, versioned clinic-protocol rule set** (e.g., "chest pain mentioned → route"), visible on screen. The model only proposes the patient's quoted words; the rule fires; the nurse sees the quote. The word *triage* never appears in the product.
- **The real core is the information chase:** auto-messages for health card numbers, medication photos, and referrals, in the patient's language, until the file is complete. Metric: **% complete files before the visit** vs the phone-tag baseline — a workflow number the clinic already feels daily.
- **De-staging the voice demo:** include one deliberately messy recording (accent, noise) next to a clean one — the mess proves it's real, and voice is positioned as a catch, not the story.
- **Contradiction surface:** the patient contradicts themselves on medication; the product shows both quotes side by side for the nurse and resolves nothing. Responsibility stays visible.
- **Demo:** one persona, text + one messy voice message, the rules file on screen.

**Feasibility guard:** one flow, one rule set, one chase loop.
**Residual attack to rehearse:** "who is responsible for a missed red flag?" — answer: the rule set is the clinic's, versioned, with an audit log; the product executed it and recorded the quote.

### 2.3 ChartKeeper — v1

**Kill shot:** *"OCR plus summarize, and a diff view. The dentist's waiting room software is more sophisticated."*

**Charges:**
- "What changed since last visit" is entity-diff fragility — feed it two contradictory labs and it logos dissolve.
- GPs don't buy software; their systems are locked by regional suppliers; your demo doctor is fictional and Giulia knows it.
- Real charts are impossible (privacy), synthetic charts prove nothing, and every-claim-cites-source is table stakes by now.
- Marco: the LLM and embeddings are decorative; the interesting part (OCR of bad scans) is a library call.

**Verdict:** 🔴 KILL — **3/10**. "A filing cabinet with a summary button."

### ChartKeeper V2 — close the referral loop

Re-anchor on the loop nobody owns and every GP loses sleep over: **sent → seen? → report back?** — the referral black hole.

- **The product is loop closure.** Two referrals tracked in the demo: one overdue (escalated with a chase action), one closed — with the specialist's report merged into the timeline. The timeline and "changed since last visit" become supporting views, not the pitch.
- **The catch moment:** the new specialist report **contradicts the current medication list** — both sources side by side, with a drafted correction note for the GP. That's the wow; extraction and traceability exist to serve it.
- **Referral packets:** one click compiles the referral with prior labs and attachments → fewer bounce-backs. Rejected referrals are wasted appointments — a KPI GPs feel in their own schedule.
- **Metrics:** % referrals closed within expected window; re-referral/bounce-back rate; minutes per packet. The money story for a regional payer: duplicate tests and visits prevented — each with a source link.
- **Demo:** one patient, one overdue referral, one contradiction catch.

**Feasibility guard:** the diff view is a bonus; the loop and the catch are the product.
**Residual attack to rehearse:** "synthetic data" — answer: formats modeled on public health-system documents; the demo is the workflow, and the workflow is what hospitals recognize.

### 2.4 MedRec — v1

**Kill shot:** *"String and dose comparison — an Excel macro with a dictionary does 80%. The intelligence is a lookup table."*

**Charges:**
- The hard question — *which list is right* — remains with the pharmacist, so the "AI" added a queue, not judgment.
- The three-way data triangle (hospital record + pharmacy record + patient knowledge) does not exist as shareable data in Italy; Rossi: "you fabricated the data architecture."
- A handful of list comparisons is decorative GPU work.
- Catch rates are quoted from literature, not measured in anything you built.

**Verdict:** 🔴 KILL — **3/10**. "A pharmacist's to-do list generated by a regex."

### MedRec V2 — photograph your medicines

Put the hardest real source in the loop: **the patient's actual boxes.**

- **Multimodal reality capture:** the patient photographs their pillboxes/boxes (or shows them on a video visit). A vision model reads brand names and doses; embeddings normalize to **active ingredient** — solving the genuinely Italian problem where the same active ingredient travels under five brand names. Demo: one photo → "same active ingredient, different brand — matches the letter" and "these two boxes double the daily dose if combined." That's the money moment, and it is real multimodal GPU work.
- **Reconciliation matrix:** letter vs pharmacy record (if available) vs photographed reality; severity-coloured discrepancies; pharmacist queue stays as the resolver. Nothing auto-changes.
- **Interop honesty as architecture:** pharmacy record is optional; without it the product degrades gracefully to photo + letter. The "data triangle doesn't exist" attack dies in the design, not in the pitch.
- **Metrics:** discrepancies caught per 100 reviews; pharmacist minutes per review; brand-equivalence catches (the demo's own number).

**Feasibility guard:** 5 boxes photographed; one brand-equivalence catch, one duplicate-therapy catch.
**Residual attack to rehearse:** "vision misreads boxes" — answer: confidence per field, unclear fields are asked for again (second photo), pharmacist confirms.

### 2.5 CarePath — v1

**Kill shot:** *"A chatbot with reminders for an audience that demonstrably doesn't pay."*

**Charges:**
- Caregiver navigation has burned through startups; WhatsApp already reminds people.
- "Missed appointments" responds to transport and cost, not reminders; you address neither.
- Public-health FAQ content is a commodity; nobody pays for it.
- "Caregiver hours saved" is survey fiction — no measurable core.

**Verdict:** 🔴 KILL — **2/10**. "A caring idea with no invoice."

### CarePath V2 — the exam-prep conductor (the hospital pays)

Pick the concrete, costly, unautomated job: **exam preparation** — fasting, stopping medications, an escort being required, documents, transport. Failures mean cancelled or repeated exams, and the hospital eats the wasted slot.

- **Closed accountability loop:** a prep plan per exam type, built from the clinic's own prep documents; the caregiver confirms steps with timestamps; unconfirmed steps escalate to the clinic 48 hours before the appointment — so someone calls *before* the patient shows up unprepared.
- **The buyer flips:** hospitals/clinics pay to avoid wasted slots; the caregiver uses it free. Metric: **wasted slots avoided per 100 exams** — a number a department head already tracks.
- **The demo case writes itself:** colonoscopy prep — notorious for failures. One caregiver, two languages, one escalated case, one saved slot.
- **Technical core:** document-grounded prep extraction per clinic + a per-appointment state machine + message orchestration; the LLM explains *only* from clinic documents (traceable), refuses otherwise.

**Feasibility guard:** two exam types, one clinic, one escalation.
**Residual attack to rehearse:** "reminders don't work" — answer: this isn't a reminder; it's a confirmed checklist with escalation to a human — the failure mode is caught by a person, not by a notification.

> **Track 2 shortlist after the panel:** **Dimissioni Chiare V2** (teach-back closes the loop), **MedRec V2** (the pillbox-photo moment), **CarePath V2** (the payer flip). PreVisit V2 survives as an admin-play; ChartKeeper V2 is the quiet workhorse.

---

## Track 3 — Reinvent Commerce

> Track-specific reflex: "a language model narrated a number. Show me who computed the number and how."

### 3.1 Saldi — v1

**Kill shot:** *"Your demo dataset doesn't contain your pitch. You promised sizes and weather — UCI Online Retail has neither. You'll show forecasts of the wrong universe."*

**Charges:**
- The features you claim (size, weather, promo lift) don't exist in the demo data. The demo contradicts the pitch in the first minute.
- Markdown optimization is a mature category (Revionics et al.); a retail judge has seen vendor demos with actual dollars behind them.
- Single-store MAPE vs naive baseline over one backtest is noisy — statistically indefensible, and Sofia will say "p-hacked."
- By the doc's own admission, GPU is decorative.

**Verdict:** 🔴 KILL — **4/10**. "A forecast of a universe that isn't in the CSV."

### Saldi V2 — rules with receipts

- **Change what the backtest judges: do not sell point-forecasts — sell a *policy*.** Run the shop's incumbent rule ("20% off at week 4") against the proposed adaptive rule over full history; show **profit curves with confidence intervals**. The claim becomes: "this rule made more money on your own data" — far harder to poke than MAPE bingo, and the CI shows you know what noise is.
- **Stop promising what the data lacks.** Reframe scope to what exists (daily units, prices, promos where present) and *say the cuts on a slide*: "sizes/weather: not in this data, disabled; the schema supports them when the retailer has them." Honesty converts the attack into a maturity point.
- **The artifact is a one-page season plan:** initial price, first markdown trigger ("if sell-through < X% at week 3, cut Y%"), expected profit with range — a plan a shop owner can execute with a pen. Plus campaign copy from the LLM.
- **AMD, honestly:** embeddings for cross-season similar-product features + LLM for plan/copy; benchmarked; state what runs on CPU.
- **The counterfactual table is the UI:** every suggestion expands to "cut now vs wait — expected profit for each," computed, not narrated.

**Feasibility guard:** one dataset, one rule comparison, one plan page, one CI chart.
**Residual attack to rehearse:** "one store is not evidence" — answer: "we compare rules on the store's own history; the pilot is the next store, and the method transfers."

### 3.2 Never Run — v1

**Kill shot:** *"Reorder points are a default feature of every ERP. You built a worse module of software the buyer already owns."*

**Charges:**
- Any judge's uncle with a management system has seen "reorder suggestions" since 2005.
- No public dataset has expiry dates; your "spoilage €" will be invented and Giulia will find out.
- "Top 10 actions" — what does the existing ERP report do that this doesn't?
- The buyer is a small retailer with three other tools already failing at the same job.

**Verdict:** 🔴 KILL — **3/10**. "An ERP feature with a startup's confidence."

### Never Run V2 — inventory without an ERP

Target the shop that has *nothing*: no inventory system, just a POS and a phone. The wedge is **zero-setup inventory**.

- **Two demo moments:**
  1. **Shelf photo → on-hand estimate.** Vision counts facings and estimates stock, filling the "inventory" the shop never had. Minutes to first useful output, no configuration.
  2. **Delivery arrives → photo the crate → received vs ordered.** A discrepancy note to the supplier *before signing*. Nobody automates this for micro-retail.
- **Forecasting stays, honestly:** real daily SKU-level data (M5-style food categories) with service-level targets; the number shown is **days of cover** — which needs no expiry data at all. If shelf-life scenarios appear, they are labeled as category assumptions *on screen*.
- **Every digest item gets provenance:** "why: Saturday demand usually +40%; last Saturday you ran out by 14:00 (≈€X lost)." The why-panel is the product.
- **AMD:** vision counting + embeddings + LLM digest, visible and benchmarked.

**Feasibility guard:** one store, one shelf photo, one delivery check, one digest.
**Residual attack to rehearse:** "photo counting is inaccurate" — answer: estimates, not diagnoses; the day-list ships only items that survive low confidence; the shop corrects in one tap and the count updates.

### 3.3 Voice of Customer — v1

**Kill shot:** *"Embeddings plus k-means: a 2020 tutorial. You will find one hot cluster and call it a defect crisis."*

**Charges:**
- Aspect-level sentiment is a solved, dull pipeline; the "hidden defect" reveal is seeded and unverifiable.
- Real review data is mostly noise; one demo cluster proves nothing.
- Nobody in a ten-person shop owns "product feedback" — the budget belongs to no one.
- Marco: the culprit is the embedding call, and he's yawning.

**Verdict:** 🔴 KILL — **3/10**. "A pretty pivot table with opinions."

### VoC V2 — Returns Radar: the money comes back

Re-anchor the unit of analysis: **the return, not the review.**

- **Statistical control per SKU:** alert when a SKU's return rate breaks its own historical band (a control chart — a legitimate method with a visible threshold judges can interrogate). Cause classification into the classic buckets (description error / defect / shipping / expectation gap), informed by review aspects.
- **Every alert ends in money or a fix:** draft the **supplier claim** (defect-rate breach — €X at stake) or rewrite the listing (expectation error). "Claiming money back from suppliers" is the thing nobody demos.
- **The demo moment:** one SKU where reviews look fine but the returns control chart breaks — "reviews would have missed it; the money wouldn't."
- **Metrics:** € recovered via supplier claims; duplicated returns prevented — shop-accountant numbers, not vanity metrics.
- **AMD:** batched embedding throughput for clustering + classifier training + claim drafting LLM — shown, benchmarked.

**Feasibility guard:** one hot SKU, one claim, one listing fix.
**Residual attack to rehearse:** "control charts on sparse returns are noisy" — answer: minimum-volume gates plus the band; the alert explains its own significance.

### 3.4 WISMO Copilot — v1

**Kill shot:** *"A support chatbot. The brief lists 'support desk' as its own sample use case. Your originality just left the room."*

**Charges:**
- Maximum crowding; the order-data integration will be a mock; every team says "ours has real context."
- Deflection rate is the vanity metric of demos — and wrong deflection is churn: "the customers we handled worse, faster."
- Multilingual: one prompt line.
- Giulia: e-commerce SMBs churn through tools like this monthly.

**Verdict:** 🔴 KILL — **2/10**. "The default idea, executed politely."

### WISMO V2 — the exception desk

Move from answering to **pre-empting**: the money is in the 15–20% of orders that go wrong.

- **Product:** watches shipment events + order state; detects exceptions (customs holds, failed delivery, address errors, damage, returns) **before the customer writes**; runs plays: pre-emptive message in the customer's language, carrier claim drafted, replacement proposed per policy, refund computed. The demo: one customs-delayed order resolved at 09:00 — customer never contacts anyone; one damaged arrival → carrier claim drafted with an evidence checklist.
- **KPIs a CFO signs off:** exceptions resolved before first customer contact; cost per exception; **carrier claim € recovered**. The word "deflection" never appears.
- **The integration becomes the demo's spine:** feed simulated carrier events live; judges watch a bad event become a handled case in 90 seconds.
- **Originality:** nobody demos carrier-claim automation. It's boring money — exactly the gap between "support bot" and "logistics."
- **AMD:** LLM for messages/policy reasoning + embeddings mining historical exception→resolution plays.

**Feasibility guard:** two exception types, one play each.
**Residual attack to rehearse:** "the carrier integration is fake" — answer: the event feed is simulated (labeled), the *play engine* is the product, and event adapters are swappable shown in the architecture.

### 3.5 Churn Radar — v1

**Kill shot:** *"Churn prediction is the hello world of ML. And your model will save the members who were never going to leave."*

**Charges:**
- Telco churn demos are old enough to vote; gym data quality (turnstile gaps, shared memberships) means your features are aspirational.
- Win-back discounts burn margin on sure-stayers — a fine judge will poke exactly there.
- "Retention %" attribution: prove the offer moved anyone.
- Giulia: gyms are famously cheap buyers.

**Verdict:** 🔴 KILL — **3/10**. "An ML classic paying discounts to the already-loyal."

### Churn Radar V2 — persuadables only

- **Swap the model from prediction to *causal* targeting (uplift):** not "who will churn," but "who churns *unless* intervened and responds *if* we do" — the classic four quadrants (sure-stayers, lost causes, persuadables, sleepers). The demo's centerpiece is the quadrant chart: **"we spend offers on the middle box only."** That's a different ML problem, visibly, and Sofia can't call it hello-world.
- **Offers stop being discounts:** usage micro-behaviors → concrete interventions (schedule fix, buddy, class slot, check-in) — LLM drafts, staff approves. The positioning: *"discounts for persuadables only; nothing for the rest."*
- **Unit economics:** € per persuaded save vs discount cost per save — exactly the Vibe Generation math.
- **Data honesty:** a real public subscription dataset (usage + churn labels, KKBox-style) mapped to the membership narrative; the method shown, assumptions labeled.

**Feasibility guard:** one cohort, one campaign, quadrant chart, three drafted offers.
**Residual attack to rehearse:** "uplift needs experiment data" — answer: retrospective policy evaluation over cohort history; the chart shows uncertainty; the pilot designs the A/B.

> **Bonus one-liners, killed fast:** *Catalogue enrichment* — "transcription with a bow; the buyer already pays an intern" → V2 only as **attribute-level confidence + cross-supplier conflict resolution** (three suppliers describe one product differently → canonical record with per-attribute provenance); that's data governance, not copywriting. *Personal shopper* — "a recommender demo; the wine shop doesn't have the data" → V2: a sommelier that **shows its work** (constraints, trade-offs, "try two, tell me which won" learning loop) sold to wineries running D2C clubs — they have repeat-purchase data.
>
> **Track 3 shortlist after the panel:** **Returns Radar** (money comes back), **WISMO V2 Exception Desk** (boring money, real originality), **Saldi V2** (rules with receipts). Never Run V2 if the team loves computer vision.

---

## Track 4 — A New Kind of Experience

> Track-specific reflex: "where's the *experience*? This is a pipeline."

### 4.1 Museo Vivo — v1

**Kill shot:** *"Smartify exists, with museum deals and real footfall. You have eight artworks and a prompt that changes tone."*

**Charges:**
- Personalized audio guides are a funded category; eight artworks is a demo, not a moat; Sofia will name a competitor you haven't heard of — it's in her notes.
- The experience is TTS with different system prompts. Where's the innovation in the *interaction*?
- The provenance claim is prompt engineering; one jailbreak and the trust story dies.
- Museums are broke: "cost per visit" is a number without a budget line.

**Verdict:** 🔴 KILL — **3/10**. "ChatGPT in a cardigan, priced for institutions that collect entry fees, not subscriptions."

### Museo Vivo V2 — ask the room

- **New core interaction:** point your phone at anything in the room → the guide talks about *what you are actually looking at* (a vision model reads the photo), grounded strictly in the curator's fact base. If it isn't in the base, it **says so** and files the question for the curator — the honest "not in my notes" is a feature, kills the hallucination attack, and creates a memorable moment in the demo.
- **Curator console:** unanswered questions as a content-gap dashboard (museums pay for engagement analytics), and an approve-to-add flow that grows the fact base **during the session** — the human+AI workflow shown in both directions.
- **Payer switch — replace a cost line, don't add one:** museums rent hardware audio guides per visit for multiple euros; position at cents per visit, plus accessibility (audio description for blind visitors rides a separately funded budget). "We are a smaller line in the old budget, not a new line."
- **Demo:** one room; child + historian + blind-visitor persona; one photo question; one "not in my notes" moment; one curator approval.
- **AMD:** vision + LLM + TTS on GPU; RAG over curated texts with the no-invention guardrail, benchmarked.

**Feasibility guard:** one artwork set (photos), two personas, three interactions; no live museum integration.
**Residual attack to rehearse:** "museums still won't buy" — answer: the hardware-replacement math plus the analytics line; name the pilot partner if you have one, even a small museum.

### 4.2 Race Story — v1

**Kill shot:** *"After two videos the wow is gone. And the AI voiceover reads like a GPS explaining a memoir."*

**Charges:**
- Race photographers already sell recap packages; "AI commentary" is a novelty, not a business.
- Photo rights: you cannot use real race photos — the demo will be stock or staged, and "cinematic" is unearned.
- The film is a template montage with voiceover; the editorial taste that makes recaps work is outsourced to a music bed.
- €0.50/runner is asserted; render + TTS + LLM says optimistic.

**Verdict:** 🔴 KILL — **3/10**. "A slideshow with splits data reading a horoscope."

### Race Story V2 — the race's own media engine

- **Two revenue lines:** the **organizer** pays for a media engine — social cuts of story moments *detected from the splits* (negative splits, comebacks, milestones, sprint finishes) published within hours of the race; **runners** buy personal films as the upsell. The organizer line is the business; the runner film is the consumer demo.
- **The moments are detected, not prompted:** event detection over split series is the actual tech; the LLM only narrates a detected moment with injected numbers ("at km 32 she passed 47 runners"). Grounded narration — nothing to hallucinate, no horoscope.
- **Kill the cringe:** default artifact is a typography-led **shareable story card** (screenshot-and-share is the KPI); voice is optional and can be the race's own announcer (with consent) instead of AI.
- **Rights answer:** production ingests the *official photographer's* archive under the organizer's license — the organizer owns those assets, which is precisely why the organizer pays. The demo uses public race splits + stand-in imagery, labeled.
- **Metrics:** organizer: cost per story moment, share rate; runner: cost per film, attach rate.

**Feasibility guard:** two runner films + one organizer cut + one detected moment.
**Residual attack to rehearse:** "event detection on splits is trivial" — answer: the detection catalogue is the product; show three moment types detected from one real race's split data.

### 4.3 Storie — v1

**Kill shot:** *"One weird output from a kids' product and you're a screenshot. You demoed two nice stories and called it safety."*

**Charges:**
- Kids + LLM is politically radioactive; the failure mode is the story, not the success.
- Consistency across nights = JSON memory; not hard, not a moat.
- Diffusion illustrations look like generic AI art, and children's publishing is an art-direction business.
- Parents pay for taste and ritual; competing with Tonies, libraries, and free YouTube for a generation utility — CAC hell.
- Marco: ASR + LLM + diffusion — a pipeline every team runs.

**Verdict:** 🔴 KILL — **2/10**. "A content generator in the most trust-sensitive market there is."

### Storie V2 — the keepsake ritual

- **From generation to ritual + artifact:** the nightly five minutes (one question to the child, one story, one conversation starter for the parent) and the **quarterly printed keepsake book** of that quarter's stories. The AI is the means; the ritual and the object are what parents pay for. A print product also has margin and marketing built in (grandparents receive copies).
- **Safety as a visible constitution:** the parent pre-approves tonight's *ingredients* (30 seconds, not content); a "no peril, no villains, no ads" policy engine; and a per-child **audit log** — the parent can read every story ever generated. Show the rejection demo: child asks for a scary monster → policy rewrites to "a grumpy giant who is not scary" → side-by-side shown.
- **Curated house style:** one art direction per book, parent-selectable palettes, similarity checks against approved pages — "house style," not "AI style."
- **Demo:** two nights, two children, one refusal demo, one printed-book spread mock.

**Feasibility guard:** skip full print pipeline; show the laid-out book PDF as the artifact.
**Residual attack to rehearse:** "still risky for children" — answer: pre-approval + policy engine + audit log; the parent is the editor-in-chief.

### 4.4 AccessAll — v1

**Kill shot:** *"Captions, translation, TTS — the three-tool pipeline. And dubbing real voices is a rights minefield you haven't entered."*

**Charges:**
- Captioning is a mature cheap market with established vendors; you're late to a solved problem.
- Voice dubbing without a consent architecture is a legal time bomb; Sofia's cousin is in a voice actors' union.
- Audio-description quality is unverifiable in a demo; the actually-hard part — timing alignment — is waved through.
- "Cost per minute vs manual" — which manual, what rate? The figure is never shown.

**Verdict:** 🔴 KILL — **3/10**. "A pipeline with a press release attached."

### AccessAll V2 — the audio-description factory

- **Focus on AD** — the least automated, most expensive accessibility piece, with a live regulatory tailwind (European Accessibility Act obligations are in force; broadcasters and platforms need described content at volume).
- **The tech that makes it defensible:** shot-boundary detection + **character/continuity tracking across the film** (the same coat is re-identified after a cut; "she" stays "she") + **duration-aware writing** (description must fit between dialogue — forced alignment to the audio timeline) + **per-client style profiles** (broadcasters have in-house AD rules). The demo: naive VLM description vs the shot-aware, timing-aware script on the same public-domain scene — the before/after *is* the pitch.
- **Align with the AD community:** a professional writer's edit queue with diff view and approval — the humans who might otherwise attack the concept are in the product's loop. Demo the review, don't skip it.
- **Metrics:** cost per finished described minute vs freelance benchmark (state the benchmark), minutes processed per language, and **% of catalogue described** — the number broadcasters report to regulators.
- **Kill dubbing and captioning from the core** — roadmap slides only; the rights minefield and the crowded market both vanish.

**Feasibility guard:** one 90-second public-domain clip, two style profiles, one review edit.
**Residual attack to rehearse:** "how good is the description, really?" — answer: writer review is mandatory in the workflow; quality gate is a person, always.

### 4.5 Studio One — v1

**Kill shot:** *"Adobe GenStudio ships this with brand guardrails and a billion-dollar polish. Your 'consistency score' is a CLIP similarity you tuned until the screenshot looked good."*

**Charges:**
- Brand-guarded generation is a crowded suite feature; the judge has seen it in enterprise decks.
- Consistency score = invented KPI; approval step = checkbox; legal-line enforcement = regex.
- Two variants and two captions — where's the product?
- Giulia: agencies are price-pressured and slow; the wow is low, the budget is vague.

**Verdict:** 🔴 KILL — **2/10**. "A feature, not a company, aimed at a buyer who already has it."

### Studio One V2 — claims with receipts

- **Wedge into regulated marketing:** the bottleneck is not generation — it's **claim substantiation**. Every "clinically proven," "number one," "doctor-approved" needs an approved evidence document behind it; legal review takes weeks; regulators fine.
- **The product:** variants where every claim is either (a) linked to a substantiated entry in the claim library **with its evidence document**, or (b) **blocked with the reason**. Demo: one variant auto-blocked ("number one" without evidence), one corrected with a substantiated alternative, and a legal export — claim → evidence → asset — for audit.
- **Brand memory:** ingest the catalogue; every asset shows a **provenance chain** (style rules applied, past assets referenced, claims cited). For regulated brands, the audit trail *is* the product.
- **Buyer switch:** regulated marketing teams (pharma, food, finance — budgets that exist because fines exist) and the agencies serving them.
- **Metrics:** claims-review cycle days → hours; cost per variant; blocked/auto-fixed claims per campaign.

**Feasibility guard:** one brief, two variants, one block + one fix, one legal export.
**Residual attack to rehearse:** "you're not lawyers" — answer: the library is the client's own substantiation; we enforce their corpus, we don't judge legality.

> **Track 4 shortlist after the panel:** **Museo Vivo V2** (the "ask the room" moment), **AccessAll V2** (regulation-backed demand), **Studio One V2** (boring compliance money). Race Story V2 is the best pure unit-economics play; Storie V2 if the team has genuine art direction.

---

## Evolus Track — Business Agents on AMD

> The Inspector's lens on top of everything: the workspace usage stats are the ground truth, and sample-use-case clones are disqualified in spirit even when they pass in form.

### E.1 GaraBot — v1

**Kill shot:** *"Commercial tender-alert services exist. Your delta is a bid/no-bid judgment computed from twelve PDFs — that's a folder, not a knowledge library."*

**Charges:**
- Bid/no-bid from a handful of past bids is unfalsifiable in demo — show win/loss labels or it's astrology.
- One hallucinated requirement in public procurement is disqualification-grade pain; you demo three PDFs and claim reliability — where's the accuracy number?
- Scanned, stamped, 140-page attachments: the failure case is certain and unaddressed.
- The Inspector: which building blocks are real, and would the usage stats show them doing anything?

**Verdict:** 🔴 KILL — **3/10**. "A folder with a scoring function."

### GaraBot V2 — nothing disqualifies us

- **Reposition around the disqualifier killers:** extract only the hard gates — certifications, minimum turnover, guarantees, formatting/bollo requirements — into a **compliance grid where every cell cites the tender page, highlighted in the PDF**. The agent never asserts an unattributed requirement; the human confirms.
- **Bring the evaluation the panel demanded:** a hand-built **golden checklist** (≈50 items across the three tenders) → show extraction precision/recall in the demo. Reliability becomes a number, not a vibe.
- **Bid/no-bid stays, downgraded and honest:** an explainable weighted rubric against the company profile — with the explicit note "this is a rubric, not a model, because you have twelve past bids." Rubrics are auditable; auditability is the feature. The library still improves with each added bid — show one addition improving the match.
- **Recurring value = the countdown:** the 30/15/7/2-day submission timeline, per-tender document checklist, and PEC-email drafts. Misses are why SMEs get disqualified; the agent runs the clock.
- **The dataset is the most honest in the hackathon:** real public tenders from national portals — messy, public, verifiable by any judge on the spot.
- **Building blocks (5 visible):** extractor + knowledge library + workflow + email MCP + AI tool. Workspace stats will show all of them.

**Feasibility guard:** 3 tenders, 1 company profile, 1 golden checklist.
**Residual attack to rehearse:** "OCR on scans" — answer: flags low-confidence extractions for human review; the grid's cells are clickable to the page image.

### E.2 Supplier Compliance Sentinel — v1

**Kill shot:** *"An Outlook rule with OCR. The 'compliance dossier' is a folder."*

**Charges:**
- DURC and visura have lookup paths; OCR-ing what an API returns is *worse* than the lookup — you would be adding errors to data that already exists.
- Originality floor: Evolus sample #1 (documents → extract → workflow) re-skinned.
- "Zero expired suppliers" — a vanity metric nobody verifies.
- The Inspector: extractor + workflow + email — the sample-use-case trifecta.

**Verdict:** 🔴 KILL — **3/10**. "Compliance plumbing, priced like a platform."

### Supplier Compliance Sentinel V2 — Supply Continuity Sentinel

- **Escalate from paperwork to business risk.** Each supplier scored on: (a) document validity, (b) **exposure** — share of critical components single-sourced, dependency depth, (c) **continuity signals** from public sources (news, filings, labor actions). The output is a risk board; the headline alerts are continuity alerts: *"Supplier X is your sole source of Y; distress signals detected; backup qualification takes ~6 weeks — start now,"* with a drafted qualification request.
- **The boring core stays as the intake channel** (documents in, validity out); the product's face is **stoppage prevention** — a CFO topic, not a clerk's calendar.
- **Answer the API attack in the architecture:** use official lookups where they exist (show one live MCP lookup), OCR only where no API exists — say exactly that on the slide.
- **Metrics:** critical single-source dependencies identified; time-to-backup-qualification; expired suppliers as the hygiene floor.

**Feasibility guard:** 3 suppliers, 1 news source, 1 drafted backup request.
**Residual attack to rehearse:** "news signals are noisy" — answer: signals trigger a *review*, not a verdict; the risk board separates signal from evidence.

### E.3 8D Quality Agent — v1

**Kill shot:** *"An 8D is a Word template. You built mail-merge with extra steps."*

**Charges:**
- Each OEM has its own 8D format and portal; you support one template — "single-format tool."
- Recurrence tracking is a GROUP BY.
- Pairing with Track 1 reads as "one demo pitched twice" — a submission-strategy risk as much as a product risk.
- The reasoning that matters (why did it happen, why was it not detected) is still done by the quality engineer; you moved the typing, not the thinking.

**Verdict:** 🔴 KILL — **3/10**. "A template with a thesaurus."

### 8D Quality Agent V2 — the first 48 hours

- **The 8D is the report; containment is the product.** When a complaint arrives, the clock runs on stopping the bleeding. The agent: extracts part/lot → pulls shipment and QC context → **drafts immediate containment** (quarantine list, customer notification, stock check) → QA approves → then assembles the 8D over the following days with every claim citing its source (inspection record, email, photo).
- **Demo:** complaint at 09:00 → containment drafted by 09:04 → two customer formats (e.g., OEM-style and VDA-style) compiled from the same case — the multi-template compiler kills the single-format attack.
- **Metrics:** hours from complaint to containment (the safety number); 8D cycle days; recurrence secondary.
- **Submission strategy fix:** submit in *one* track; mention the factory's quality loop as integration, not as a second pitch of the same demo.

**Feasibility guard:** one complaint, one containment, two formats.
**Residual attack to rehearse:** "quality engineers still do the thinking" — answer: correct, and deliberately so; the product removes 6 hours of assembly per complaint, not the engineer.

### E.4 Claim Intake — v1

**Kill shot:** *"This is Evolus sample use case number one — invoice intake — with insurance nouns. Originality, dead on arrival."*

**Charges:**
- Email + attachments → extract → chase missing → escalate: a structural clone of the sample.
- Policyholder validation "via API" will be mocked, visibly.
- Insurance claim handling is regulated; the legal judge asks who owns a wrong routing.
- "Complete files at first touch" is a real metric with no baseline in your demo.

**Verdict:** 🔴 KILL — **2/10**. "Sample clone, spotted in three seconds."

### Claim Intake V2 — FNOL Studio: collect it right the first time

- **Move to first notification of loss and make *evidence quality* the product.** The agent interviews the client in their language (chat/voice) → structured loss file → **guided photo capture** ("wide shot of damage → VIN plate → other party's plate → close-up") with per-photo quality checks (blur, darkness, wrong angle → re-request) → coverage-basics rules check → routing with an SLA clock.
- **Why it's a different product:** claims re-open and disputes trace back to day-0 evidence. No intake checklist fixes that; the guided capture does. That's a root-cause fix, and it demos in ninety seconds: first photo batch rejected (blurred VIN) → re-guided → complete file.
- **Regulated activity boundary is visible:** the agent never denies, never prices; it completes and escalates. Human adjuster owns decisions — on the architecture slide.
- **Per-category flows** (auto/home/travel) prove the architecture beyond one template.
- **Metrics:** % first-touch complete-and-settleable files; re-request rate; days-to-settlement as the outcome proxy.

**Feasibility guard:** one flow (auto), one rejection/rescue loop, one escalation.
**Residual attack to rehearse:** "photo quality checks are cosmetic" — answer: the checks are per-field requirements of the claim file; show a file that *fails* settlement-readiness and one that passes.

### E.5 Short-let Compliance Concierge — v1

**Kill shot:** *"A guest-messaging bot with calendar reminders — and you admit in your own doc that the business value is thin. Next."*

**Charges:**
- Airbnb already collects tourist tax in many municipalities; property-management suites run messaging playbooks.
- Hosts don't buy "reminders"; fines are the actual fear, and a reminder doesn't prevent one.
- Rule data per comune (registration, ID filing, tax) is exactly where the demo will be hand-waved.

**Verdict:** 🔴 KILL — **2/10**. "The weakest idea in the bank, and it knows it."

### Short-let Compliance Concierge V2 — the compliance desk for short-let managers

- **Not messaging — back-office compliance at portfolio scale:** a per-comune rule library (registration, CIN, guest-ID obligations, tax); **reconciliation of tourist tax collected by each OTA against what each comune expects** (platforms remit inconsistently — the reconciliation catches the shortfall, with a seeded € example); auto-prepared filings and a quarterly audit pack per apartment; ID-check tracking per booking.
- **Buyer:** the 30-flat property manager — fines per apartment and admin hours are their P&L; priced per property.
- **Demo:** one quarter, three apartments, two comuni — reconciliation catches an under-collection, one filing prepared, one ID-check gap flagged.
- **Blocks:** knowledge library + workflow + extractor (guest docs) + MCP to the accounting system.
- **Still the weakest lane:** if nobody on the team knows this domain, skip it; the consultant-for-consultants pitch is just an honest strength.

> **Evolus shortlist after the panel:** **GaraBot V2** (original + verifiable data + 5 blocks), **FNOL Studio** (root-cause fix, not sample clone), **8D V2** (tin first 48 hours). Supply Continuity Sentinel if the team has industrial procurement knowledge.

---

## The panel's second-round scoreboard

Scores: v1 = the idea as originally written; v2 = after restructuring. The panel stays hostile either way.

| Idea | v1 | V2 | Rehearse this attack |
|------|----|----|----------------------|
| Sentinel | 3 | **8** | "C-MAPSS is simulated" → method transfer, pilot framing |
| QCvision | 3 | **8** | "five examples is small" → operator sets the operating point |
| Guardian | 2 | **7** | "still surveillance" → constitution screen, counts-only flow |
| WattWatch | 3 | **7** | "confounded baseline" → CI + assumption panel |
| Mechanic's Copilot | 2 | **8** | "capture quality" → technician reviews before save |
| Dimissioni Chiare | 4 | **8** | "MDR?" → scope sentence + supervised pilot |
| PreVisit | 3 | **7** | "missed red flag responsibility" → versioned clinic rules + audit log |
| ChartKeeper | 3 | **7** | "synthetic data" → workflow familiarity |
| MedRec | 3 | **8** | "vision misreads" → per-field confidence + pharmacist confirms |
| CarePath | 2 | **7** | "reminders don't work" → confirmed checklist + human escalation |
| Saldi | 4 | **8** | "one store" → rules compared on own history |
| Never Run | 3 | **7** | "photo counting is inaccurate" → estimates + low-confidence gate |
| Voice of Customer | 3 | **8** | "sparse returns" → volume gates + self-explaining alerts |
| WISMO | 2 | **8** | "carrier feed is simulated" → play engine is the product; adapters swappable |
| Churn Radar | 3 | **7** | "uplift needs experiments" → retrospective policy evaluation |
| Museo Vivo | 3 | **8** | "museums won't buy" → replace the hardware-guide budget line |
| Race Story | 3 | **8** | "detection is trivial" → three moment types from one real race |
| Storie | 2 | **7** | "risky for children" → pre-approval + policy engine + audit log |
| AccessAll | 3 | **8** | "how good is the description" → writer gate mandatory |
| Studio One | 2 | **7** | "you're not lawyers" → enforce the client's own corpus |
| GaraBot | 3 | **9** | "OCR on scans" → low-confidence flags + page-linked cells |
| Supplier Sentinel | 3 | **7** | "noisy news" → signal triggers review, not verdict |
| 8D Quality Agent | 3 | **8** | "engineers still think" → we remove assembly, not judgment |
| Claim Intake | 2 | **8** | "quality checks cosmetic" → settlement-readiness pass/fail shown |
| Short-let Concierge | 2 | **6** | "hand-waved comune rules" → one comune, done properly |

## What survives — if you must pick today

- **Highest floor, any track:** **Sentinel V2** — measurable, demo-able on public data, the cost model gives you the "how computed" panel that hostile judges demand.
- **Highest originality for the effort:** **GaraBot V2** — real public tenders, visible golden-set evaluation, five Evolus blocks, and a value story (disqualification avoided) no one can dispute.
- **Warmest + safest:** **Dimissioni Chiare V2** — teach-back is the feature no other team will have, and the traceability weapon answers the safety questions structurally.
- **Most tasteful:** **Museo Vivo V2** — "ask the room" plus the budget-replacement pitch; if your team has any design culture, this is the one that makes judges *feel* something.
- **Best dark horse:** **WISMO V2 Exception Desk** — boring money in an overlooked corner; nobody else in the room will be doing carrier-claim automation.

## The armor slide — how to pre-empt any hostile judge

For your chosen idea, make slide one of the pitch exactly this:

1. **The expected kill shot, said out loud:** "You're thinking: another bearings demo." (Saying it first disarms it; hiding it hands it to Sofia.)
2. **The mechanism that answers it:** one sentence + one diagram (cost model / five-click bank / teach-back loop / claim grid).
3. **The live test:** "you can re-run this yourself in the demo — here's the button."
4. **The number and its method:** the computed figure and the one-screen explanation of how it was computed.

If you can't fill those four boxes for your idea, the panel already killed you; pick the V2 that can.

## Final pre-submission checklist (the panel's last pass)

- [ ] AMD part is load-bearing and benchmarked — a number on screen, re-runnable.
- [ ] Every claimed number computed by the product, with a visible method panel.
- [ ] The human gate does real work — flagged items, approvals, audit trail; not a button labeled *Approved*.
- [ ] The demo works on the messy case, not only the golden path (the second photo is blurry, the patient contradicts themselves, the scan is rotated).
- [ ] Dataset honesty: what's real, what's simulated — labeled on screen, not confessed under questioning.
- [ ] The kill shot is rehearsed with its answer — first slide of the pitch, not the Q&A.
- [ ] The buyer has a budget line and a name — say them out loud.
- [ ] Evolus only: own vLLM endpoint connected, ≥4 blocks visibly used, API calls in the stats, keys in env vars.

> Want maximum wow instead of maximum safety? The radical alternative set — ideas designed to make judges remember you — is in [11-wow-ideas.md](11-wow-ideas.md).
