# ORCHESTRATION — how this project moves across surfaces

This directory (`labwork/unsloth/`) is the **single source of truth** for the LFM2.5-2.6B humanizer project. Work happens on several surfaces — ZCode (here), VS Code, muse, Google Colab, Kaggle — and any agent or human must be able to sit down at any of them and continue correctly.

## File map (who owns what)

| File | Role | Update rule |
|---|---|---|
| `plan.md` | Execution plan v2: locked decisions D1–D9, config table, phases, canonical sources | Changes only when a *decision* changes; append a dated note to the change log |
| `TASKS.md` | Live task board (the project's work queue) | Update the touched task's status + note on every session that touches it |
| `STATE.md` | Dashboard: current phase, CU budget ledger, active runs, blockers, next action | Updated at the **end of every working session**, and whenever a run starts/ends |
| `runs/<run-id>/` | One folder per training/eval run; `run.json` (config snapshot + CU meter readings), `metrics.jsonl` (append-only), `notes.md` (operator/agent log) | Created by `runs/README.md` contract; metrics appended incrementally **during** runs, not after |
| `datasets/LEDGER.md` | Provenance/license ledger for every corpus and generated dataset | Append an entry before any new corpus is used in training |
| `.env` | Local secrets (gitignored) | Colab uses Colab Secrets with the same key names — keep both in sync |
| `draft.md` | Operator scratch — never edited by agents |

## Session protocol (every surface, every agent)

1. **Read** `STATE.md`, then the `TASKS.md` rows for anything marked `IN PROGRESS` or the next `TODO` you intend to take.
2. **Claim** the task: set its row to `IN PROGRESS (surface, date)` before doing the work. One claimant per task.
3. **Work** under the run contract (`runs/README.md`) if the task produces a run. Smoke-test before anything expensive; assert before you trust (token counts, upload receipts, template equality — see fail-safe rules below).
4. **Post incrementally**: append to `runs/<id>/metrics.jsonl` as results land; push checkpoints/adapters to HF Hub on the cadence in the run contract. A session that dies must leave recoverable state.
5. **Close out**: update the task row (`DONE`/`BLOCKED`+reason), append results summary to the run's `notes.md`, update `STATE.md` (phase, CU ledger if GPU was spent, next action). Do this **even if the session failed** — a failed session that records itself cost data; one that doesn't wastes it.

## Fail-safe rules (non-negotiable — each traces to a real prior failure)

1. **Smoke → calibrate → resize.** No full run without a 10-sample smoke pass and a measured tok/s on the actual GPU. Resize the plan to measured throughput, never spec sheets. *(prior run: throughput assumption off by 50%)*
2. **Checkpoint to resumable storage every 30–60 min** (HF Hub or Drive), and verify the upload (read it back / list it). A run's outputs don't exist until the artifact listing shows them. *(prior run: weights-only-at-end cost 4 GPU-h; silent rc=0 upload failures)*
3. **Log the Colab CU meter reading** at run start and end into `run.json`. Budget truth lives in `STATE.md`. *(you can't manage 200 CU/mo you don't measure)*
4. **Data gates before training.** A dataset that failed a gate (license, dedup, decontamination, schema) never enters a training mix. Dedup on full content, not prompts. *(prior run: training on filter-rejected data actively hurt)*
5. **Template equality assert**: training system prompt ≡ serving system prompt, character-for-character, native `apply_chat_template` only, no double-BOS. *(13.5-point gap on the prior run's own checkpoint)*
6. **Save raw completions before scoring.** A grading bug then costs a re-score, not a regeneration. Eval decoding = greedy, frozen, byte-reproducible.
7. **Loss is not a verdict.** Rankings come from paired per-item task metrics with the base model rerun under identical conditions, per domain. *(prior run: three arms within 0.0006 nats; loss pointed the wrong way)*
8. **One pin set per notebook** (transformers/trl/unsloth versions). Mismatched pins are the first suspect when a load error appears.
9. **Escalate, don't improvise**: if a cell errors twice for the same reason, stop, write the error + 2 attempts into `notes.md`, mark the task `BLOCKED`. *(prior run: an untested one-line fix produced the same TypeError twice)*

## Surfaces

| Surface | Does | Credentials |
|---|---|---|
| **ZCode (this repo)** | Orchestration, data prep, eval harness, analysis, docs, dataset uploads to HF | `.env` here |
| **Google Colab** | All GPU training + GPU eval; notebooks in `notebooks/` | Colab Secrets: `HF_TOKEN` (+ optional `WANDB_API_KEY`) — add via Runtime ▸ Secrets; session caps 12 h (24 h Pro+) |
| **VS Code / muse / other agents** | Same rules as this file; claim tasks in `TASKS.md`, write into this repo, never fork the state elsewhere | `.env` here (or the surface's equivalent); no parallel claimants on one task |
| **Hugging Face Hub** | Canonical artifact home: datasets, adapters, merged models, GGUFs under `jamesnavinhill/...` | `HF_TOKEN` (write), buckets listed in `.env` |
| **Kaggle** | Dataset provenance checks (T5) | `KAGGLE_USERNAME/KAGGLE_KEY` or browser |

## Keeping tabs (operator)

- Open `STATE.md` — it is always the current answer to "where are we, what's next, what's blocked".
- `TASKS.md` rows carry per-task history in their Notes column.
- Incremental run results: `runs/<id>/metrics.jsonl` (append-only) + a human-readable line in `notes.md` per milestone. Nothing waits for a session to end to become visible.
- CU spend is a running table in `STATE.md`; every GPU session adds a row.

## Conventions

- Run IDs: `<phase><seq>-<slug>` (e.g., `p0-1-verify-unsloth-2.6b`, `p2-1-sft-v1`).
- All timestamps UTC, ISO-8601.
- Task IDs: `T<nn>` — stable forever; new tasks take the next number, cancelled tasks stay listed as `CANCELLED` (never deleted).
- Artifacts on HF follow `jamesnavinhill/lfm25-humanizer-*` naming.
