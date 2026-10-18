# 15 — Ghost Expert: market and competition

Research for the deck (Phase C of [14-investor-plan.md](14-investor-plan.md)), done 18 October 2026. Each figure says where it comes from. Vendor-published numbers are marked: they are sales material, not research.

## The problem, in numbers

| Claim | Figure | Source | Strength |
|---|---|---|---|
| US manufacturing hiring need, 2024–2033 | up to 3.8 M workers | [Deloitte + Manufacturing Institute, Apr 2024](https://www2.deloitte.com/us/en/pages/about-deloitte/articles/press-releases/us-manufacturing-could-need-new-employees-by-2033.html) | Strong: survey of 200+ manufacturers |
| Of those, could go unfilled | 1.9 M (more than half) | [same](https://themanufacturinginstitute.org/manufacturers-need-as-many-as-3-8-million-new-employees-by-2033/) | Strong |
| Lockout/tagout's rank among OSHA's most-cited standards, FY2025 | No. 4, 2,562 violations | [OSHA Top 10](https://www.osha.gov/top10citedstandards); count from [Safety+Health](https://www.safetyandhealthmagazine.com/?p=52496) | Strong (rank); count is a magazine's report of OSHA's final data |
| Time for a new hire to reach full proficiency | 2–6 months | [LNS Research](https://blog.lnsresearch.com/how-to-get-a-30-day-employee-to-a-30-year-performance-level), vendor reports ([simpleclub](https://business.simpleclub.com/en-us/time-to-competency-report), [Tyfoom](https://www.tyfoom.com/employee-onboarding-training/)) | Weak: vendor material. Our own pilot must measure this |
| New hires who leave within 90 days | 1 in 3 to 1 in 2 | LNS Research blog; vendor pages | Weak: say "industry reports", don't headline it |

**Use on the deck:** the 3.8 M / 1.9 M gap and the LOTO ranking. Leave out the vendor time-to-proficiency and cost figures until our pilot measures our own.

## Market size

Published estimates disagree because they define "connected worker" differently:

- **Platforms only:** USD 1.44 B in 2025, USD 2.72 B by 2031; software is 58% of it ([Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/connected-worker-platforms-market)).
- **Broad, hardware included:** USD 8.62 B in 2025, USD 20.18 B by 2030, 18.5% CAGR ([MarketsandMarkets](https://www.marketsandmarkets.com/Market-Reports/connected-worker-market-144109467.html)).

**Use on the deck:** the platforms-only figure. It is the honest category for Ghost Expert, and a smaller number that we can defend beats a big one we can't.

**Bottom-up sizing (fill in before the deck goes out):**

```
plants (US manufacturing establishments with 100+ employees)   = [Census County Business Patterns 2022, NAICS 31–33: needs a free API key]
× share that run LOTO-style, safety-critical procedures        = [assumption, state it on the slide]
× price per plant per year                                      = [from pilot pricing, not a guess]
```

Don't put a bottom-up TAM on the deck until the price comes from a real pilot conversation.

## Competition

| Company | What it does | Where Ghost Expert differs |
|---|---|---|
| **Poka** (bought by IFS, June 2023, [IFS](https://www.ifs.com/news/corporate/ifs-acquires-poka)) | Connected-worker platform: training, skills matrix, troubleshooting. Customers include Nestlé, Tetra Pak and Mars | Instructions and training are authored by hand |
| **Augmentir** ([Series A $7.5 M, Nov 2021](https://seedtable.com/companies/augmentir/funding-rounds/series-a-2021-11)) | AI connected-worker platform: work instructions, skills, guidance | Instructions are authored in the tool, not drafted from a video of the expert |
| **Tulip** | No-code frontline operations apps, including camera checks the plant builds itself | Each app and check is built per station; nothing drafts them from an expert's video |
| **Dozuki**, **SwipeGuide** | Visual work instructions, step-by-step guides | Written by hand |
| **Retrocausal** ([~$5 M raised](https://www.vcbacked.co/company/retrocausal)) | Vision AI copilots on assembly lines | Closest in technology. Built for repetitive line assembly with a per-station setup, not "film one job, coach anyone" |
| **Drishti** | Video analytics on manual assembly lines | Line analytics for engineers, not a coach for trainees. Funding not verified |

**Ghost Expert's position:** the only one that **writes the procedure from one narrated video** (Whisper + SigLIP + Gemma, with the expert approving) **and then checks each step live on camera**, with a rule engine that won't accuse anyone on a single model answer.

**The risk to say out loud:** Poka/IFS or Augmentir could add video drafting. Our answers are speed, the per-plant library of approved procedures and footage, and on-site deployment so video never leaves the plant.

Claims about competitors stay to what their own sites say they do. Check each company's site before a meeting.

## Still to verify before the deck goes out

- [ ] Tulip's total funding: sources disagree (Owler says $272.7 M including a January 2026 round). Check the company's own announcements.
- [ ] Drishti's funding and current status.
- [ ] The bottom-up plant count, from Census CBP with a free API key.
