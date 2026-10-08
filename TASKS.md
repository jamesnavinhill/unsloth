# TASKS — LFM2.5-2.6B humanizer

Statuses: `TODO` / `IN PROGRESS (surface, date)` / `BLOCKED (reason)` / `DONE (date)` / `CANCELLED`. Claim before working; close out even on failure. Rules: `ORCHESTRATION.md`. Fallbacks are part of each task — never stall on a failed verification.

## Phase 0 — verify & provision

**T1 · Verify Unsloth trains LFM2.5-2.6B** — `DONE (2026-10-07)`
Colab Tesla T4. Loaded `LiquidAI/LFM2.5-2.6B` with `FastLanguageModel.from_pretrained(max_seq_length=4096)`, attached 16-bit LoRA config (20,135,936 trainable params / 0.741%), ran 10-step smoke train from in-notebook dataset.
- DoD: smoke train completed in 62.86s; peak VRAM 5.35 GB; 0.20 CU burned (0.67 CU/h); monotonic loss convergence (3.41 → 1.06); verdict GO recorded in `runs/p0-1-verify-unsloth-2.6b/notes.md`. Fallback ladder not needed.
- Source: [W&B run record](https://wandb.ai/navin_hill/huggingface/runs/huxz5tt6).

**T2 · Pin versions + notebook template** — `DONE (2026-10-07)` (pairs with T1)
Created `notebooks/sft_lfm25_2_6b_v1.ipynb` from the official notebook/script: pinned installs (`unsloth` latest, `transformers==4.57.6`, `trl==0.22.2 --no-deps`), Colab Secret usage (`HF_TOKEN` via `userdata`), the full §3 config, checkpoint-to-HF-Hub every 30–60 min, CU-meter logging helper, smoke mode flag.
- DoD: notebook in repo, runs end-to-end in smoke mode on Colab.
- Source: [official Conversational notebook](https://github.com/unslothai/notebooks/blob/main/python_scripts/LFM2.5_(1.2B)-Conversational.py), adapted per D1.

**T3 · Provision credentials** — `DONE (2026-10-07)`
All credentials verified live and recorded in `.env`:
- `HF_TOKEN` — verified via whoami-v2: user `jamesnavinhill`, fine-grained **write** role, token name "unsloth". Reads both HF Buckets. **Still needs adding to Colab Secrets** (Runtime ▸ Secrets, name `HF_TOKEN`) before the first training run.
- W&B — personal key verified via GraphQL viewer (account `jamienavinhill`); service-account key also valid (no user identity), kept as `WANDB_SA_API_KEY`; a third supplied key was invalid ("auth token too short") and was removed. Entity `navin_hill`, project `copyright` (operator's existing project — as set by operator).
- Agency gateway — `gateway.yrka.io/v1` verified: 213 models listed. Draft-generation (T9) + judge evals (T10/T12) route through it; no OpenAI/OpenRouter key needed.
- Kaggle — `KGAT_` token verified via basic auth (`username:token`) on api.kaggle.com/v1; no `~/.kaggle` file required.

**T4 · HF bucket inventory** — `DONE (2026-10-07)`
Audited all 46 storage buckets under `jamesnavinhill` via `HfApi` native bucket tree APIs. Key discovery: 4 active trace repositories containing frontier agent & developer logs:
- `jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket` (20,137 trajectories of verified deepseek-v4-pro tool & dialogue execution)
- `jamesnavinhill/k3-bucket` (544 trajectories of moonshotai/kimi-k3 terminal sessions)
- `jamesnavinhill/kernelbench-mega-traces-bucket` (133 multi-turn sessions across codex_gpt-5.5, claude-opus-4-8, glm-5.2, kimi-k2.7-code, gemini-3.5-flash)
- `jamesnavinhill/claude-fable-5-claude-code-bucket` (65 multi-turn interactive Claude Code CLI developer traces)
- DoD: Full inventory completed; buckets cataloged in `datasets/LEDGER.md`.

## Phase 1 — data

**T5 · Zip triage + licensing** — `DONE (2026-10-07)`
Audited `archive.zip` via streaming inspect + Kaggle API (`youssefelebiary/human-written-text`). Finding: CNN/DM is corrupted by naive regex cleaning (detached punctuation `"word . "`); Wikipedia is dry reference stubs; Shuffled is an identical duplicate; Gutenberg is raw 80k-word Victorian books with mixed copyright.
- DoD: All 5 members audited, provenance documented, verdicts recorded in `datasets/LEDGER.md`. Strategic verdict: **RETIRE archive.zip**; anchor dataset sourcing on modern HF Buckets (T4/T6) and Agency Gateway traces.

**T6 · 10k Concluding Assistant "DONE" Trace Extraction** — `DONE (2026-10-07)`
Extracted concluding, meaty assistant responses from multi-turn traces across 4 active buckets (`deepseek-v4-pro`, `k3-bucket`, `kernelbench-mega-traces`, `claude-fable-5`). Assembled exactly **10,000 unique candidate responses** ($\ge 120$ chars, text-only, non-error): 9,437 deepseek-v4-pro, 438 moonshotai/kimi-k3, 60 claude-fable-5, 65 kernelbench frontier models (codex, claude-opus, glm, grok, etc.).
- DoD: Executed `scripts/extract_trace_responses.py`; produced `datasets/raw_candidates/assistant_done_10k.jsonl` (10.55 MB), companion `.parquet` (4.16 MB), and `extraction_report.json`. Verified in `datasets/LEDGER.md`.

**T7 · Rewriter model + trace sources** — `TODO` (v2 draft per D5; finalize in data-plan session)
Two picks, both routed through the **agency gateway** (verified live, 213 models):
1. *Rewriter LLM* — converts trace responses into per-domain human style. Candidates: `or-nvidia-nemotron-3-ultra-550b`, `or-nvidia-nemotron-3-super-120b`, `or-free`, `ne-gpt-oss-120b`, `cf-*` pool. Also notable: `or-liquid-lfm-2.5-2.6b` (target model servable — inference baselines without local downloads).
2. *Trace sources* (the INPUT side = real LLM outputs): (a) public prompt/response datasets — candidates: WildChat-class, LMSYS-class, Nemotron/Tulu-class post-training mixtures; **license verified per dataset before selection** (some are research-only); (b) **agency gateway's own LiteLLM logs** (Postgres per vault `agency`) — production-faithful traces from real use; privacy/licensing review required before training on them.
- DoD: rewriter chosen (with a small-sample A/B on 20 rewrites against the style-pack rubric); trace sources shortlisted with license verdicts in `datasets/LEDGER.md`.
- Sources: method provenance [jialinyyzz/humanizer](https://huggingface.co/jialinyyzz/humanizer), [Panza](https://arxiv.org/abs/2407.10994).

**T8 · Style packs + trace curation** — `IN PROGRESS (agent, 2026-10-07)`
Per domain (Tech Docs, Changelogs, Engineering Lore, Creative Narrative): curated human **style pack** = exemplar passages + style spec + banned clichés lexicon. Roster locked: Stripe, Linear, Fly.io, Plaid, Render, Docker, PostHog (core team), Joel on Software, Dan Luu, Travis Downs, Julia Evans (jvns), Simon Willison, The Pragmatic Engineer, The Daily WTF.
- DoD: 4 style packs reviewed by operator (this is the human-judgment-heavy step); trace pool gated in ledger.

**T9 · Rewrite-at-scale + gates** — `TODO` (v2 draft; needs T7/T8)
Batch rewrite trace responses into domain style grounded on the style packs; run quality gates per pair: fact-fidelity judge, naturalness judge, 5-gram copy-reuse ceiling, refusal check; failures → regenerate once, then drop. Also produce the reverse-task slice (human text as targets) as a mix anchor (~30–50% of pairs, ratio set in data-plan session). Publish gated pairs to HF (private until licensing clears).
- DoD: ~20k+ gated pairs published; ledger rows; 50-pair spot check reviewed by operator.

**T10 · Eval suite v1 (frozen before any training)** — `TODO` (parallel with T8)
Build and freeze: (a) per-domain rewrite probes (30+/domain, held-out human passages never in training); (b) fiction refusal probes (XSTest-style, ~50 items); (c) general-IF guard set; (d) LLM-judge rubric for naturalness + fact-fidelity + 5-gram copy-reuse. Publish to HF (private), record hashes in the ledger.
- DoD: eval sets frozen + hashes recorded; judge rubric documented in `runs/` template.
- Sources: [XSTest](https://arxiv.org/abs/2403.14387) for over-refusal probe design; [Liquid eval guidance](https://docs.liquid.ai/guides/use-case-evaluation).

## Phase 2 — SFT v1 + eval

**T11 · SFT v1 run** — `TODO` (needs T1/T2/T9/T10)
Full run per `plan.md` §3 on the best affordable GPU (L4 preferred for 4096 ctx). Run contract: `runs/p2-1-sft-v1/`. Tripwires active (eval/train >1.5, train loss <0.2). Checkpoint to HF Hub every 30–60 min.
- DoD: trained adapter + merged model on HF Hub; metrics.jsonl complete; CU spent logged.

**T12 · Eval v1 vs base** — `TODO` (needs T11)
Matched reruns: base vs tuned, greedy, same template, per-domain stratification, plus refusal probes and general-IF guard. Raw completions saved before scoring. Verdict per domain: pass / needs-iteration.
- DoD: `runs/p2-1-sft-v1/notes.md` carries the verdict table; STATE.md next-action set from it.

## Phase 3 — iterate (defined by T12 results)

**T13 · Iteration round(s)** — `TODO` (defined later)
Choose per results: more data for weak domains (T6/T8/T9 rerun), DPO with fact-fidelity-filtered pairs (reference config: β=5.0, cosine 8e-7→8e-8, batch 2048 — Liquid's own preference-stage hyperparameters from the [LFM2 tech report](https://arxiv.org/abs/2511.23404)), or one per-domain adapter (D3 contingency).

## Phase 4 — ship

**T14 · Uncensor pass (conditional)** — `TODO`
If T12 refusal probes show refusals: run [Heretic](https://github.com/p-e-w/heretic) on the merged model; re-run full eval incl. prose-quality judge before/after. If no refusals: record that and skip.
- DoD: refusal-rate table (base / SFT / post-Heretic) or a documented skip.

**T15 · Quantization bake-off + publish** — `TODO`
Export GGUF q4_k_m + q8_0 from the merged model; compare against Liquid's official QAT-Q4_0 line through llama.cpp (b7075+) on the eval suite (runtime ≠ bits — test both through the same runtime). Publish winners + dataset with license attribution.
- DoD: quant comparison table; public repos live; ledger finalized.

## History

| Date | Event |
|---|---|
| 2026-10-07 | Board created; plan v2 locked (D1–D9); T3 blocked on operator credentials; T1/T2 next. |
| 2026-10-07 | T3 DONE: HF token (write role) / W&B (personal + SA keys) / agency gateway / Kaggle all verified live. T4 unblocked (buckets public: CC=251GB/300 files, cccc=393GB/653 files). T7 rerouted to agency gateway. |
| 2026-10-07 | Repo initialized & synced to GitHub (jamesnavinhill/unsloth); CONNECTIONS.md created; T2 DONE (notebooks/sft_lfm25_2_6b_v1.ipynb pinned & ready); T1 IN PROGRESS (runs/p0-1-verify-unsloth-2.6b/ staged). |
