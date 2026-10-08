# STATE — dashboard (the always-current answer to "where are we?")

Last updated: 2026-10-08 (UTC) — Phase 0 COMPLETE; Phase 1 IN PROGRESS.
- T1–T6, T8 DONE.
- T7 Clean Evaluation DONE (10/10 samples evaluated using official upstream NIM defaults).
- Key Pivot: Analysis revealed that aggressive rewriters degrade engineering quality by stripping code diffs, before/after examples, and scannable test structures. Target SFT model is an in-pipeline / API I/O surgical reformatter & de-slopper (preserves technical context 100%, strips AI conversational boilerplate and emojis).

**Target**: `LiquidAI/LFM2.5-2.6B` (**VERIFIED**: native 16-bit LoRA on Unsloth confirmed, 20.1M params, peak VRAM 5.35 GB)
**Phase**: 1 — data (T7 complete; T9 conservative training pair generation next)
**Next action**: Implement `scripts/generate_training_pairs.py` using conservative surgical cleanup prompts (preserving diffs/code/reproductions 100%, stripping emojis/throat-clearing/boilerplate), validate on a sample batch, and generate the SFT dataset for Colab.

## CU budget ledger (200 CU/month, resets monthly)

| Date | Surface | GPU | Task | CU used | CU remaining | Note |
|---|---|---|---|---|---|---|
| 2026-10-07 | — | — | — | 0 | 200 | baseline |
| 2026-10-07 | Colab | T4 | T1 | 0.20 | 199.80 | Smoke verification (10 steps, 62.86s, 5.35GB VRAM) |

## Active runs

None. (Run `p0-1-verify-unsloth-2.6b` completed and archived).

## Blockers

None.

## Recent results

- 2026-10-08 — T7 DONE: 10-sample clean evaluation executed using official upstream gateway parameters (`temperature: 1.0, top_p: 0.95`, no client-side overrides) across SWE-Hero completions. Full outputs saved to `datasets/eval_10_clean_comparison.md`. Analysis confirmed that aggressive rewriters over-compress and strip high-value diffs/examples; established the **Conservation of Context** rule in `docs/ANTI_SLOP_SPEC.md`.
- 2026-10-08 — Sampling Knobs Purged: Eliminated all hardcoded client-side temperatures (`0.3`/`0.2`), arbitrary character truncations (`MAX_CHAR_LEN = 6000`), and display slicing across scripts and notebooks.
- 2026-10-08 — Documentation Standardized: All project documentation strictly consolidated under `docs/` (`docs/plan.md`, `docs/STATE.md`, `docs/TASKS.md`, `docs/CONNECTIONS.md`, `docs/ORCHESTRATION.md`, `docs/ANTI_SLOP_SPEC.md`). Root kept clean.
- 2026-10-07 — T6 DONE: 10,000 raw concluding assistant "DONE" responses extracted with strict $\ge 500$ character cutoff (median 1,828 chars, mean 1,827 chars) across OpenHands SWE-Hero (5,944), DeepSeek V4 Pro (3,011), Moonshot Kimi K3 (831), Claude Fable-5 (108), and KernelBench frontier models (106). Written to `datasets/raw_candidates/assistant_done_10k.parquet` (10.1 MB).
- 2026-10-07 — T8 DONE: Style Exemplar Library harvested across all 14 requested sources (34 authentic markdown documents) in `references/style_exemplars/`.
- 2026-10-07 — T2 DONE: production-grade training notebook created at `notebooks/sft_lfm25_2_6b_v1.ipynb` with exact version pins.
- 2026-10-07 — T1 DONE: Colab Tesla T4 smoke verification completed (10 steps, 62.86s, 5.35GB peak VRAM, 0.20 CU).

