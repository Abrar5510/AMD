# 14 — Ghost Expert: investor plan (do now)

Only work that can be done at a desk today: code, copy and documents. No filming, no GPU box, no meetings. Everything that needs the physical world is in [../ghost-expert/ROADMAP.md](../ghost-expert/ROADMAP.md).

The positioning for every phase: **Ghost Expert cuts the time it takes a new hire to become competent, and leaves an audit trail.** The safety flag stays, framed as "flags the skipped step" with a supervisor signing off, not "stops injuries".

## Phase A — Honesty and hygiene (today)

- [x] README: the rule engine's catch rate matches `eval/sim_results.md` (92%, not 98%).
- [x] Commit the README fix.
- [x] Reword "stops them before they get hurt" in the README tagline and `submission/cover.html` (and `cover.png`) to the competence + audit-trail framing. The demo script promises no injury prevention, so it stays as rendered.
- [ ] Every number in the README, cover and deck says whether it is simulated or measured.
- [x] Check for secrets: no keys in the repo, `.env` stays ignored.
- [x] `python -m tests.test_coach` and `python -m tests.test_author` pass.

## Phase B — Product gaps that need no footage

What exists: multi-procedure storage (`GET /api/procedures`), upload → draft → approve → coach, replay mode, presenter reset (`R`), the training record with PDF and JSON.

- [x] **Phone and tablet camera.** `coach.html` asks for any camera, so a phone opens the selfie camera. Ask for the rear camera (`facingMode: "environment"`) and check the coach layout at phone width.
- [x] **Supervisor sign-off.** The training record gets a supervisor name, date and "Signed off" action. The coach's verdict shows "Pending supervisor sign-off" until it is signed. The record takes the trainee's name, and the PDF, JSON and xAPI include both names.
- [x] **LMS export.** A "Download xAPI" button on the training record that writes xAPI statements (completed, step times, mistakes, verdict). SCORM packaging waits until a customer asks.
- [x] **"Try it yourself" mode.** One guided path for a visitor: upload a phone video → watch the draft appear → approve → get coached. Each visitor gets their own random procedure id so demos never overwrite each other. End-to-end testing needs the GPU box (roadmap).

## Phase C — Investor materials

- [ ] **Pitch deck draft**, 10 slides: problem, demo, how it works, numbers, pilot, market, competition, moat, team, ask. Slides that need real numbers carry a visible `[PENDING: filmed eval]` placeholder.
- [ ] **Competition one-pager.** Augmentir, Dozuki, Poka, SwipeGuide, Tulip (digital work instructions), Drishti and Retrocausal (vision on the line). Ghost Expert's difference: the AI drafts the procedure from one video, and it checks each step live.
- [ ] **Market sizing** with cited sources: frontline training and connected-worker spend, bottom-up from plants × stations × price.
- [ ] **Customer interview script** for plant training, EHS and quality managers: onboarding cost, time to competence, how sign-offs are documented today, what they would pay to halve it.
- [ ] **Pilot proposal one-pager** and **LOI template**, ready to send after the first good conversation.
- [ ] **Demo film v2: script and shot list**, so filming day is one session. Order: problem → real expert video drafted into steps → trainee coached and flagged → training record → real numbers. Same HeyGen voice, no music.
