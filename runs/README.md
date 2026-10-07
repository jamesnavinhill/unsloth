# Run contract

Every training or eval run gets `runs/<run-id>/` with exactly three files (create all three at run start, before the GPU is touched):

```
runs/p2-1-sft-v1/
├── run.json        # config snapshot + CU meter readings + artifact links
├── metrics.jsonl   # append-only; one JSON object per line, as results land
└── notes.md        # human-readable log; one entry per milestone or incident
```

## run.json (minimum fields)

```json
{
  "run_id": "p2-1-sft-v1",
  "task": "T11",
  "started_utc": "2026-10-08T14:00:00Z",
  "surface": "colab",
  "gpu": "L4",
  "cu_meter": { "at_start": 187.5, "at_end": null },
  "config": { "base_model": "LiquidAI/LFM2.5-2.6B", "lora_r": 16, "lora_alpha": 32, "lora_dropout": 0.05,
               "lr": 1e-4, "scheduler": "cosine", "warmup_ratio": 0.03, "epochs": 2,
               "batch_eff": 16, "seq_len": 4096, "seed": 17, "pins": {"transformers": "4.57.6", "trl": "0.22.2"} },
  "data": { "dataset_repo": "jamesnavinhill/lfm25-humanizer-pairs-v1", "revision_sha": "...", "rows": 20000 },
  "artifacts": { "adapter": null, "merged": null, "gguf": null },
  "status": "running"
}
```

## metrics.jsonl discipline

- Append **during** the run (every eval step, every checkpoint push) — a session that dies mid-run still leaves its curve.
- One line per event: `{"t": "...Z", "kind": "train_loss|eval_loss|ckpt_push|cu_meter|probe", "value": {...}}`.
- Never rewrite history; corrections are new lines with `"kind": "correction"`.

## notes.md discipline

- One dated entry per milestone, incident, or decision. Failed attempts are recorded — they cost CU and they're findings.
- An error that fires twice identically = stop, record both attempts, mark the task BLOCKED (ORCHESTRATION.md rule 9).

## Canonical artifacts

Local `artifacts/` dirs are caches only (gitignored). Canonical home is HF Hub under `jamesnavinhill/lfm25-humanizer-*`; `run.json.artifacts` carries the repo/revision links. An upload counts only after the artifact is listed/read back.
