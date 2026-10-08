# HANDOFF — Next Session Guide

**Date**: 2026-10-08  
**Project**: Fine-Tuning `LiquidAI/LFM2.5-2.6B` into an Engineering Prose Reformatter & De-slopper  
**Status**: Phase 1 (Data Preparation) — Pivot to Conservative Surgical Reformatting  

---

## 1. Executive Summary & Objective

The objective is to fine-tune `LiquidAI/LFM2.5-2.6B` with 16-bit LoRA using Unsloth into an **In-Pipeline / API I/O Reformatter and De-slopper**.

### What the Model Does
When an agent or LLM finishes a coding task, its output often contains useful technical substance surrounded by synthetic chatbot clutter:
- **What to Strip**:
  - Conversational throat-clearing (*"Perfect! Now let me summarize what I've accomplished:"*, *"I have successfully implemented the fix..."*).
  - Repetitive boilerplate conclusions (*"The fix is minimal, focused, and maintains full backward compatibility..."*).
  - Emoji checklist spam (`🎯`, `🔧`, `✅`, `🧪`, `📊`, `🎉`).
- **What to PRESERVE 100% (Rule of Conservation of Technical Context)**:
  - **All code snippets and diffs** (never strip "Before" or "After" code blocks).
  - **All concrete reproduction examples** (e.g. `Period('2016-01-03') + 1` returning incorrect vs correct output).
  - **All file paths and line numbers**.
  - **Scannable test verification bullet points** (do not compress into dense semicolon run-on paragraphs).
- **Core Guideline**: If the input is good, **leave it alone**. Minor surgical edits only. Output must never become worse or lose information.

---

## 2. Hard Non-Negotiable Invariants

1. **100% FREE Models Only**:
   - Strictly use free NVIDIA NIM routes: `nv-moonshotai-kimi-k3` (primary) and `nv-nvidia-nemotron-3-ultra-550b-a55b` (fallback with retry wrapper).
   - **Never** call paid models (`ne-*`, `cf-*`, `gr-*`, or paid `or-*`).
2. **Official Authored Upstream Sampling Parameters Only**:
   - The LiteLLM gateway (`agency/config/litellm/config.yaml`) enforces `temperature: 1.0, top_p: 0.95` on NIM routes.
   - Client requests must pass strictly `model` and `messages`.
   - **Never** pass arbitrary client-side `temperature`, `top_p`, or `max_tokens`. Let generations stream naturally to stop tokens (`finish_reason: "stop"`).
3. **Docs Strictly in `docs/`**:
   - Keep the workspace root clean. All markdown docs live under `docs/`.
4. **Conservation of Technical Context**:
   - Never turn a structured PR summary into a dense, lossy prose paragraph. Follow `docs/ANTI_SLOP_SPEC.md` §3.

---

## 3. Current Workspace State & Verified Assets

- **Colab Smoke Test Verified**: `LiquidAI/LFM2.5-2.6B` trained with 16-bit LoRA in 62.86s, 5.35 GB peak VRAM on Tesla T4 (0.20 CU burned, 199.80 CU remaining).
- **Notebook Ready**: `notebooks/sft_lfm25_2_6b_v1.ipynb` with exact version pins (`transformers==4.57.6`, `trl==0.22.2 --no-deps`).
- **Raw Trace Pool**: `datasets/raw_candidates/assistant_done_10k.parquet` containing 10,000 real concluding agent responses ($\ge 500$ chars, filtered for coding traces).
- **Evaluation Benchmark**: `datasets/eval_10_clean_comparison.md` and `datasets/eval_10_clean.json` documenting the clean 10-sample evaluation.
- **Reference Specifications**:
  - `docs/ANTI_SLOP_SPEC.md` — Linguistic invariants and conservation rules.
  - `docs/plan.md` — Project execution plan v2.2.
  - `docs/STATE.md` — Real-time progress dashboard.
  - `docs/TASKS.md` — Task board and tracking.
  - `docs/CONNECTIONS.md` — Network and credentials topology.

---

## 4. Immediate Next Steps for Next Session (Task T9)

1. **Build `scripts/generate_training_pairs.py`**:
   - Use `nv-moonshotai-kimi-k3` via `gateway.yrka.io/v1`.
   - Payload: strictly `model` and `messages`.
   - System prompt: Conservative surgical reformatter instructing the model to:
     - Preserve all code blocks, diffs, line numbers, and input/output reproductions exactly.
     - Keep scannable headings and bullet points.
     - Strip conversational openings, boilerplate conclusions, and emojis.
     - If the text is already clean and technical, leave it unchanged.
2. **Run a 20-Pair Pilot & Inspect**:
   - Verify that 100% of code diffs and reproductions were preserved across all 20 pairs before scaling.
3. **Generate Full SFT Dataset**:
   - Process candidates into `datasets/sft_humanizer_train.parquet` and `datasets/sft_humanizer_val.parquet`.
4. **Execute Colab SFT Training (T11)**:
   - Run `notebooks/sft_lfm25_2_6b_v1.ipynb` on Google Colab (L4/T4).
