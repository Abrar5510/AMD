# AMD Developer Hackathon: ACT III

> **Build AI agents and high-performance AI applications on AMD GPUs in the cloud.**

---

## Overview

The **AMD Developer Hackathon: ACT III** is a hands-on event for developers, founders, engineers, and builders who want to push what's possible with AI on real infrastructure. Whether you are just starting out or already shipping, you can jump in and start creating.

You'll be working with **AMD GPUs in the Cloud** with the **ROCm software stack**, AMD's open-source GPU computing platform. Everything runs fully in the cloud — there is no local hardware to set up, so you can focus on building instead of configuration.

> **One hackathon. Three cities. One special weekend in Italy.**

---

## Event Format

### Online Phase
- **Dates:** 12–18 October 2026

### On-Site Phase — Italy
- **Dates:** 17–18 October 2026

The hackathon remains open online throughout the event, while selected participants can also join in person for the on-site phase. If approved, you'll choose one of three locations to build alongside other developers, get hands-on support, and showcase your project live.

### On-Site Locations

| City   | Venue                  | Address                                              | Opening / Closing                                    |
|--------|------------------------|------------------------------------------------------|------------------------------------------------------|
| Rome   | Link Campus University | Via del Casale di San Pio V, 44, 00165 Roma          | 10:00 AM – 6:00 PM (Oct 17) / 10:00 AM – 5:00 PM (Oct 18) |
| Milan  | SmartCityLab Milano    | Via Giuseppe Ripamonti, 88, 20141 Milano MI          | 9:00 AM – 6:00 PM (Oct 17) / 9:00 AM – 5:00 PM (Oct 18)   |
| Imperia| IMPERIAWARE            | Via Antonio Delbecchi, 22, 18100 Imperia (IM)        | 9:00 AM – 6:00 PM (Oct 17) / 9:00 AM – 5:00 PM (Oct 18)   |

---

## Challenges

> **Solve a real business problem with AMD technology.**

Choose one or more tracks and build a working product on AMD infrastructure. We are looking for projects that solve a real problem for a real user. Your idea can use language models, computer vision, audio, agents, predictive models, or a combination of technologies.

The important part is simple: **the product should work, and AMD technology should power a meaningful part of it.** AMD is a **required technology** to be eligible for prizes.

---

### Track 1 (by Partner: Vibe Generation) — Intelligent Industry

> **Help factories spot problems earlier and operate better.**

#### Brief
Factories produce data from machines, cameras, sensors, maintenance reports, and technical manuals. The problem is rarely a lack of information. The problem is knowing what matters and what to do next.

Build a product that helps a manufacturer **reduce downtime, improve quality, increase safety, or use resources more efficiently.**

#### Ideas
- Predict equipment failures
- Detect defects from images or video
- Explain production anomalies
- Help technicians search manuals and maintenance records
- Recommend maintenance actions
- Monitor safety conditions
- Reduce energy or material waste

#### Demo Expectation
Show your product processing realistic industrial data and producing a useful alert, explanation, recommendation, or action. Make it clear who would use the product and what result it improves.

#### What Good Projects Will Show
- A real manufacturing problem
- A working product, not only a dashboard or presentation
- Results that operators can understand
- A measurable improvement in time, cost, safety, quality, or efficiency

---

### Track 2 (by Partner: Vibe Generation) — Health and Wellbeing

> **Make a part of the patient journey safer, clearer, or easier.**

#### Brief
Patients and healthcare workers deal with long documents, scattered information, repetitive administration, language barriers, and limited time.

Build a product that helps patients, caregivers, or healthcare staff handle one part of this journey better.

#### Ideas
- Patient intake
- Medical record summaries
- Appointment preparation
- Care navigation
- Clearer discharge instructions
- Multilingual patient communication
- Healthcare document processing
- Administrative workflow automation
- Wellbeing and prevention support

#### Demo Expectation
Show a realistic case from the first input to the final result. Your product should make uncertainty visible. It should also know when a person needs to review or take over the case.

#### Safety Rules
The product **must not** present autonomous diagnosis or treatment as medical advice. Explain how you handle:
- Incorrect or unsupported responses
- Sensitive information
- Uncertain results
- High-risk decisions
- Human review

#### What Good Projects Will Show
- A clearly defined patient or staff need
- Responsible handling of health information
- Useful and understandable results
- A measurable improvement in time, accuracy, accessibility, or workload

---

### Track 3 (by Partner: Vibe Generation) — Reinvent Commerce

> **Help a business understand its customers and take better action.**

#### Brief
Retailers have product data, transactions, inventory, reviews, support conversations, and marketing results. These sources are often disconnected, which makes it difficult to turn them into useful decisions.

Build a product that helps a business **attract, serve, convert, or retain customers.**

#### Ideas
- Shopping assistants
- Product discovery and recommendations
- Customer support
- Demand and inventory planning
- Product catalogue enrichment
- Review and sentiment analysis
- Promotion planning
- Churn prevention
- Accessible and multilingual shopping
- In-store computer vision

#### Demo Expectation
Show how your product turns customer or business data into a useful recommendation or action.

> ⚠️ If your product predicts demand, sales, or customer behaviour, **explain how the prediction was calculated.** Do not use a language model as the only forecasting method.

#### What Good Projects Will Show
- A real customer or merchant problem
- A useful commercial action
- Relevant recommendations or personalization
- A measurable effect on revenue, margin, conversion, retention, inventory, or service quality

---

### Track 4 (by Partner: Vibe Generation) — Create a New Kind of Experience

> **Build a media, marketing, or entertainment experience that was not practical before generative AI.**

#### Brief
Do more than generate an image, advertisement, or chatbot. Create something that responds to its audience, changes with context, or produces a different experience for each person.

#### Ideas
- Personalized video
- Interactive stories
- Audience-driven entertainment
- Adaptive campaigns
- Multilingual creative content
- Generative brand experiences
- Responsive sound or visual environments
- New social media formats
- Accessible media experiences
- Creative quality control

#### Demo Expectation
Show the experience changing for at least **two different audiences, situations, or inputs.** Explain:
- What the team created
- What the models generated or decided
- How you controlled quality and consistency
- How much each generated experience costs
- Who would pay for it and why

#### What Good Projects Will Show
- An original concept
- A strong user experience
- A thoughtful combination of human creativity and technology
- A product that could work at a realistic cost

---

## Evolus Track: Business Agents on AMD

> **Build an AI agent that runs a real business process end-to-end, on Evolus, powered by an open model served on AMD.**

Pick a process that a real company runs every day and let an agent run it. The agent:
1. Takes the input (an email, a PDF, a recording, a web form, a chat)
2. Reasons over it with an **open model running on AMD** through your own vLLM endpoint on AMD Developer Cloud
3. Acts: it runs an Evolus workflow, turns documents into data, uses AI Tools, updates another system, or hands the case to a person when it should

### Requirements
- Build in a **free Evolus event workspace**, created at `app.evolus.ai` with the event code shared at kickoff.
- **Bring your own model:** the main agent must use an **open model served on AMD infrastructure** through your own **vLLM endpoint** on AMD Developer Cloud.
- Use **at least two Evolus building blocks:** workflows, document extractors, AI Tools, knowledge libraries, MCP connectors, sub-agents, chat widget.
- **Drive Evolus from your app through its APIs:** the Evolus REST API for workflows, extractors, AI Tools, and libraries; agent chat through the REST API or the OpenAI-compatible endpoint.
- Follow the hackathon submission rules: **containerized app, public GitHub repository, a README that runs.** Never commit API keys — use environment variables.

### Sample Use Cases

| Use Case                  | Input                            | What the Solution Does                                                                                          |
|---------------------------|----------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Invoice and order intake  | Emails with PDF attachments      | A workflow started by incoming email reads the PDF, extracts the fields into JSON, matches them to the order and flags mismatches to a person |
| Support desk on company knowledge | Chat, email, or website widget | An agent answers from the company's documents with sources and passes the case to a person when unsure |
| Lead qualification        | Chat widget on a website          | Qualifies the visitor, books a call and pushes the lead to a CRM through MCP                                    |
| Contract review           | Uploaded contracts                | Extracts key clauses, compares them with the company's standard terms and redacts personal data before sharing |
| Multilingual documents    | PDF and Word files                | Translates manuals and offers keeping their layout, then files them through a workflow                          |
| Meeting follow-up         | Recordings of calls and meetings | Turns the recording into minutes and action items and sends them to the attendees                              |

### Judging (Evolus Track)
The hackathon's four criteria applied to this track:

- **Application of Technology** — How deeply the solution uses Evolus building blocks, and how well the AMD-hosted model is integrated.
- **Business Value** — A real process, a clear user, a measurable gain.
- **Originality** — A new approach, or a process nobody automated this way.
- **Presentation** — A clear demo and pitch.

> ℹ️ To verify the requirements, the Evolus team reviews the configuration and usage statistics of each event workspace: the connected model endpoint, the building blocks used, and the API calls.

---

## Technology Requirements

> Every project must run a meaningful part of its workload on **AMD infrastructure or AMD hardware.**

Teams may use:
- **AMD Developer Cloud**
- **AMD Instinct accelerators**
- **AMD ROCm**
- **AMD Ryzen AI**
- **AMD Radeon hardware**
- Other approved AMD-powered infrastructure provided during the event

The **AMD component must be part of the working product shown to the judges.** Teams may choose their own compatible models, frameworks, and development tools.

### FAQ
1. The event is hosted on `notebooks.amd.org/tokenfactory`. There is no billing or credit card info needed.
2. Developers don't need the $100 credit to participate in the event — just the API from the tokenfactory.

### Partner Awards
Google and Evolus technologies are **optional**. Teams that use an eligible partner technology can also compete for that partner's prize. A single project may qualify for the main challenge prize, one partner prize, or both partner prizes.

---

## Partners

### Lead Partner — AMD (MANDATORY for all challenges)
This hackathon gives developers the opportunity to explore and build AI workloads using AMD's cloud-based AI stack. All development happens on cloud-accessible AMD GPUs, so there is no need to own or manage hardware.

The focus is on experimenting, benchmarking, and running real workloads in a flexible environment. During the hackathon, teams can choose to work with the technologies below.

#### AMD Developer Cloud
On-demand access to AMD GPUs through the cloud. Spin up a GPU environment in minutes and build and test AI workloads without infrastructure overhead.
- Training and fine-tuning models
- Benchmarking AI workloads on AMD GPUs
- Prototyping before moving to on-prem infrastructure

#### ROCm
ROCm is AMD's open-source software platform for GPU computing — the AMD equivalent of CUDA. It runs AI/ML and HPC workloads on AMD GPUs.
- Running PyTorch and TensorFlow on AMD GPUs
- Porting CUDA-based workloads to AMD hardware
- High-performance AI and ML workloads

#### AMD AI Developer Program
Membership in the AMD AI Developer Program (ADP) unlocks the AMD developer ecosystem around the hackathon.
- AI tutorials, training, and technical resources
- Access to AMD engineers and technical experts
- Private community channels and developer updates

#### Training & Learning Resources
Curated AI learning material, tutorials, and hands-on labs to help you build faster during the event.
- AMD AI Academy courses and documentation
- Hands-on labs with real GPU access
- Fully cloud-based — no local setup required

**Key Links:**
- AMD AI Developer Program
- AMD cloud development
- ROCm AI Developer Hub
- ROCm documentation
- ROCm installation guide
- `github.com/ROCm/ROCm`

---

### Technology Partners

#### Google — Gemma on AMD GPUs
You can now build with **Gemma**, Google DeepMind's family of open models, running on AMD GPUs in the cloud using AMD Developer Cloud and ROCm. Use Gemma in your project for a chance to win the Google prize.

> As Google DeepMind, our world-class talent is harnessing our unparalleled computing infrastructure to create the next wave of research breakthroughs and transformative products. Guided by the scientific method and with a holistic approach to responsibility and safety, we're working to ensure AI benefits everyone and helps solve the biggest challenges facing humanity.

- Gemma documentation
- Gemma Website

#### Vibe Generation
**Vibe Generation** is the project founded by **Paolo Bonetti** to integrate specialized professionals and artificial intelligence tools into the real-world processes of businesses.

The model was created to support companies, brands, and organizations in moving from the occasional use of AI tools to building **hybrid teams and processes**, in which technology and human skills work together.

The project focuses in particular on the relationship between artificial intelligence, talent, judgment, and organizational transformation.

#### Evolus AI
**Evolus AI** — The platform to build AI agents that run real business processes. Bring your own AMD-hosted model and ship an agent that does real work.

Evolus gives companies AI agents that:
- Read documents
- Answer from company knowledge
- Run automations
- Act on the systems they already use through APIs and MCP

Businesses also use Evolus for **digital employees** that work in email and Microsoft Teams, and for an **AI Switchboard** that answers the phone.

For developers:
- Everything is driven by the Evolus REST API
- Agents can also be reached through an OpenAI-compatible endpoint
- An MCP server lets coding agents build on Evolus directly
- During the hackathon, every team brings its own model

> 🎟️ **500 Evolus AI coupons available.** Coupons are available on a first-come, first-served basis, while supplies last.
>
> [Claim your Evolus AI coupon →]

---

### Additional Partners

#### PwC Italy
PwC's purpose is to **build trust in society and solve important problems** by providing innovative responses to complex challenges. PwC operates through **23 offices in Italy** with more than **9,000 professionals** committed to delivering high-quality tax, legal, audit, and consulting services across organizational and strategic areas. PwC offers an extensive range of integrated and multidisciplinary services.

PwC's true strength lies in its ability to combine in-depth knowledge of local markets with a globally integrated network. With **over 364,000 people in 136 countries**, it is one of the world's largest networks of professional services firms.

#### Imment
**Building the Future of Startups.** We help you create, fund, and manage your startup using innovative tools and specialized expertise in Administration, Finance, and Control.

#### BAC Network
We conduct outreach initiatives — such as events, workshops, and roundtables — aimed at fostering a local entrepreneurial culture. We:
- Bridge the funding gap for innovative startups through co-investments
- Provide strategic guidance based on our expertise
- Grow businesses by leveraging our personal and professional networks

---

## Prizes

### Total Prize Pool: $17,000+

### AMD Prizes — $5,000
| Place | Prize |
|-------|-------|
| AMD   | $5,000 in prizes from AMD |

### Google Prizes — $5,000
| Place | Prize |
|-------|-------|
| Google | $5,000 in prizes from Google |

### Evolus Track: Business Agents Prizes

| Place      | Prize                                                                                                                                                              |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 🥇 1st Place | **€578** — 12 months of the Evolus Developer plan for the team + 1,000,000 bonus credits + a showcase on evolus.ai                                                |
| 🥈 2nd Place | **€289** — 6 months of the Evolus Developer plan for the team + 500,000 bonus credits                                                                              |
| 🥉 3rd Place | **€144.50** — 3 months of the Evolus Developer plan for the team + 250,000 bonus credits                                                                          |

> **Evolus Track Total: €1,011.50**
>
> Values at list price, VAT excluded: the Evolus Developer plan costs €29 per month, and bonus credits are valued at €0.23 per 1,000.

### Vibe Generation Special Prize
> **The best solution will be awarded with AirPods 5 for all members of the team.**

The solution will be judged based on those 3 criteria:

| Criterion    | Description                                                                                       |
|--------------|---------------------------------------------------------------------------------------------------|
| **Hybrid**       | Strategic thinking, ability to quantify value, commercial attitude.                              |
| **Becreatives**  | Quality of technical execution, orchestration of AI tools, ability to ship.                      |
| **Vibe Generation** | Taste, originality of the concept, design of the human + AI creative workflow.                   |

### Imment: Best Italian Teams Startup Incubation Opportunity

The three most promising startup ideas will be selected to receive dedicated **incubation support**, helping teams transform innovative concepts into viable ventures.

| Team    | Prize                  | Value    |
|---------|------------------------|----------|
| Team 1  | Startup Award Program  | €1,599   |
| Team 2  | Startup Award Program  | €1,599   |
| Team 3  | Startup Award Program  | €1,599   |

> ⚠️ Please note: participation in lablab.ai hackathons is voluntary. Prizes and opportunities depend on eligibility, availability, and third-party sponsors. Hackathon rules, prizes, and terms may change or be canceled at our discretion. Submissions must be original and MIT-compliant. Prize distribution may take up to 90 days. Full details.

---

## Before You Start Building — Guidelines

### How to Participate
The hackathon takes place online on the **lablab.ai platform** and the **lablab.ai Discord server**. Please register for both in order to participate.

To join:
1. Click the **Enroll** button at the bottom of the page.
2. Read the:
   - Hackathon Guidelines
   - Getting Started Guide
   - lablab.ai Hackathon Rule Book

> ⚠️ To be approved for the hackathon, participants must also **sign up for the AMD AI Developer Program.**

> Everyone is welcome to participate, regardless of previous AI or coding experience.

> Before the kickoff, browse the **AI Tech and tutorials pages** to read up on the available technologies and get a head start on your project.

### Teams
- Teams consist of **1–6 people.**
- If you don't have a team, you can connect with other participants from all over the world on the **dashboard** or on the **Discord server**, where you can also find teammates and bounce around ideas.

---

## What to Submit

### 📋 Basic Information
- Project title
- Short description
- Long description
- Technology & category tags
- Selected challenge

### 📸 Cover Image and Presentation
- Cover image
- Video presentation (demo video)
- Slide presentation (pitch presentation)
- Clear explanation of the problem and intended user

### 💻 App Hosting and Repository
- Public GitHub repository
- Demo application platform
- Application URL
- Working prototype

---

## Judging Criteria

| Criterion                  | Description                                                                                                          |
|---------------------------|----------------------------------------------------------------------------------------------------------------------|
| **Application of Technology** | How effectively the chosen model(s) are integrated into the solution.                                              |
| **Presentation**          | The clarity and effectiveness of the project presentation.                                                          |
| **Business Value**        | The impact and practical value, considering how well it fits into business areas.                                    |
| **Originality**           | The uniqueness and creativity of the solution, highlighting approaches and ability to demonstrate behaviors.        |

---

## Quick Reference Summary

| Item                        | Detail                                                              |
|-----------------------------|---------------------------------------------------------------------|
| **Event Name**              | AMD Developer Hackathon: ACT III                                    |
| **Online Phase**            | 12–18 October 2026                                                  |
| **On-Site Phase (Italy)**  | 17–18 October 2026 (Rome, Milan, Imperia)                           |
| **Prize Pool**              | $17,000+                                                            |
| **Team Size**               | 1–6 people                                                          |
| **Mandatory Technology**    | AMD (Developer Cloud, ROCm, Instinct, Ryzen AI, Radeon)             |
| **Optional Partner Tech**  | Google Gemma, Evolus AI                                             |
| **Platform**                | lablab.ai + Discord                                                 |
| **Notebooks**               | notebooks.amd.org/tokenfactory                                      |
| **Required Sign-Up**        | AMD AI Developer Program                                            |
| **Main Tracks (Vibe Gen)** | Intelligent Industry · Health & Wellbeing · Reinvent Commerce · Create a New Kind of Experience |
| **Partner Track**           | Evolus — Business Agents on AMD                                     |
| **Submission License**      | MIT-compliant                                                       |
| **Prize Distribution**      | Up to 90 days                                                       |
