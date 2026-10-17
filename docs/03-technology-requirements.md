# 03 — Technology Requirements

## Mandatory vs optional

| Technology | Status | Why it matters |
|------------|--------|----------------|
| **AMD** | **MANDATORY** for every project and every track | No AMD → not eligible for any prize |
| Google Gemma | Optional | Use it to compete for the **Google prize** |
| Evolus AI | Optional (mandatory only inside the Evolus track) | Use it to compete for the **Evolus prizes** |

You may choose your own compatible models, frameworks and dev tools.

## The AMD rule, precisely

1. Every project must run a **meaningful part of its workload** on AMD infrastructure or AMD hardware.
2. The AMD component must be **part of the working product shown to the judges** — not a side experiment.

### Accepted AMD options

- AMD Developer Cloud
- AMD Instinct accelerators
- AMD ROCm
- AMD Ryzen AI
- AMD Radeon hardware
- Other approved AMD-powered infrastructure provided during the event

## Access & cost FAQ

- The event runs on **`notebooks.amd.org/tokenfactory`**.
- **No billing or credit card** is needed.
- You **don't need the $100 credit** — only the API from the tokenfactory.

## What each AMD piece is for

| Piece | What it is | Typical use in the hackathon |
|-------|-----------|------------------------------|
| **AMD Developer Cloud** | On-demand AMD GPUs in the cloud; spin up in minutes | Training / fine-tuning, benchmarking, prototyping, hosting a vLLM endpoint |
| **ROCm** | AMD's open-source GPU computing platform (≈ CUDA for AMD) | Running PyTorch / TensorFlow, porting CUDA code, high-performance AI/ML |
| **AMD AI Developer Program (ADP)** | Membership program — **sign-up required for approval** | Tutorials, training, access to AMD engineers, private community channels |
| **Training & Learning Resources** | AMD AI Academy, docs, hands-on labs with real GPUs | Learning fast during the event, fully cloud-based |

### Key links (names as given in the brief)

- AMD AI Developer Program
- AMD cloud development
- ROCm AI Developer Hub
- ROCm documentation
- ROCm installation guide
- `github.com/ROCm/ROCm`

## Google Gemma on AMD

Gemma (Google DeepMind's open models) runs on AMD GPUs via AMD Developer Cloud + ROCm. Using Gemma makes you eligible for the Google prize. Resources: Gemma documentation, Gemma website.

## Prize stacking

One project can qualify for: the **main challenge prize**, **one partner prize**, or **both partner prizes** (Google + Evolus). Details in [04-prizes.md](04-prizes.md).
