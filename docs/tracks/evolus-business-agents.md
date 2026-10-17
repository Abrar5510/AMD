# Evolus Track — Business Agents on AMD

**Partner:** Evolus AI
**Goal:** An AI agent that runs a **real business process end-to-end**, on Evolus, powered by an **open model served on AMD**.

## How the agent should work

```
 INPUT                    REASON                               ACT
 email / PDF /     ──►    open model on AMD, via YOUR   ──►    run an Evolus workflow, turn docs into
 recording / web          own vLLM endpoint on                 data, use AI Tools, update another
 form / chat              AMD Developer Cloud                  system, or hand off to a person
```

Pick a process a real company runs every day and let the agent run it.

## Hard requirements (all must be true)

- [ ] Built in a **free Evolus event workspace** at `app.evolus.ai`, using the **event code shared at kickoff**.
- [ ] **Bring your own model:** the main agent uses an **open model** served on AMD through **your own vLLM endpoint** on AMD Developer Cloud.
- [ ] Uses **at least two** Evolus building blocks from:
  - workflows
  - document extractors
  - AI Tools
  - knowledge libraries
  - MCP connectors
  - sub-agents
  - chat widget
- [ ] Your app **drives Evolus through its APIs**:
  - Evolus **REST API** for workflows, extractors, AI Tools and libraries
  - Agent chat via the **REST API** or the **OpenAI-compatible endpoint**
- [ ] Follows hackathon submission rules: **containerized app**, **public GitHub repo**, **a README that actually runs**.
- [ ] **No API keys committed** — use environment variables.

> ℹ️ **How this is verified:** the Evolus team inspects each event workspace's configuration and usage stats — the connected model endpoint, the building blocks used, and the API calls made. If it isn't in the workspace logs, it doesn't count.

## Sample use cases

| Use case | Input | What the solution does |
|----------|-------|------------------------|
| Invoice & order intake | Emails with PDF attachments | Email-triggered workflow reads the PDF, extracts fields to JSON, matches to the order, flags mismatches to a person |
| Support desk on company knowledge | Chat, email, or website widget | Answers from company documents **with sources**; hands off to a person when unsure |
| Lead qualification | Website chat widget | Qualifies the visitor, books a call, pushes the lead to a CRM via MCP |
| Contract review | Uploaded contracts | Extracts key clauses, compares to standard terms, redacts personal data before sharing |
| Multilingual documents | PDF and Word files | Translates manuals and offers keeping the layout, then files them via a workflow |
| Meeting follow-up | Call / meeting recordings | Produces minutes + action items and sends them to attendees |

## Judging (Evolus track)

The four standard criteria, applied to this track:

| Criterion | What it means here |
|-----------|--------------------|
| Application of Technology | How deeply you use Evolus building blocks, and how well the AMD-hosted model is integrated |
| Business Value | A real process, a clear user, a measurable gain |
| Originality | A new approach, or a process nobody has automated this way |
| Presentation | A clear demo and pitch |

## Prizes

See [../04-prizes.md](../04-prizes.md#evolus-track--business-agents). Coupons: 500 Evolus AI coupons, first-come first-served.
