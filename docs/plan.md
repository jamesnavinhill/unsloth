# LFM2.5 Humanizer — Execution Plan v2 (target locked: LFM2.5-2.6B)

Date: 2026-10-07. Supersedes v1 (research synthesis). Companion files: `draft.md` (operator scratch), `ORCHESTRATION.md` (how work moves across surfaces), `TASKS.md` (live board), `STATE.md` (dashboard), `runs/` (run records), `datasets/LEDGER.md` (data provenance).

**What changed from v1**: model fork resolved — **LFM2.5-2.6B is the target** (image grounding not in scope). All "Option A/B/C/D" ambiguity is gone; remaining unknowns are explicit tasks in `TASKS.md`. Every task carries a fallback so a failed verification never stalls the project.

---

## 1. Locked decisions

| # | Decision | Rationale / source |
|---|---|---|
| D1 | **Model: `LiquidAI/LFM2.5-2.6B`** — dense text, 2.69B params, 131k ctx, 128k vocab, hybrid conv/GQA. Fallback ladder: (a) if Unsloth path fails in T1 → Liquid cookbook's official TRL/axolotl SFT; (b) only if both fail → `LFM2.5-VL-3B` (same backbone + vision tower, officially supported by Unsloth with vision frozen). | Same text backbone as VL-3B, 4× context, no vision complexity. [HF card](https://huggingface.co/LiquidAI/LFM2.5-2.6B), [Unsloth LFM2.5 tutorial](https://unsloth.ai/docs/models/tutorials/lfm2.5), [Liquid cookbook](https://github.com/Liquid4All/cookbook). Unsloth trainability verified in T1 smoke pass. |
| D2 | **Product: In-pipeline / API I/O Reformatter & De-slopper** across 2 engineering domains — Technical Documentation & Architecture Guides; Release Notes, Changelogs & PR Summaries. **Core Invariant: Conservation of Technical Context**: If output is good, leave it alone. Never drop code diffs, before/after examples, or test reproductions in favor of lossy text compression. Minor surgical edits only (strip AI throat-clearing, repetitive boilerplate, and emoji clutter). | Operator direction, 2026-10-08. Eliminates aggressive text loss and preserves developer utility. |
| D3 | **Architecture: one base + one domain-tagged humanizer LoRA.** Router deferred; per-domain adapters only if per-domain eval shows a domain lagging after v1. If/when needed, router = `LFM2.5-Encoder-230M/350M` or ModernBERT. | Naturalness lives in weights (shared); format lives in the prompt. No published evidence of cross-domain style interference at 1–3B; multi-task interference exists ("Cocktail Effect") but the prior run's own sweep showed the raw mixture beats careful balancing on the behavior axis that mattered. |
| D4 | **Training: Unsloth on Google Colab** (~200 CU/month). 16-bit LoRA. Config table §3. | Official notebooks; [Liquid docs: fine-tuning](https://docs.liquid.ai/lfm/fine-tuning/unsloth). |
| D5 | **Data: Conservative Reformatter Pairs (v2.2)**. Inputs = real LLM traces (SWE-Hero repository completions). Targets = free NIM models (`nv-moonshotai-kimi-k3` and `nv-nvidia-nemotron-3-ultra-550b-a55b`) executing non-aggressive surgical cleanups. Zero client-side temperature or top_p overrides (official upstream `temperature: 1.0, top_p: 0.95` enforced). Preserves code diffs, before/after reproductions, and line numbers 100%. Gated against information loss before SFT. | Operator direction, 2026-10-08. Prevents lossy compression while eliminating LLM slop. |

| D6 | **Uncensored: measure first, minimal intervention.** Fiction refusal probes (XSTest-style) run on base before any training; own-SFT is the first uncensoring step; Heretic post-merge only if probes still refuse. No classic abliteration pre-SFT. | [XSTest](https://arxiv.org/abs/2403.14387): over-refusal concentrates in safety-shaped prompts; [Heretic](https://github.com/p-e-w/heretic): KL-minimizing automated decensoring; ablation damage concentrates in math/reasoning, not prose. |
| D7 | **Eval: frozen before training, per-domain, greedy, matched base reruns, raw completions saved.** Metrics: LLM-judge naturalness + fact-fidelity + 5-gram copy-reuse + refusal rate + general-IF guard. Loss is not a ranking criterion. | Prior-run audit (val_loss pointed the wrong way at both ends; 13.5-pt template-mismatch gap) + [Liquid eval guidance](https://docs.liquid.ai/guides/use-case-evaluation). |
| D8 | **Orchestration: this repo is the single source of truth** (`STATE.md`/`TASKS.md`/`runs/`), protocol in `ORCHESTRATION.md`. Any surface (ZCode, VS Code, muse, Colab) reads before work and updates after. | Operator direction: bounce between surfaces, incremental results, fail-safe. |
| D9 | **License: LFM Open License v1.0** — fine-tuning + redistribution permitted, free commercial use <$10M revenue, license passthrough on derivatives. Public dataset pushes require license triage first (T4/T5). | [LFM license](https://www.liquid.ai/lfm-license). |

## 2. Budget

~200 compute units/month. Community-measured burn (verify in T1 — Google publishes no rates): T4 ≈ 1.6–2.0 CU/h, L4 ≈ 3.0–4.8 CU/h, A100 ≈ 8.5–11.8 CU/h. A full SFT v1 (20k pairs × ~1.5k tokens × 2 epochs ≈ 60M train tokens) ≈ 8–15 h ≈ **13–30 CU**. Sessions cap at 12 h (24 h Pro+) → checkpoint to HF Hub every 30–60 min, always resumable. Spending discipline (from prior run): smoke → calibrate throughput → resize the plan to the allowance, and log the CU meter reading at run start/end in `runs/<id>/run.json`.

## 3. Training config (v1 SFT)

| Setting | Value | Provenance |
|---|---|---|
| Base | `LiquidAI/LFM2.5-2.6B`, bf16, 16-bit LoRA | D1; Unsloth: 16-bit LoRA "slightly faster and slightly more accurate" than QLoRA; ~2.7B fits T4/L4 |
| LoRA r / alpha / dropout | **16 / 32 / 0** | Prior sweep validated r16/α32; dropout=0 required for Unsloth fast fused Triton kernels (measured in T1 smoke pass) |
| target_modules | `q_proj,k_proj,v_proj,out_proj,in_proj,w1,w2,w3` | LFM2.5 hybrid names (no gate/up/down); ≡ "all-linear"; explicit = deterministic. Source: official notebooks ([unslothai/notebooks LFM2.5](https://github.com/unslothai/notebooks/blob/main/python_scripts/LFM2.5_(1.2B)-Conversational.py), [Liquid cookbook script](https://github.com/Liquid4All/cookbook/blob/main/finetuning/scripts/unsloth-sft-lfm2.5.py)) |
| LR / scheduler | **1e-4, cosine, warmup_ratio 0.03** | Official 2e-4 w/ "reduce to 2e-5 for long runs"; 1e-4 validated by prior sweep; ratio-scaled warmup beats fixed 5 steps |
| Optimizer | adamw_8bit, weight_decay 0.01 | Official config |
| Batch | effective 16 (bs2×accum8 on T4; bs4×accum4 on L4) | Prior sweep; official uses 8 |
| Seq len | 4096 on L4 / 2048 on T4; chunk data to fit | Prior run measured truncation harm (targets live at the tail) |
| Loss masking | `train_on_responses_only` | Official; ~1% multi-turn gain per Unsloth guide |
| Packing | off | Official LFM2.5 setup |
| Epochs | 1–3, eval-gated | [Liquid docs](https://docs.liquid.ai/lfm/fine-tuning/overview): 500–5,000 task examples, quality>volume; tripwires below |
| Checkpointing | `use_gradient_checkpointing="unsloth"`; push adapters to HF Hub every 30–60 min | Prior run: silent stall + weights-only-at-end cost 4 GPU-h |
| Template | native LFM2.5 ChatML via `apply_chat_template`, no `get_chat_template`, strip leading BOS; train system prompt ≡ serving system prompt, character-for-character | Template-mismatch = 13.5-pt gap (prior run); [Liquid ADR-0001](https://github.com/Liquid4All/cookbook/blob/main/examples/voice-assistant/docs/adr/0001-eval-methodology.md) 100%→0% failure case |
| Tripwires | eval/train loss > 1.5 → overfit; train loss < 0.2 → overfit | Liquid cookbook script heuristic + Unsloth guide |
| Sampling (serve/eval) | temp 0.2, top_k 50 ([2.6B card](https://huggingface.co/LiquidAI/LFM2.5-2.6B)); eval runs greedy, frozen | Card + determinism discipline |
| Export | adapters + merged 16-bit + GGUF q4_k_m + q8_0; bake off vs Liquid's official QAT-Q4_0 line through llama.cpp b7075+ | Prior run: vendor QAT beat UD quant by 5.6 pts; runtime ≠ bits |
| Pins | latest `unsloth`/`unsloth-zoo` (≥ Oct 2026), `transformers==4.57.6` + `trl==0.22.2 --no-deps` (Unsloth pin) — one pin set per notebook, never mixed; seed fixed (17) | Known LFM2.5-VL bugs fixed Sep–Oct 2026: [unsloth#3938](https://github.com/unslothai/unsloth/issues/3938)/[unsloth-zoo#448](https://github.com/unslothai/unsloth-zoo/pull/448), [#11959](https://github.com/unslothai/unsloth/issues/11959) (VL-only, listed as fallback context) |

## 4. Phases

- **Phase 0 — verify & provision** (~2 CU + 30 min operator time): T1 Unsloth×2.6B verification notebook (tok/s, VRAM, CU burn), T3 HF token + Colab Secrets. Fallback ladder in D1.
- **Phase 1 — data** (~$0 CU, API $ only): zip triage/licensing (T4/T5), CC-bucket inventory (T6), draft-model selection + cost (T7), chunk/dedup/decontam pipeline (T8), draft generation (T9), eval suite frozen (T10).
- **Phase 2 — SFT v1 + eval** (~15–40 CU): T11 train per §3, T12 evaluate vs base (matched reruns, per-domain).
- **Phase 3 — iterate** (defined by T12 results): scale the failing axis only — more data for weak domains, DPO with fact-fidelity-filtered pairs, or one per-domain adapter. DPO reference config from prior-run notes: β=5.0, cosine 8e-7→8e-8, batch 2048 (Liquid's own preference-stage hyperparameters, [LFM2 tech report](https://arxiv.org/abs/2511.23404)).
- **Phase 4 — ship**: Heretic if refusals persist; GGUF bake-off; publish model + dataset with license attribution; text-only serving (no mmproj concept applies to VL fallback only).

## Change log

- 2026-10-07 — v2: plan rewritten; target locked to LFM2.5-2.6B (D1); decisions D1–D9.
- 2026-10-07 — v2.1: D5 amended per operator direction — inputs become **real LLM traces** (public trace datasets + agency gateway logs) rewritten into per-domain human style via style packs, with a retained reverse-task (human-target) slice. TASKS T7–T9 rewritten as draft; final data plan designed jointly in the data-plan session.
- 2026-10-08 — v2.2: D2/D5 refined to Conservative Reformatter & De-slopper across 2 engineering domains (Tech Docs and PR/Changelogs). Rule of Conservation of Technical Context established: no loss of code diffs, before/after examples, or structure. 100% free NIM models only, official upstream parameters (`temp: 1.0, top_p: 0.95`). All documentation strictly located under `docs/`.


## 5. Canonical sources

- Model: https://huggingface.co/LiquidAI/LFM2.5-2.6B · family: https://huggingface.co/LiquidAI
- License: https://www.liquid.ai/lfm-license
- Liquid fine-tuning docs: https://docs.liquid.ai/lfm/fine-tuning/overview · datasets: https://docs.liquid.ai/lfm/fine-tuning/datasets · Unsloth page: https://docs.liquid.ai/lfm/fine-tuning/unsloth · eval: https://docs.liquid.ai/guides/use-case-evaluation
- Liquid cookbook (official notebooks + scripts): https://github.com/Liquid4All/cookbook
- Unsloth: https://unsloth.ai/docs/models/tutorials/lfm2.5 · hyperparameter guide: https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide · GGUF export: https://unsloth.ai/docs/basics/inference-and-deployment/saving-to-gguf · notebooks repo: https://github.com/unslothai/notebooks
- Colab FAQ (limits, no published CU rates): https://research.google.com/colaboratory/faq.html · tiers: https://colab.research.google.com/signup
- llama.cpp (pin b7075+; LFM2.5 supported incl. tool-call parsing): https://github.com/ggml-org/llama.cpp
- Prior-art anchors: https://huggingface.co/jialinyyzz/humanizer · https://arxiv.org/abs/2407.10994 (Panza) · https://arxiv.org/abs/2410.16107 (PNAS style divergence) · https://arxiv.org/abs/2406.07016 (excess vocabulary) · https://github.com/p-e-w/heretic · https://arxiv.org/abs/2403.14387 (XSTest)
- Skills installed locally: `unsloth/.agents/skills/{hf-cli, huggingface-datasets, huggingface-llm-trainer}` — official Hugging Face skills, https://github.com/huggingface/skills
