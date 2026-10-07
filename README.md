# Liquid AI LFM2.5-2.6B Humanizer

A production-grade text-to-text humanizer fine-tuning pipeline for **`LiquidAI/LFM2.5-2.6B`** across four core prose domains:
- **Blog** (casual, engaging, authentic cadence)
- **Website Copy** (punchy, conversion-focused, direct)
- **Documentation** (technical clarity, structured, concise)
- **Short Story** (narrative voice, emotional resonance, sensory rhythm)

This repository serves as the single source of truth for orchestration across local development, Google Colab GPU training, Hugging Face Hub, Weights & Biases telemetry, and Agency Gateway inference.

---

## Architecture & Locked Design Decisions

| Parameter | Specification | Details / Rationale |
|---|---|---|
| **Base Model** | `LiquidAI/LFM2.5-2.6B` | Dense text architecture (2.69B params, 131k context window, 128k vocab, hybrid Conv/GQA). |
| **Fine-Tuning Method** | 16-bit LoRA | Rank $r=16$, $\alpha=32$, dropout $0.05$. Target modules: `q_proj, k_proj, v_proj, out_proj, in_proj, w1, w2, w3`. |
| **Framework** | Unsloth + TRL | `transformers==4.57.6`, `trl==0.22.2 --no-deps`, latest Unsloth. Fast, memory-efficient LoRA. |
| **Compute Engine** | Google Colab | 200 Compute Units (CU) / month budget; L4 GPU preferred for 4096 sequence length. |
| **Data Construction** | Real Traces + Style Packs | Real LLM traces rewritten into human style packs, augmented with authentic human-target anchors. |
| **Telemetry** | Weights & Biases | Entity: `navin_hill`, Project: `copyright`. Real-time step loss, tok/s throughput, and CU tracking. |
| **Artifact Hub** | Hugging Face Hub | Repositories under `jamesnavinhill/lfm25-humanizer-*` for datasets, adapters, and merged weights. |

For the complete technical specification, review [`plan.md`](file:///c:/Users/james/projects/labwork/unsloth/plan.md).

---

## Repository Structure

```
unsloth/
├── .agents/skills/      # HF CLI, Hugging Face Datasets, LLM Trainer skills
├── datasets/
│   └── LEDGER.md        # Provenance and license ledger for all corpora
├── notebooks/           # Colab training and verification notebooks
├── runs/
│   └── README.md        # Run contract: run.json, metrics.jsonl, notes.md
├── CONNECTIONS.md       # Nominal integration directory and credential guides
├── ORCHESTRATION.md     # Multi-surface workflow rules and fail-safe protocols
├── plan.md              # Execution plan v2 (locked decisions D1–D9)
├── STATE.md             # Live project dashboard (phase, runs, CU budget)
├── TASKS.md             # Active task board (T1–T15)
├── .env.example         # Environment template (secrets are strictly excluded)
└── .gitignore           # Airtight exclusion of secrets and heavy binaries
```

---

## Getting Started

### 1. Clone & Environment Setup

```bash
git clone https://github.com/jamesnavinhill/unsloth.git
cd unsloth

# Copy environment template and fill in local values
cp .env.example .env
```

### 2. Verify Connections

Review [`CONNECTIONS.md`](file:///c:/Users/james/projects/labwork/unsloth/CONNECTIONS.md) for full credentials, endpoints, and authentication guides for GitHub, Hugging Face, Weights & Biases, Kaggle, and the Agency Gateway.

### 3. Workflow Protocol

Always check [`STATE.md`](file:///c:/Users/james/projects/labwork/unsloth/STATE.md) and [`TASKS.md`](file:///c:/Users/james/projects/labwork/unsloth/TASKS.md) before starting any run:
1. **Claim** the task in `TASKS.md` (`IN PROGRESS`).
2. **Execute** under the run contract (`runs/<run-id>/` with `run.json`, `metrics.jsonl`, `notes.md`).
3. **Record** throughput (tok/s), peak VRAM, and CU consumption.
4. **Close out** the task and update `STATE.md`.

---

## License

Model base fine-tuning is governed by the [LFM Open License v1.0](https://www.liquid.ai/lfm-license). Dataset provenance is recorded per corpus in [`datasets/LEDGER.md`](file:///c:/Users/james/projects/labwork/unsloth/datasets/LEDGER.md).
