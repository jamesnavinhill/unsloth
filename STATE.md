# STATE — dashboard (the always-current answer to "where are we?")

Last updated: 2026-10-07 (UTC) — credentials verified (T3 done); pre-data-plan setup complete.

**Target**: `LiquidAI/LFM2.5-2.6B` (fallback: cookbook TRL path → VL-3B; decision D1 in `plan.md`)
**Phase**: 0 — verify & provision (env/accounts DONE; GPU verification T1/T2 pending)
**Next action**: T1/T2 (Colab smoke-verify + notebook template) — agent work, ~2 CU. Then deeper data plan with operator (T5–T9 design, human-in-the-loop sourcing).

## CU budget ledger (200 CU/month, resets monthly)

| Date | Surface | GPU | Task | CU used | CU remaining | Note |
|---|---|---|---|---|---|---|
| 2026-10-07 | — | — | — | 0 | 200 | baseline |

## Active runs

None.

## Blockers

None. (Credentials all verified 2026-10-07; HF token still needs a one-time copy into Colab Secrets before the first GPU run.)

## Recent results

- 2026-10-07 — T3: HF token verified (write role, reads both buckets); W&B personal + SA keys verified (one invalid key removed); agency gateway live (213 models — draft generation will route through it); Kaggle token verified.
- 2026-10-07 — Buckets confirmed **public**: CommonCrawl-CC = 251.1 GB / 300 parquet files under `data/<crawl>/<lang>/`; cccc_all_domains = 393.1 GB / 653 files. Inventory (T4) unblocked.
