# Dataset ledger — provenance & license for everything that feeds training or eval

Rule (ORCHESTRATION.md fail-safe #4): **no corpus enters a training or eval mix without a ledger row**. Append rows; never delete (superseded rows get status `RETIRED`).

## Known findings (from 2026-10-07 zip inspection)

`datasets/human_written_text/archive.zip` (2.3 GB zip / 6.35 GB uncompressed, Kaggle source: https://www.kaggle.com/datasets/youssefelebiary/human-written-text):

| Member | Size | Finding |
|---|---|---|
| `Gutenberg.csv` | 2.06 GB | Mixed public-domain **and** copyrighted supplementary items (first row = © 2001 interview collection); multilingual (EN/FR/ES observed) |
| `Human.csv` | 2.12 GB | Wikipedia-derived (first row byte-matches `Wikipedia.csv`) |
| `Shuffled_Human.csv` | 2.12 GB | Same content as `Human.csv`, shuffled order (same size, different CRC) — **duplicate, drop** |
| `Wikipedia.csv` | 30 MB | Wikipedia; `Human.csv` appears to be its superset |
| `CNN_DailyMail.csv` | 30 MB | Wire news with tokenization artifacts ("Maureen . They were found . ") |

Coverage vs targets: story ✔ (Gutenberg, needs modern-style filter), docs ✔ (Wikipedia), news→blog △ (CNN/DM), **modern blog/casual web copy ✘** → must come from CC buckets (T6).

## Ledger

| ID | Source | Domain | License verdict | Status | Rows (post-gate) | Notes |
|---|---|---|---|---|---|---|
| SRC-001 | zip: Gutenberg.csv | short story | **TBD** (T5: mixed PD/copyright, multilingual) | TRIAGE | — | boilerplate strip needed; language filter EN |
| SRC-002 | zip: Human.csv / Wikipedia.csv | documentation | **TBD** (T5: Wikipedia = CC-BY-SA w/ attribution) | TRIAGE | — | verify Human.csv ⊇ Wikipedia.csv; provenance research on Kaggle page |
| SRC-003 | zip: CNN_DailyMail.csv | news/blog input | **TBD** (T5: research-licensed — likely keep out of public sets) | TRIAGE | — | tokenization artifacts need cleanup |
| SRC-004 | HF bucket CommonCrawl-CreativeCommons | blog / web copy | **TBD** (CC-crawl derived; operator-staged CC-licensed content — confirm license filter used at build time) | TRIAGE | — | verified 2026-10-07: public bucket, 251.1 GB / 300 files, layout `data/<CC-crawl>/<lang>/*.parquet` (multilingual: afr, deu, … seen), README.md + counts.json at root. Inventory via `hf` CLI (buckets don't serve `resolve/` URLs) |
| SRC-005 | HF bucket cccc_all_domains | TBD | **TBD** (T4) | TRIAGE | — | verified 2026-10-07: public bucket, 393.1 GB / 653 files |
| GEN-001 | T9 reverse-task drafts (big model) | all four | Derived — draft side is machine-generated; human side inherits source license | PLANNED | target ~20k | model choice + cost in T7 |

## Published artifacts

| Repo | Contents | License | Visibility |
|---|---|---|---|
| (none yet) | | | |
