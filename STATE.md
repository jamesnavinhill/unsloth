# STATE — dashboard (the always-current answer to "where are we?")

Last updated: 2026-10-07 (UTC) — Phase 0 COMPLETE: T1 verified (Unsloth × LFM2.5-2.6B on Tesla T4), T2 notebook template done, T3 credentials live, repo synced to GitHub.

**Target**: `LiquidAI/LFM2.5-2.6B` (**VERIFIED**: native 16-bit LoRA on Unsloth confirmed, 20.1M params, peak VRAM 5.35 GB)
**Phase**: 1 — data (T4 HF Bucket inventory DONE; T5 archive triage DONE; T6 10k assistant DONE extraction DONE; T8 style pack curation underway)
**Next action**: Curate seed style packs for the 3 target domains (T8: Stripe/Linear/Plaid/Render/Docker docs & changelogs, Fly.io & tech lore blogs) and configure the Gateway rewriter + judge gates (T7/T9).

## CU budget ledger (200 CU/month, resets monthly)

| Date | Surface | GPU | Task | CU used | CU remaining | Note |
|---|---|---|---|---|---|---|
| 2026-10-07 | — | — | — | 0 | 200 | baseline |
| 2026-10-07 | Colab | T4 | T1 | 0.20 | 199.80 | Smoke verification (10 steps, 62.86s, 5.35GB VRAM) |

## Active runs

None. (Run `p0-1-verify-unsloth-2.6b` completed and archived).

## Blockers

None. Phase 0 fully verified.

## Recent results

- 2026-10-07 — T6 DONE: 10,000 raw concluding assistant "DONE" responses extracted across user HF buckets (`deepseek-v4-pro`: 9,437, `kimi-k3`: 438, `kernelbench`: 65, `claude-code`: 60). Written to `datasets/raw_candidates/assistant_done_10k.jsonl` (10.55 MB) and companion `.parquet` (4.16 MB).
- 2026-10-07 — T4 DONE: Full HF bucket inventory completed; 4 active trace repositories identified and integrated via native `HfApi` bucket tree APIs.
- 2026-10-07 — DATA_SPEC.md & LEDGER.md updated: Fly.io added to style roster alongside Stripe, Linear, Plaid, Render, Docker, PostHog, Joel on Software, Dan Luu, Julia Evans; trace extraction specs codified.

- 2026-10-07 — GitHub sync complete: repository initialized on branch `main` and pushed to `https://github.com/jamesnavinhill/unsloth.git`. `.gitignore` verified airtight against secrets and bulky artifacts.
- 2026-10-07 — CONNECTIONS.md established: nominal, zero-workaround configurations and diagnostic script `scripts/verify_connections.py` verifying all 6 external integrations.
- 2026-10-07 — T2 DONE: production-grade training & smoke notebook created at `notebooks/sft_lfm25_2_6b_v1.ipynb` with exact version pins (`transformers==4.57.6`, `trl==0.22.2 --no-deps`), Colab Secrets integration, 16-bit LoRA target modules, response-only loss masking, D1 fallback ladder, and CU meter tracker.
- 2026-10-07 — T3 DONE: HF token verified (write role, reads both buckets); W&B personal + SA keys verified; agency gateway live (213 models); Kaggle token verified.
- 2026-10-07 — Buckets confirmed **public**: CommonCrawl-CC = 251.1 GB / 300 parquet files under `data/<crawl>/<lang>/`; cccc_all_domains = 393.1 GB / 653 files. Inventory (T4) unblocked.
