# CONNECTIONS — Nominal Infrastructure & Integration Directory

This document details every external and internal connection used across the **LFM2.5-2.6B Humanizer** pipeline. In accordance with project discipline, all setups follow the **nominal configuration**—direct, authenticated, auditable protocols without temporary workarounds.

---

## 1. Connection Topology Map

```
                     ┌──────────────────────────────────────────────┐
                     │          Local Orchestration Core            │
                     │          (labwork/unsloth)                   │
                     │  - Single source of truth (STATE/TASKS/runs) │
                     │  - Local secrets (.env - gitignored)         │
                     └───────┬───────────────────────────────┬──────┘
                             │                               │
            ┌────────────────┴──────────────┐                │
            ▼                               ▼                ▼
   ┌─────────────────┐             ┌─────────────────┐   ┌─────────────────┐
   │  GitHub Remote  │             │  Google Colab   │   │  Agency Gateway │
   │  (Public Repo)  │             │  (GPU Training) │   │  (LiteLLM API)  │
   │ jamesnavinhill/ │             │ T4 / L4 / A100  │   │ 213 LLM models  │
   │    unsloth      │             │  Colab Secrets  │   │  T7/T9/T10/T12  │
   └─────────────────┘             └────────┬────────┘   └─────────────────┘
                                            │
                       ┌────────────────────┴────────────────────┐
                       ▼                                         ▼
             ┌─────────────────────┐                   ┌───────────────────┐
             │  Hugging Face Hub   │                   │ Weights & Biases  │
             │ - Base Model (2.6B) │                   │ Entity: navin_hill│
             │ - HF Buckets (CC)   │                   │ Project: copyright│
             │ - Adapters & Merged │                   │ Live step metrics │
             └─────────────────────┘                   └───────────────────┘
```

---

## 2. Service-by-Service Nominal Specifications

### 2.1 GitHub (Source Code & Workflow Synchronization)
* **Remote Repository**: `https://github.com/jamesnavinhill/unsloth.git`
* **Account**: `jamesnavinhill`
* **Authentication**: HTTPS authenticated via Git Credential Manager and `gh` CLI.
* **Token Role**: `gho_` / PAT with scopes `repo`, `workflow`, `gist`, `read:org`.
* **Discipline**:
  - Main development branch: `main`.
  - All project state (`STATE.md`, `TASKS.md`, `ORCHESTRATION.md`, `plan.md`, `runs/`) is version-controlled.
  - `.env` and all secrets are strictly excluded via `.gitignore`.
  - Raw datasets and heavy model weights are stored on Hugging Face Hub, not GitHub.

### 2.2 Hugging Face Hub & Buckets (Model & Data Artifacts)
* **Account**: `jamesnavinhill`
* **Authentication**: `HF_TOKEN` (fine-grained token with **Write** role, named `unsloth`).
* **Base Model**: `LiquidAI/LFM2.5-2.6B` (license: LFM Open License v1.0).
* **Published Repositories**:
  - Adapters: `jamesnavinhill/lfm25-humanizer-lora`
  - Merged weights: `jamesnavinhill/lfm25-humanizer-2.6b`
  - GGUF Quantizations: `jamesnavinhill/lfm25-humanizer-gguf`
  - Datasets: `jamesnavinhill/lfm25-humanizer-pairs-v1`
* **Storage Buckets** (Public, verified token-readable 2026-10-07):
  - `jamesnavinhill/CommonCrawl-CreativeCommons-bucket`: 251.1 GB, 300 parquet files (`data/<crawl>/<lang>/*.parquet`), includes root `README.md` and `counts.json`.
  - `jamesnavinhill/cccc_all_domains-bucket`: 393.1 GB, 653 files.
  - **Nominal Access Protocol**: HF Buckets do not use standard `resolve/main` HTTP endpoints. File inventory and downloads are managed nominally through the `hf` CLI (`.agents/skills/hf-cli/`) or `huggingface_hub` Bucket API.

### 2.3 Weights & Biases (Experiment Tracking)
* **Account**: `jamienavinhill`
* **Entity**: `navin_hill`
* **Project**: `copyright` (operator-designated active project)
* **Primary Key**: `WANDB_API_KEY` (verified via GraphQL viewer).
* **Backup Key**: `WANDB_SA_API_KEY` (service-account key, spare).
* **Logged Telemetry**:
  - Training loss and validation loss per step.
  - Token throughput (`tokens_per_second`).
  - Peak GPU VRAM allocated and reserved.
  - Step-wise Colab Compute Unit consumption.
  - Tripwire monitors: Overfitting tripwires (eval/train > 1.5, train loss < 0.2).

### 2.4 Agency Gateway (LiteLLM Proxy)
* **Endpoint**: `https://gateway.yrka.io/v1`
* **Fallback Endpoint**: Configured via `GATEWAY_FALLBACK_URL`.
* **Authentication**: `GATEWAY_API_KEY` Bearer token.
* **Status**: Live, verified 213 available models (2026-10-07).
* **Target Roles**:
  - **T7 Rewriter Model**: Models like `or-nvidia-nemotron-3-ultra-550b`, `ne-gpt-oss-120b`, or `or-liquid-lfm-2.5-2.6b` for few-shot rewriting of trace responses into domain style packs.
  - **T9 Rewrite-at-scale**: Fast asynchronous batch processing of prompt-response pairs.
  - **T10 / T12 Evaluator Judge**: Model-based evaluation for fact-fidelity, naturalness, and 5-gram copy-reuse metrics.

### 2.5 Kaggle (Provenance Verification)
* **Account**: `jamesnavinhill` (`KAGGLE_USERNAME`)
* **Authentication**: `KAGGLE_API_TOKEN` (`KGAT_...`).
* **Nominal Protocol**: Authenticates directly via HTTP Basic Auth (`username:token`) against `https://api.kaggle.com/v1/`.
* **Zero Workaround**: Does not require creating or writing local `~/.kaggle/kaggle.json` credential files.
* **Role**: Verification of dataset licensing and author provenance (e.g. `youssefelebiary/human-written-text`).

### 2.6 Google Colab (Compute Engine)
* **Budget**: ~200 Compute Units (CU) / month.
* **Hardware Profiles**:
  - Smoke / Verification (T1): T4 or L4 GPU (~1.6–3.5 CU/h).
  - Production SFT (T11): L4 preferred (4096 sequence length, 24 GB VRAM) or A100.
* **Authentication in Colab**:
  - Secure injection via `google.colab.userdata`:
    ```python
    from google.colab import userdata
    hf_token = userdata.get('HF_TOKEN')
    wandb_key = userdata.get('WANDB_API_KEY')
    ```
* **Nominal Checkpointing Protocol**:
  - Colab sessions cap at 12 hours (24 hours on Pro+).
  - The training loop checkpoints adapters directly to Hugging Face Hub every 30–60 minutes.
  - Every run logs start and end CU meter readings into `run.json`.

### 2.7 Liquid AI Architecture & Unsloth Framework
* **Model Class**: `LiquidAI/LFM2.5-2.6B` (`Lfm2ForCausalLM`).
* **Architectural Specifics**: Hybrid 1D-convolution and Grouped Query Attention (GQA).
* **LoRA Target Modules**: Explicit module names `["q_proj", "k_proj", "v_proj", "out_proj", "in_proj", "w1", "w2", "w3"]`.
* **Chat Template**: Native ChatML format executed via `tokenizer.apply_chat_template`.
  - System prompt matches inference serving character-for-character.
  - Strips leading BOS duplicate tokens.
* **Software Pins**:
  - `transformers==4.57.6`
  - `trl==0.22.2` (installed with `--no-deps` to avoid dependency conflicts)
  - `unsloth` latest / `unsloth-zoo` (pinned to stable Oct 2026 release)

---

## 3. Verification & Diagnostic Commands

Run these nominal checks from the repository root to verify connection health:

```bash
# 1. GitHub sync status
git status
git remote -v

# 2. Hugging Face authentication & target model inspection
python -c "from huggingface_hub import HfApi; api = HfApi(); print('HF User:', api.whoami()['name'])"

# 3. Agency Gateway model availability
python -c "import os, urllib.request, json; req = urllib.request.Request('https://gateway.yrka.io/v1/models', headers={'Authorization': f'Bearer {os.getenv(\"GATEWAY_API_KEY\")}'}); res = json.loads(urllib.request.urlopen(req).read()); print(f'Gateway models available: {len(res.get(\"data\", []))}')"

# 4. Weights & Biases connection
python -c "import wandb; print('W&B version:', wandb.__version__)"
```
