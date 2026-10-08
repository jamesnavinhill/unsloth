#!/usr/bin/env python3
"""
Trace Concluding "DONE" Response Extraction Pipeline
Extracts ~10,000 concluding assistant responses from multi-turn traces across:
  1. jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket (deepseek-v4-pro)
  2. jamesnavinhill/k3-bucket (moonshotai/kimi-k3)
  3. jamesnavinhill/kernelbench-mega-traces-bucket (codex_gpt-5.5, claude-opus-4-8, glm-5.2, etc.)
  4. jamesnavinhill/claude-fable-5-claude-code-bucket (claude-code / fable-5)

Output:
  - datasets/raw_candidates/assistant_done_10k.jsonl
  - datasets/raw_candidates/assistant_done_10k.parquet
  - datasets/raw_candidates/extraction_report.json
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd
from huggingface_hub import HfApi

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT_DIR / "datasets" / ".cache"
OUTPUT_DIR = ROOT_DIR / "datasets" / "raw_candidates"
ENV_PATH = ROOT_DIR / ".env"

MIN_CHAR_LEN = 500
TARGET_TOTAL = 10000

def load_env() -> Dict[str, str]:
    env = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip("'\"")
    return env

def compute_hash(text: str) -> str:
    norm = " ".join(text.lower().split())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()

def is_valid_prose(text: str) -> bool:
    """Filter out single-line confirmations, pure code blocks, raw JSON schemas, and synthetic harness loops."""
    stripped = text.strip()
    if len(stripped) < MIN_CHAR_LEN:
        return False
    
    # Reject raw JSON / dict dumps
    if stripped.startswith("{") or stripped.startswith("["):
        return False
    
    # Reject synthetic file-counting harness loops
    if "item=count" in stripped or "out/total.txt" in stripped:
        return False

    # Reject known API error messages
    error_markers = [
        "session limit",
        "rate limit",
        "hit your session limit",
        "context length exceeded",
        "server error",
        "internal server error",
        "request timed out"
    ]
    lower = stripped.lower()
    for em in error_markers:
        if em in lower and len(stripped) < 700:
            return False
    return True

# -----------------------------------------------------------------------------
# Bucket 1: DeepSeek V4 Pro Agentic Traces
# -----------------------------------------------------------------------------
def extract_deepseek_traces(api: HfApi, max_needed: int) -> List[Dict[str, Any]]:
    bucket_id = "jamesnavinhill/deepseek-v4-pro-0813-agentic-bucket"
    target_dir = CACHE_DIR / "deepseek"
    target_dir.mkdir(parents=True, exist_ok=True)
    train_parquet = target_dir / "train-00000-of-00001.parquet"
    test_parquet = target_dir / "test-00000-of-00001.parquet"

    # Download if not present
    files_to_dl = []
    if not train_parquet.exists():
        files_to_dl.append(("canonical/train-00000-of-00001.parquet", train_parquet))
    if not test_parquet.exists():
        files_to_dl.append(("canonical/test-00000-of-00001.parquet", test_parquet))
    
    if files_to_dl:
        print(f"[*] Downloading {len(files_to_dl)} parquets from {bucket_id}...")
        api.download_bucket_files(bucket_id, files_to_dl)

    candidates = []
    seen_hashes = set()

    for p_path in [test_parquet, train_parquet]:
        if not p_path.exists():
            continue
        print(f"[*] Parsing {p_path.name}...")
        df = pd.read_parquet(p_path)
        # Prioritize successful trajectories and drop non-English / raw schema tasks
        task_filter = (
            (df["task_type"] != "ds4-structured_outputs") &
            (df["task_type"] != "ds4-multilingual_multi_turn") &
            (df["task_type"] != "ds4-memory_context_management") &
            (df["task_type"] != "ds4-verifiable_math") &
            (df["task_type"] != "ds4-science_verifiable")
        )
        success_mask = ((df["disposition"] == "traj_success") | (df["verifier_passed"] == True)) & task_filter
        df_success = df[success_mask] if success_mask.any() else df[task_filter]

        for _, row in df_success.iterrows():
            msgs = row.get("messages")
            if isinstance(msgs, (list, tuple)) or hasattr(msgs, "__iter__"):
                msgs = list(msgs)
            else:
                continue
            
            # Find the final assistant message
            asst_msgs = [m for m in msgs if isinstance(m, dict) and m.get("role") == "assistant"]
            if not asst_msgs:
                continue
            
            last_asst = asst_msgs[-1]
            content = last_asst.get("content")
            if isinstance(content, str):
                text = content.strip()
            elif isinstance(content, (list, tuple)) or (hasattr(content, "__iter__") and not isinstance(content, str)):
                text_parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                text = "\n".join(text_parts).strip()
            else:
                continue

            if not is_valid_prose(text):
                continue

            h = compute_hash(text)
            if h in seen_hashes:
                continue
            seen_hashes.add(h)

            candidates.append({
                "source_bucket": bucket_id,
                "source_file": p_path.name,
                "model": row.get("teacher_model", "deepseek-v4-pro"),
                "task_type": row.get("task_type", "agentic_execution"),
                "domain": row.get("domain", "code"),
                "trajectory_id": str(row.get("id", "")),
                "text": text,
                "char_len": len(text),
                "word_count": len(text.split()),
                "sha256": h
            })

            if len(candidates) >= max_needed:
                break
        if len(candidates) >= max_needed:
            break

    print(f"[✓] Extracted {len(candidates)} candidates from {bucket_id}")
    return candidates

# -----------------------------------------------------------------------------
# Bucket 2: K3 Bucket (MoonshotAI Kimi-K3)
# -----------------------------------------------------------------------------
def extract_k3_traces(api: HfApi) -> List[Dict[str, Any]]:
    bucket_id = "jamesnavinhill/k3-bucket"
    target_dir = CACHE_DIR / "k3"
    target_dir.mkdir(parents=True, exist_ok=True)

    items = list(api.list_bucket_tree(bucket_id))
    trace_files = [i for i in items if hasattr(i, "size") and i.size > 0 and i.path.endswith(".jsonl") and not i.path.endswith("manifest.jsonl")]
    
    # Download missing files
    to_dl = []
    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists() or local_p.stat().st_size == 0:
            to_dl.append((tf.path, local_p))
    
    if to_dl:
        print(f"[*] Downloading {len(to_dl)} files from {bucket_id}...")
        api.download_bucket_files(bucket_id, to_dl)

    candidates = []
    seen_hashes = set()

    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists():
            continue
        try:
            with open(local_p, "r", encoding="utf-8") as f:
                events = [json.loads(line) for line in f if line.strip()]
            
            # Find terminal text message
            msgs = [e for e in events if e.get("type") == "message"]
            if not msgs:
                continue
            
            # Scan backwards for substantive text without tool calls
            for e in reversed(msgs):
                m = e.get("message", {})
                if m.get("role") != "assistant":
                    continue
                content = m.get("content", [])
                if isinstance(content, list):
                    text_parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                    tools = [c for c in content if isinstance(c, dict) and (c.get("type") == "toolCall" or "arguments" in c)]
                    text = "\n".join(text_parts).strip()
                    if len(tools) == 0 and is_valid_prose(text):
                        h = compute_hash(text)
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            candidates.append({
                                "source_bucket": bucket_id,
                                "source_file": local_p.name,
                                "model": "moonshotai/kimi-k3",
                                "task_type": "sandbox_verification",
                                "domain": "engineering",
                                "trajectory_id": e.get("id", local_p.stem),
                                "text": text,
                                "char_len": len(text),
                                "word_count": len(text.split()),
                                "sha256": h
                            })
        except Exception as err:
            pass

    print(f"[✓] Extracted {len(candidates)} candidates from {bucket_id}")
    return candidates

# -----------------------------------------------------------------------------
# Bucket 3: KernelBench Mega Traces (Frontier Models)
# -----------------------------------------------------------------------------
def extract_kernelbench_traces(api: HfApi) -> List[Dict[str, Any]]:
    bucket_id = "jamesnavinhill/kernelbench-mega-traces-bucket"
    target_dir = CACHE_DIR / "kernelbench"
    target_dir.mkdir(parents=True, exist_ok=True)

    items = list(api.list_bucket_tree(bucket_id))
    trace_files = [i for i in items if hasattr(i, "size") and i.size > 0 and i.path.endswith(".jsonl")]

    to_dl = []
    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists() or local_p.stat().st_size == 0:
            to_dl.append((tf.path, local_p))

    if to_dl:
        print(f"[*] Downloading {len(to_dl)} files from {bucket_id}...")
        api.download_bucket_files(bucket_id, to_dl)

    candidates = []
    seen_hashes = set()

    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists():
            continue
        try:
            # Parse model name from filename
            parts = local_p.name.split("_")
            model_name = parts[2] if len(parts) > 2 else "frontier_model"
            if len(parts) >= 4 and parts[1] in ("codex", "claude", "zai-claude", "minimax-claude", "kimi-claude", "deepseek-claude", "cursor", "gemini"):
                model_name = f"{parts[1]}_{parts[2]}"

            with open(local_p, "r", encoding="utf-8") as f:
                events = [json.loads(line) for line in f if line.strip()]

            assts = [e for e in events if e.get("type") == "assistant"]
            # Scan backwards for concluding response
            for a in reversed(assts):
                msg = a.get("message", {})
                content = msg.get("content", [])
                if isinstance(content, list):
                    text_parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                    tools = [c for c in content if isinstance(c, dict) and c.get("type") == "tool_use"]
                    text = "\n".join(text_parts).strip()
                    if len(tools) == 0 and is_valid_prose(text):
                        h = compute_hash(text)
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            candidates.append({
                                "source_bucket": bucket_id,
                                "source_file": local_p.name,
                                "model": model_name,
                                "task_type": "kernel_optimization",
                                "domain": "engineering",
                                "trajectory_id": a.get("uuid", local_p.stem),
                                "text": text,
                                "char_len": len(text),
                                "word_count": len(text.split()),
                                "sha256": h
                            })
        except Exception as err:
            pass

    print(f"[✓] Extracted {len(candidates)} candidates from {bucket_id}")
    return candidates

# -----------------------------------------------------------------------------
# Bucket 4: Claude Fable-5 Claude-Code Bucket (Developer CLI Sessions)
# -----------------------------------------------------------------------------
def extract_claude_code_traces(api: HfApi) -> List[Dict[str, Any]]:
    bucket_id = "jamesnavinhill/claude-fable-5-claude-code-bucket"
    target_dir = CACHE_DIR / "claude_code"
    target_dir.mkdir(parents=True, exist_ok=True)

    items = list(api.list_bucket_tree(bucket_id))
    trace_files = [i for i in items if hasattr(i, "size") and i.size > 0 and i.path.endswith(".jsonl")]

    to_dl = []
    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists() or local_p.stat().st_size == 0:
            to_dl.append((tf.path, local_p))

    if to_dl:
        print(f"[*] Downloading {len(to_dl)} files from {bucket_id}...")
        api.download_bucket_files(bucket_id, to_dl)

    candidates = []
    seen_hashes = set()

    for tf in trace_files:
        local_p = target_dir / Path(tf.path).name
        if not local_p.exists():
            continue
        try:
            with open(local_p, "r", encoding="utf-8") as f:
                events = [json.loads(line) for line in f if line.strip()]

            assts = [e for e in events if e.get("type") == "assistant" and not e.get("error") and not e.get("isApiErrorMessage")]
            for a in reversed(assts):
                msg = a.get("message", {})
                content = msg.get("content", [])
                if isinstance(content, list):
                    text_parts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                    tools = [c for c in content if isinstance(c, dict) and c.get("type") == "tool_use"]
                    text = "\n".join(text_parts).strip()
                    if len(tools) == 0 and is_valid_prose(text):
                        h = compute_hash(text)
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            candidates.append({
                                "source_bucket": bucket_id,
                                "source_file": local_p.name,
                                "model": msg.get("model", "claude-code"),
                                "task_type": "interactive_cli_session",
                                "domain": "engineering",
                                "trajectory_id": a.get("uuid", local_p.stem),
                                "text": text,
                                "char_len": len(text),
                                "word_count": len(text.split()),
                                "sha256": h
                            })
                        break
        except Exception as err:
            pass

    print(f"[✓] Extracted {len(candidates)} candidates from {bucket_id}")
    return candidates

# -----------------------------------------------------------------------------
# Bucket 5: Fable-5 Premium Bucket (Claude Fable-5 & Opus Benchmark Traces)
# -----------------------------------------------------------------------------
def extract_fable_premium_traces(api: HfApi) -> List[Dict[str, Any]]:
    bucket_id = "jamesnavinhill/fable-5-premium-bucket"
    target_dir = CACHE_DIR / "fable_premium"
    target_dir.mkdir(parents=True, exist_ok=True)

    files = [
        ("agent_traces/validation.parquet", target_dir / "validation.parquet"),
        ("agent_traces/test.parquet", target_dir / "test.parquet")
    ]
    to_dl = [(r, l) for r, l in files if not l.exists() or l.stat().st_size == 0]
    if to_dl:
        print(f"[*] Downloading {len(to_dl)} files from {bucket_id}...")
        api.download_bucket_files(bucket_id, to_dl)

    candidates = []
    seen_hashes = set()

    for _, local_p in files:
        if not local_p.exists():
            continue
        try:
            df = pd.read_parquet(local_p)
            for _, row in df.iterrows():
                msgs = row.get("messages")
                if isinstance(msgs, str):
                    try:
                        msgs = json.loads(msgs)
                    except Exception:
                        continue
                if not isinstance(msgs, (list, tuple)):
                    continue
                asst_msgs = [m for m in msgs if isinstance(m, dict) and m.get("role") == "assistant"]
                if not asst_msgs:
                    continue
                content = asst_msgs[-1].get("content", "")
                if isinstance(content, list):
                    content = "\n".join([c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"])
                if isinstance(content, str) and is_valid_prose(content):
                    h = compute_hash(content)
                    if h not in seen_hashes:
                        seen_hashes.add(h)
                        candidates.append({
                            "source_bucket": bucket_id,
                            "source_file": local_p.name,
                            "model": row.get("model", "claude-fable-5"),
                            "task_type": "coding_benchmark",
                            "domain": "engineering",
                            "trajectory_id": str(row.get("session_id", "")),
                            "text": content.strip(),
                            "char_len": len(content.strip()),
                            "word_count": len(content.strip().split()),
                            "sha256": h
                        })
        except Exception as err:
            pass

    print(f"[✓] Extracted {len(candidates)} candidates from {bucket_id}")
    return candidates

# -----------------------------------------------------------------------------
# Bucket 6: SWE-Hero OpenHands Trajectories (Real-World SWE Issue Resolution)
# -----------------------------------------------------------------------------
def extract_swe_hero_traces(max_needed: int) -> List[Dict[str, Any]]:
    dataset_id = "nvidia/SWE-Hero-openhands-trajectories"
    print(f"[*] Stream-sampling up to {max_needed} concluding responses from {dataset_id}...")
    candidates = []
    seen_hashes = set()

    for chunk in range(14):
        if len(candidates) >= max_needed:
            break
        url = f"https://huggingface.co/datasets/nvidia/SWE-Hero-openhands-trajectories/resolve/main/data/train-{chunk:05d}-of-00014.parquet"
        print(f"[*] Reading chunk {chunk:02d} ({url.split('/')[-1]})...")
        try:
            df = pd.read_parquet(url)
            for _, row in df.iterrows():
                traj = row.get("trajectory")
                if not isinstance(traj, (list, tuple)) and not hasattr(traj, "__iter__"):
                    continue
                traj_list = list(traj)
                if not traj_list:
                    continue
                last = traj_list[-1]
                if not isinstance(last, dict):
                    continue

                text = (last.get("content") or "").strip()
                tc = last.get("tool_calls", [])
                if isinstance(tc, (list, tuple)):
                    for c in tc:
                        if isinstance(c, dict):
                            fn = c.get("function", {})
                            args = fn.get("arguments", "")
                            if isinstance(args, str) and "message" in args:
                                try:
                                    args_obj = json.loads(args)
                                    m = args_obj.get("message", "")
                                    if isinstance(m, str) and len(m) > len(text):
                                        text = m.strip()
                                except Exception:
                                    pass

                if is_valid_prose(text):
                    h = compute_hash(text)
                    if h not in seen_hashes:
                        seen_hashes.add(h)
                        candidates.append({
                            "source_bucket": dataset_id,
                            "source_file": f"train-{chunk:05d}-of-00014.parquet",
                            "model": "openhands/swe-agent",
                            "task_type": "swe_issue_resolution",
                            "domain": f"repo:{row.get('repo', 'python')}",
                            "trajectory_id": str(row.get("instance_id", "")),
                            "text": text,
                            "char_len": len(text),
                            "word_count": len(text.split()),
                            "sha256": h
                        })
                        if len(candidates) >= max_needed:
                            break
        except Exception as err:
            print(f"[!] Warning reading chunk {chunk}: {err}")
            continue

    print(f"[✓] Extracted {len(candidates)} candidates from {dataset_id}")
    return candidates

# -----------------------------------------------------------------------------
# Main Extraction Coordinator
# -----------------------------------------------------------------------------
def main():
    env = load_env()
    token = env.get("HF_TOKEN")
    if not token:
        print("[!] HF_TOKEN not found in .env")
        sys.exit(1)

    api = HfApi(token=token)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Starting Trace Concluding 'DONE' Response Extraction (Target: ~10,000)")
    print("=" * 70)

    # 1. Specialized frontier sources from user buckets
    claude_cands = extract_claude_code_traces(api)
    kb_cands = extract_kernelbench_traces(api)
    k3_cands = extract_k3_traces(api)
    fable_cands = extract_fable_premium_traces(api)
    ds_cands = extract_deepseek_traces(api, max_needed=5000)

    local_total = len(claude_cands) + len(kb_cands) + len(k3_cands) + len(fable_cands) + len(ds_cands)
    print(f"[*] Assembled {local_total} candidates from user trace buckets.")

    needed_from_swe = max(0, TARGET_TOTAL - local_total)
    swe_cands = []
    if needed_from_swe > 0:
        # Buffer slightly by 200 to account for cross-dataset deduplication
        swe_cands = extract_swe_hero_traces(max_needed=needed_from_swe + 200)

    all_candidates = claude_cands + kb_cands + k3_cands + fable_cands + ds_cands + swe_cands

    # Deduplicate across the full composite
    unique_candidates = []
    global_hashes = set()
    for c in all_candidates:
        if c["sha256"] not in global_hashes:
            global_hashes.add(c["sha256"])
            # Assign canonical ID
            c["id"] = f"raw_trace_{len(unique_candidates):05d}"
            unique_candidates.append(c)
            if len(unique_candidates) >= TARGET_TOTAL:
                break

    print("\n" + "=" * 70)
    print(f"Extraction Complete: {len(unique_candidates)} unique responses assembled!")
    print("=" * 70)

    # Convert to DataFrame
    df = pd.DataFrame(unique_candidates)

    # Summary Statistics
    model_counts = df["model"].value_counts().to_dict()
    bucket_counts = df["source_bucket"].value_counts().to_dict()
    char_stats = {
        "min": int(df["char_len"].min()),
        "max": int(df["char_len"].max()),
        "mean": float(df["char_len"].mean()),
        "median": float(df["char_len"].median())
    }
    word_stats = {
        "min": int(df["word_count"].min()),
        "max": int(df["word_count"].max()),
        "mean": float(df["word_count"].mean()),
        "median": float(df["word_count"].median())
    }

    report = {
        "total_records": len(df),
        "target_total": TARGET_TOTAL,
        "models": model_counts,
        "buckets": bucket_counts,
        "character_length": char_stats,
        "word_count": word_stats
    }

    # Write files
    jsonl_out = OUTPUT_DIR / "assistant_done_10k.jsonl"
    parquet_out = OUTPUT_DIR / "assistant_done_10k.parquet"
    report_out = OUTPUT_DIR / "extraction_report.json"

    print(f"[*] Writing {jsonl_out}...")
    df.to_json(jsonl_out, orient="records", lines=True, force_ascii=False)

    print(f"[*] Writing {parquet_out}...")
    df.to_parquet(parquet_out, index=False)

    print(f"[*] Writing {report_out}...")
    with open(report_out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\nSummary Distribution:")
    for m, cnt in model_counts.items():
        print(f"  {m:<35} : {cnt:>6d} responses")
    print(f"\nLength Profile: Median {char_stats['median']} chars, Mean {char_stats['mean']:.1f} chars")
    print(f"Artifacts successfully written to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
