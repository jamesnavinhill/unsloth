#!/usr/bin/env python3
"""
10-Sample Clean Evaluation Run
Strict invariants:
1. 100% FREE models: nv-moonshotai-kimi-k3 & nv-nvidia-nemotron-3-ultra-550b-a55b.
2. Official upstream sampling defaults only: no client-side temperature, top_p, or max_tokens overrides.
3. Clean input pool: genuine software engineering agent completions only (zero leaked prompts).
4. Domains: 5 Tech Docs (Stripe/Fly.io) + 5 Changelogs/PRs (Linear).
5. Zero truncation: full raw texts and full target completions in output.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_PARQUET = ROOT_DIR / "datasets" / "raw_candidates" / "assistant_done_10k.parquet"
OUTPUT_JSON = ROOT_DIR / "datasets" / "eval_10_clean.json"
OUTPUT_MD = ROOT_DIR / "datasets" / "eval_10_clean_comparison.md"
ENV_PATH = ROOT_DIR / ".env"

SYSTEM_CORE = """You are a Principal Systems Engineer and Staff Technical Writer at a high-standards infrastructure company.
Your job is to rewrite raw, verbose agent logs into calm, high-signal, human-written engineering prose.

NON-NEGOTIABLE WRITING RULES:
1. NO CONTRASTIVE PARALLELISM: NEVER write "It's not X, it's Y", "This isn't just about X; it's about Y", or "Those aren't just A, they are B". State the positive mechanical fact directly.
2. NO SIGNIFICANCE SIGNPOSTS: NEVER write "Why this matters", "Here's what everyone is missing", "The real truth", "The part that silently bites", "The kicker is", or "The payoff". Do not lecture the reader.
3. NO COMPULSIVE NEGATIVE DISCLAIMERS: Do NOT append unsolicited "What this does NOT do" disclaimers. State what the code does.
4. NO THROAT-CLEARING OR PREAMBLES: Never open with "Certainly!", "Sure!", "I have successfully implemented", "Here is what was accomplished", or "You are right". Start directly with the technical subject or action.
5. NO BUZZWORDS OR TROPES: Ban "load-bearing", "first-principles", "step-function", "bespoke", "delve", "seamlessly", "testament to", "multifaceted". Do NOT adopt colloquial storytelling tropes from the input.
6. NO LIST SOUP: Do not jumble 4–6 acute technical terms together in a breathless comma-separated run-on sentence. Isolate the single mechanical failure or invariant that matters.
7. WRITE FOR ADULTS: Maintain high technical fidelity (keep exact file paths, function signatures, error names, and parameters intact). Use calm, declarative active sentences.
"""

TECH_DOCS_PROMPT = """You are writing technical documentation in the style of Stripe, Linear, and Fly.io docs.
Target Vibe: High-precision clarity, explicit preconditions, clear mechanics, parameter contracts, and zero fluff.
Do NOT use negative parallelism ("It's not X, it's Y"), do NOT add unsolicited "what this does not do" disclaimers, and do NOT use "Why this matters" signposts.

REFERENCE EXEMPLAR (Stripe / Fly.io Docs Style):
"The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Subsequent requests with the same key return the same result, including 500 errors. We save results only after the execution of an endpoint begins."

RAW AGENT OUTPUT TO REWRITE:
{raw_text}

REWRITE as a clean, publication-ready Technical Documentation section (Markdown format, declarative facts only, zero slop):"""

CHANGELOG_PROMPT = """You are writing a changelog entry and pull request summary in the style of Linear, Stripe, and Fly.io platform releases.
Target Vibe: Feature-velocity storytelling, active verbs, concise architectural causality, zero corporate cheerleading, zero emoji checklists.

REFERENCE EXEMPLAR (Linear Release Changelog Style):
"Fixed group ordering in `GroupBy.value_counts` when `sort=False`. Previously, `sort=True` globally sorted all values by count before restoring group indices, which scrambled the original insertion order. The sorting logic now operates strictly within individual group partitions before concatenating results."

RAW AGENT OUTPUT TO REWRITE:
{raw_text}

REWRITE as a clean, punchy Changelog / PR description entry (Markdown format, active verbs, zero slop):"""

DOMAIN_TEMPLATES = {
    "tech_docs": TECH_DOCS_PROMPT,
    "changelogs": CHANGELOG_PROMPT
}

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

def call_gateway(base_url: str, api_key: str, model: str, prompt: str, max_retries: int = 3) -> tuple[str, str]:
    import time
    # Strictly send model and messages. Upstream defaults apply.
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_CORE},
            {"role": "user", "content": prompt}
        ]
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(
                f"{base_url}/chat/completions",
                data=data_bytes,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    finish_reason = choices[0].get("finish_reason", "")
                    content = msg.get("content") or ""
                    return content.strip(), finish_reason
        except Exception as e:
            print(f"       [!] Attempt {attempt}/{max_retries} failed ({e}). Retrying in 5s...")
            time.sleep(5)
    return "", "error"

def main():
    env = load_env()
    base_url = env.get("GATEWAY_BASE_URL", "").rstrip("/")
    api_key = env.get("GATEWAY_API_KEY", "")
    if not base_url or not api_key:
        print("[!] Gateway credentials missing from .env")
        sys.exit(1)

    print("=" * 70)
    print("10-Sample Clean Evaluation Run")
    print("Models: nv-moonshotai-kimi-k3 & nv-nvidia-nemotron-3-ultra-550b-a55b")
    print("Parameters: Gateway upstream defaults only (temp: 1.0, top_p: 0.95)")
    print("=" * 70)

    df = pd.read_parquet(RAW_PARQUET)
    
    # Filter strictly for genuine software engineering completions
    # Drop prompt leaked strings and non-software tasks
    prompt_leaks = [
        "=== MOONSHINER", "We're integrating", "Please fix", "Build three",
        "Your task is", "Implement a", "You are given"
    ]
    mask = (df["model"] == "openhands/swe-agent")
    for leak in prompt_leaks:
        mask = mask & (~df["text"].str.contains(leak, case=False, regex=False))
    
    clean_df = df[mask].reset_index(drop=True)
    print(f"[*] Clean SWE candidate pool: {len(clean_df)} rows.")

    # Select 10 diverse samples using fixed seed (starting from index 300 to avoid pilot overlaps)
    selected_indices = [310, 325, 340, 355, 370, 385, 400, 415, 430, 445]
    
    eval_plan = [
        # (index, domain, model)
        (selected_indices[0], "changelogs", "nv-moonshotai-kimi-k3"),
        (selected_indices[1], "changelogs", "nv-nvidia-nemotron-3-ultra-550b-a55b"),
        (selected_indices[2], "changelogs", "nv-moonshotai-kimi-k3"),
        (selected_indices[3], "changelogs", "nv-nvidia-nemotron-3-ultra-550b-a55b"),
        (selected_indices[4], "changelogs", "nv-moonshotai-kimi-k3"),
        (selected_indices[5], "tech_docs", "nv-nvidia-nemotron-3-ultra-550b-a55b"),
        (selected_indices[6], "tech_docs", "nv-moonshotai-kimi-k3"),
        (selected_indices[7], "tech_docs", "nv-nvidia-nemotron-3-ultra-550b-a55b"),
        (selected_indices[8], "tech_docs", "nv-moonshotai-kimi-k3"),
        (selected_indices[9], "tech_docs", "nv-nvidia-nemotron-3-ultra-550b-a55b"),
    ]

    results = []

    for idx, (row_idx, domain, model) in enumerate(eval_plan, 1):
        row = clean_df.iloc[row_idx]
        sample_id = row["id"]
        raw_text = row["text"].strip()
        template = DOMAIN_TEMPLATES[domain]
        prompt = template.format(raw_text=raw_text)

        print(f"\n[{idx:02d}/10] Running {sample_id} ({domain.upper()}) on {model}...")
        print(f"       Raw length: {len(raw_text)} chars")

        rewritten, finish_reason = call_gateway(base_url, api_key, model, prompt)
        print(f"       Rewritten length: {len(rewritten)} chars | finish_reason: {finish_reason}")

        results.append({
            "sample_index": idx,
            "sample_id": sample_id,
            "source_model": row["model"],
            "source_file": row["source_file"],
            "domain": domain,
            "rewriter_model": model,
            "raw_text": raw_text,
            "raw_char_len": len(raw_text),
            "rewritten_text": rewritten,
            "rewritten_char_len": len(rewritten),
            "finish_reason": finish_reason
        })

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[✓] Saved raw JSON to {OUTPUT_JSON}")

    # Build full untruncated Markdown comparison report
    md_lines = [
        "# Clean Evaluation Report (10 Samples)",
        "",
        "This evaluation strictly uses official upstream sampling parameters (NVIDIA NIM / LiteLLM defaults: `temperature: 1.0, top_p: 0.95`).",
        "Raw inputs are genuine SWE-Hero software engineering completions. No artificial token caps, no display slicing.",
        "",
        "---",
        "",
        "## Summary Metrics",
        "",
        f"- **Total Samples**: {len(results)}",
        f"- **Changelogs / PR Notes**: {sum(1 for r in results if r['domain'] == 'changelogs')}",
        f"- **Technical Documentation**: {sum(1 for r in results if r['domain'] == 'tech_docs')}",
        f"- **Models Evaluated**: `nv-moonshotai-kimi-k3` (5), `nv-nvidia-nemotron-3-ultra-550b-a55b` (5)",
        f"- **All Finished on Stop Token**: {all(r['finish_reason'] == 'stop' for r in results)}",
        "",
        "---",
        ""
    ]

    for r in results:
        md_lines.extend([
            f"### Sample {r['sample_index']:02d}: {r['sample_id']} ({r['domain'].upper()})",
            f"- **Rewriter**: `{r['rewriter_model']}`",
            f"- **Raw Length**: {r['raw_char_len']} chars | **Rewritten Length**: {r['rewritten_char_len']} chars",
            f"- **Finish Reason**: `{r['finish_reason']}`",
            "",
            "#### 🔻 Raw Agent Output (Original)",
            "```markdown",
            r['raw_text'],
            "```",
            "",
            "#### 🌟 Rewritten Human Prose (Target)",
            r['rewritten_text'],
            "",
            "---",
            ""
        ])

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[✓] Saved full untruncated report to {OUTPUT_MD}")

if __name__ == "__main__":
    main()
