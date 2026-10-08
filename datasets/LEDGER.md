# Dataset ledger — provenance & license for everything that feeds training or eval

Rule (ORCHESTRATION.md fail-safe #4): **no corpus enters a training or eval mix without a ledger row**. Append rows; never delete (superseded rows get status `RETIRED`).

## Findings & Triage (2026-10-07 Kaggle & Zip Deep Audit)

`datasets/human_written_text/archive.zip` (2.37 GB zip / 6.35 GB uncompressed, Kaggle source: https://www.kaggle.com/datasets/youssefelebiary/human-written-text):

Provenance verified via Kaggle API: The dataset creator cleaned the text using a naive regex `(.*?[/])` that systematically stripped formatting and detached periods from words, corrupting the tokenization stream.

| Member | Uncompressed | True Provenance | Quality & Artifact Finding | Verdict |
|---|---|---|---|---|
| `CNN_DailyMail.csv` | 30.5 MB (7,001 rows) | CNN/DailyMail 3.0.0 news wire | **Severe tokenization artifacts**: Punctuation detached by regex (`"John and . Audrey Cook... monoxide . poisoning . "`). Tabloid wire register. Research-only license. | **REJECT / DROP** (Punctuation corruption + wrong register) |
| `Wikipedia.csv` | 29.8 MB (10,001 rows) | Wikipedia 2022 dump slice | Academic reference stubs (biographies, military units). First 3 rows byte-match `Human.csv`. | **REJECT / DROP** (Superseded by Human.csv; dry encyclopedia tone) |
| `Human.csv` | 2,117.4 MB | Wikipedia 2022 full dump | 2.1 GB of raw Wikipedia encyclopedia articles. Dry academic reference text; zero agent-to-human continuity or modern technical tone. CC-BY-SA license constraint. | **REJECT / DROP** (Fails Stripe/Linear target tone; CC-BY-SA burden) |
| `Shuffled_Human.csv` | 2,117.4 MB | Concatenated shuffle | Arbitrary shuffle concatenation of Gutenberg + Wikipedia + CNN/DM. Completely redundant duplicate. | **REJECT / DROP** (Redundant composite duplicate) |
| `Gutenberg.csv` | 2,057.1 MB (~3,000 books) | GutenDex API dump | Each CSV cell is an entire 80k-word book. Contains proofreader headers (`Proofreaders [Illustration]`), Victorian dialect, and mixed copyright notices (e.g. row 1 carries © 2001 Marie Lebert). | **CONDITIONAL / RESERVE** (Low utility; requires heavy chunking & boilerplate stripping) |

### Strategic Recommendation vs HF Buckets:
**Drop `archive.zip` from our core training pipeline.** It contains zero modern developer documentation, zero agent work updates, zero PR/changelog narrative, and its news slice is corrupted by detached punctuation.

The **HF Buckets** (`CommonCrawl-CreativeCommons-bucket` [251 GB] and `cccc_all_domains-bucket` [393 GB]) are modern, clean, well-tokenized, and carry genuine contemporary technical, marketing, and editorial human prose.

## Ledger

| ID | Source | Domain | License verdict | Status | Rows (post-gate) | Notes |
|---|---|---|---|---|---|---|
| SRC-001 | zip: Gutenberg.csv | short story | **MIXED** (PD + copyrighted donations) | RETIRED | 0 | Whole-book rows; proofreader artifacts; Victorian dialect |
| SRC-002 | zip: Human.csv / Wikipedia.csv | encyclopedia | **CC-BY-SA** | RETIRED | 0 | Dry reference text; fails modern continuity benchmark |
| SRC-003 | zip: CNN_DailyMail.csv | news | **NON-COMMERCIAL** | RETIRED | 0 | Detached punctuation corruption (`"word . "`) |
| SRC-004 | zip: Shuffled_Human.csv | composite | **MIXED** | RETIRED | 0 | Redundant shuffle composite of SRC-001/002/003 |
| SRC-005 | HF bucket CommonCrawl-CreativeCommons | blog / web copy / docs | **CC-LICENSED** | ACTIVE | TBD (T4) | Verified 2026-10-07: public, 251.1 GB / 300 parquets, modern web crawl |
| SRC-006 | HF bucket cccc_all_domains | technical / general | **CC-LICENSED** | ACTIVE | TBD (T4) | Verified 2026-10-07: public, 393.1 GB / 653 parquets |
| SRC-007 | HF bucket deepseek-v4-pro-0813-agentic-bucket | agentic execution | **RESEARCH/DERIVED** | ACTIVE | ~8,500+ | 19,072 train + 1,065 test trajectories; verifier-passed deepseek-v4-pro agent traces |
| SRC-008 | HF bucket k3-bucket | agentic tool use | **RESEARCH/DERIVED** | ACTIVE | ~540 | 544 trajectories of moonshotai/kimi-k3 terminal sessions |
| SRC-009 | HF bucket kernelbench-mega-traces-bucket | kernel & code optimization | **RESEARCH/DERIVED** | ACTIVE | ~130 | 133 frontier sessions (codex_gpt-5.5, claude-opus-4-8, glm-5.2, kimi, deepseek) |
| SRC-010 | HF bucket claude-fable-5-claude-code-bucket | CLI developer engineering | **PRIVATE/OPERATOR** | ACTIVE | 48 | 65 multi-turn interactive Claude Code CLI developer sessions |
| SRC-011 | HF bucket fable-5-premium-bucket | coding benchmarks | **PRIVATE/OPERATOR** | ACTIVE | 110 | Claude Fable-5 & Opus agent benchmark sessions (validation & test parquets) |
| SRC-012 | HF dataset nvidia/SWE-Hero-openhands-trajectories | software engineering agent | **CC-BY-4.0** | ACTIVE | 5,944 | 35k OpenHands SWE issue resolution traces; terminal `finish(message=...)` responses |
| RAW-001 | Trace Concluding DONE Pool (`assistant_done_10k`) | engineering / agent prose | **COMPOSITE** | COMPLETE | 10,000 | Strict $\ge 500$ char cutoff; 5,944 openhands, 3,011 deepseek-v4-pro, 831 kimi-k3, 108 claude-fable-5, 106 frontier/bench; median 1,828 chars, mean 1,827 chars; zero noise; written to `datasets/raw_candidates/assistant_done_10k.parquet` (10.1 MB) and `.jsonl` (23.1 MB) |
| GEN-001 | T9 reverse-task rewrites | all domains | Derived | IN PROGRESS | ~5k-10k | Inputs = RAW-001; targets = Stripe/Linear/Fly.io/Dan Luu rewrites generated via Gateway |

## Published artifacts

| Repo | Contents | License | Visibility |
|---|---|---|---|
| (none yet) | | | |

