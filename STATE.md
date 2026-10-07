# STATE — dashboard (the always-current answer to "where are we?")

Last updated: 2026-10-07 (UTC) — GitHub synced (`jamesnavinhill/unsloth`), nominal connections documented (`CONNECTIONS.md`), T2 DONE, T1 staged in `runs/p0-1-verify-unsloth-2.6b/`.

**Target**: `LiquidAI/LFM2.5-2.6B` (fallback: cookbook TRL path → VL-3B; decision D1 in `plan.md`)
**Phase**: 0 — verify & provision (T3 DONE, T2 DONE; T1 staged for Colab GPU execution)
**Next action**: Execute `notebooks/sft_lfm25_2_6b_v1.ipynb` on Google Colab (T4 or L4 GPU) to record measured tok/s, peak VRAM, and CU meter burn into `runs/p0-1-verify-unsloth-2.6b/run.json` (T1 completion). Then proceed to operator data session (T5–T9).

## CU budget ledger (200 CU/month, resets monthly)

| Date | Surface | GPU | Task | CU used | CU remaining | Note |
|---|---|---|---|---|---|---|
| 2026-10-07 | — | — | — | 0 | 200 | baseline |

## Active runs

- `p0-1-verify-unsloth-2.6b` (staged, ready for Colab execution).

## Blockers

None. (HF token and WANDB_API_KEY need to be present in Colab Secrets `HF_TOKEN` and `WANDB_API_KEY` before launching the Colab notebook).

## Recent results

- 2026-10-07 — GitHub sync complete: repository initialized on branch `main` and pushed to `https://github.com/jamesnavinhill/unsloth.git`. `.gitignore` verified airtight against secrets and bulky artifacts.
- 2026-10-07 — CONNECTIONS.md established: nominal, zero-workaround configurations and diagnostic script `scripts/verify_connections.py` verifying all 6 external integrations.
- 2026-10-07 — T2 DONE: production-grade training & smoke notebook created at `notebooks/sft_lfm25_2_6b_v1.ipynb` with exact version pins (`transformers==4.57.6`, `trl==0.22.2 --no-deps`), Colab Secrets integration, 16-bit LoRA target modules, response-only loss masking, D1 fallback ladder, and CU meter tracker.
- 2026-10-07 — T3 DONE: HF token verified (write role, reads both buckets); W&B personal + SA keys verified; agency gateway live (213 models); Kaggle token verified.
- 2026-10-07 — Buckets confirmed **public**: CommonCrawl-CC = 251.1 GB / 300 parquet files under `data/<crawl>/<lang>/`; cccc_all_domains = 393.1 GB / 653 files. Inventory (T4) unblocked.
