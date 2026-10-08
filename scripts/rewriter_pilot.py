#!/usr/bin/env python3
"""
Gateway Rewriter Pilot & Evaluation Pipeline (Task T7 & T8)
Extracts 20 diverse raw candidates from datasets/raw_candidates/assistant_done_10k.parquet,
applies domain-specific few-shot rewriter prompts with strict banned-cliché constraints,
invokes the Agency Gateway (ne-gpt-oss-120b / or-nvidia-nemotron-3-ultra-550b),
and evaluates the output against our style invariants.
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
OUTPUT_JSON = ROOT_DIR / "datasets" / "pilot_rewrites_free_20.json"
OUTPUT_MD = ROOT_DIR / "datasets" / "pilot_rewrites_free_comparison.md"
ENV_PATH = ROOT_DIR / ".env"

# -----------------------------------------------------------------------------
# Banned Tropes, Structural Crutches, & Cliché Patterns
# -----------------------------------------------------------------------------
BANNED_PATTERNS = [
    # 1. Contrastive Parallelism & Negative Framing
    (r"\b(?:it|this|that|those) (?:is|are|isn'?t|aren'?t) (?:not |n't )?(?:just )?.+?,? (?:it|they|this) (?:is|are)\b", "contrastive_parallelism"),
    (r"\bnot just (?:a |an )?.+?,? (?:but|they|it)\b", "not_just_contrast"),
    (r"\brather than .+?, (?:it|the system|we) now\b", "rather_than_contrast"),

    # 2. Manufactured Significance Signposts
    (r"\b(?:here'?s )?why this matters\b", "why_this_matters_signpost"),
    (r"\bwhy it matters\b", "why_it_matters_signpost"),
    (r"\b(?:now )?the (?:real|honest|hard) truth\b", "the_real_truth_signpost"),
    (r"\bwhat (?:everyone|everybody)('?s| is) missing\b", "what_everyones_missing"),
    (r"\bwhat no ?one('?s| is) talking about\b", "what_no_ones_talking_about"),
    (r"\bthe part that (?:really matters|silently bites|stings|hurts)\b", "the_part_that_bites"),
    (r"\bthe (?:kicker|catch|payoff|rub)\b", "manufactured_climax"),
    (r"\bhit(?:s|ting)? the nail on the head\b", "nail_on_head_cliche"),

    # 3. Compulsive Negative Disclaimers
    (r"\b(?:note that )?this does not (?:modify|delete|change|touch|break|replace|affect)\b", "negative_disclaimer"),
    (r"\bwhat (?:this|it) does not do\b", "what_it_does_not_do"),

    # 4. Modern Jargon, Hedging, & Buzzwords
    (r"\bload-bearing\b", "load_bearing_jargon"),
    (r"\bit'?s worth (?:noting|pointing out|mentioning)\b", "worth_noting_hedging"),
    (r"\bdelve\b", "delve_buzzword"),
    (r"\btestament to\b", "testament_to_buzzword"),
    (r"\bseamlessly\b", "seamlessly_buzzword"),
    (r"\bmultifaceted\b", "multifaceted_buzzword"),
    (r"\bcomprehensive suite\b", "comprehensive_suite_buzzword"),
    (r"\bgame-changer\b", "game_changer_buzzword"),
    (r"\bstep-function\b", "step_function_buzzword"),

    # 5. Sycophancy & Preamble Slop
    (r"\b(?:certainly|sure)!?\b", "throat_clearing_opener"),
    (r"\byou(?:'re| are) (?:100%|completely|totally|entirely) right\b", "sycophantic_agreement"),
    (r"\blet'?s (?:unpack|dive in|explore)\b", "unpack_dive_preamble"),
    (r"\bwe are (?:thrilled|excited|proud) to\b", "cheerleader_announcement"),
    (r"\bi have successfully (?:implemented|fixed|updated)\b", "i_have_successfully_implemented"),
    (r"\bhere(?:'s| is) what was accomplished\b", "heres_what_was_accomplished"),
    (r"\ball tests confirm the issue is resolved\b", "all_tests_confirm_slop")
]

# -----------------------------------------------------------------------------
# Domain Prompt Templates with Grounded Style Invariants
# -----------------------------------------------------------------------------
SYSTEM_CORE = """You are a Principal Systems Engineer and Staff Technical Writer at a high-standards infrastructure company.
Your job is to rewrite raw, verbose agent logs into calm, high-signal, human-written engineering prose.

NON-NEGOTIABLE WRITING RULES:
1. NO CONTRASTIVE PARALLELISM: NEVER write "It's not X, it's Y", "This isn't just about X; it's about Y", or "Those aren't just A, they are B". State the positive mechanical fact directly.
2. NO SIGNIFICANCE SIGNPOSTS: NEVER write "Why this matters", "Here's what everyone is missing", "The real truth", "The part that silently bites", "The kicker is", or "The payoff". Do not lecture the reader on how to feel about a technical fact.
3. NO COMPULSIVE NEGATIVE DISCLAIMERS: Do NOT append unsolicited "What this does NOT do" disclaimers (e.g. "Note that this does NOT modify the database"). State what the code does; assume the reader knows what it doesn't do.
4. NO THROAT-CLEARING OR PREAMBLES: Never open with "Certainly!", "Sure!", "I have successfully implemented", "Here is what was accomplished", or "You are right". Start directly with the technical subject or action.
5. NO BUZZWORDS OR TECH-TWITTER SLOP: Ban "load-bearing", "first-principles", "step-function", "bespoke", "delve", "seamlessly", "testament to", "multifaceted".
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
Target Vibe: Feature-velocity storytelling, active verbs, concise architectural causality, and zero corporate cheerleading.
Do NOT use negative parallelism ("It's not X, it's Y"), do NOT add "what this does not do" disclaimers, and do NOT use checklist soup (✅ emoji bullets).

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

def check_banned_cliches(text: str) -> List[str]:
    violations = []
    lower = text.lower()
    for pattern, tag in BANNED_PATTERNS:
        match = re.search(pattern, lower)
        if match:
            violations.append(f"{tag}: '{match.group(0)}'")
    return violations

def call_gateway(base_url: str, api_key: str, model: str, prompt: str) -> tuple[str, bool]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_CORE},
            {"role": "user", "content": prompt}
        ]
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        choices = data.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            finish_reason = choices[0].get("finish_reason", "")
            is_truncated = (finish_reason == "length")
            content = msg.get("content") or ""
            return content.strip(), is_truncated
    return "", False

def main():
    env = load_env()
    base_url = env.get("GATEWAY_BASE_URL", "").rstrip("/")
    api_key = env.get("GATEWAY_API_KEY", "")
    if not base_url or not api_key:
        print("[!] Gateway credentials not found in .env")
        sys.exit(1)

    print("=" * 70)
    print("Rewriter Pilot (100% FREE Models): GLM 5.3, Kimi K3, Nemotron 3 Ultra 550B")
    print("=" * 70)

    df = pd.read_parquet(RAW_PARQUET)
    print(f"[*] Loaded raw candidates dataset: {len(df)} total rows.")

    # Sample 20 diverse rows across sources and lengths:
    # 7 openhands, 6 deepseek, 4 k3, 2 fable-5, 1 kernelbench
    samples = []
    
    # 1. OpenHands (SWE issue fixes) -> 7 samples
    oh_sub = df[df["model"] == "openhands/swe-agent"].sample(n=7, random_state=42)
    for _, r in oh_sub.iterrows():
        samples.append((r, "changelogs"))  # Excellent for PR / Changelogs

    # 2. DeepSeek V4 Pro -> 6 samples
    ds_sub = df[df["model"] == "deepseek-v4-pro"].sample(n=6, random_state=42)
    for _, r in ds_sub.iterrows():
        samples.append((r, "tech_docs"))

    # 3. Kimi K3 -> 4 samples
    k3_sub = df[df["model"] == "moonshotai/kimi-k3"].sample(n=4, random_state=42)
    for i, (_, r) in enumerate(k3_sub.iterrows()):
        dom = "tech_docs" if i % 2 == 0 else "changelogs"
        samples.append((r, dom))

    # 4. Fable-5 -> 2 samples
    fb_sub = df[df["model"] == "claude-fable-5"].sample(n=2, random_state=42)
    for _, r in fb_sub.iterrows():
        samples.append((r, "tech_docs"))

    # 5. KernelBench frontier -> 1 sample
    kb_sub = df[df["source_bucket"] == "jamesnavinhill/kernelbench-mega-traces-bucket"].sample(n=1, random_state=42)
    for _, r in kb_sub.iterrows():
        samples.append((r, "changelogs"))

    print(f"[*] Assembled {len(samples)} pilot evaluation samples.")

    # Strictly 100% FREE Nvidia NIM models (champion: Kimi K3)
    models_to_test = [
        "nv-moonshotai-kimi-k3",
        "nv-nvidia-nemotron-3-ultra-550b-a55b"
    ]

    results = []
    for idx, (row, domain) in enumerate(samples, 1):
        model = models_to_test[(idx - 1) % len(models_to_test)]
        prompt_tmpl = DOMAIN_TEMPLATES[domain]
        raw_text = row["text"]
        prompt = prompt_tmpl.format(raw_text=raw_text)

        print(f"\n[{idx:02d}/20] Processing {row['id']} | Domain: {domain:<16} | Model: {model}...", flush=True)
        try:
            rewritten, is_truncated = call_gateway(base_url, api_key, model, prompt)
            cliche_violations = check_banned_cliches(rewritten)
            
            raw_len = len(raw_text)
            rewritten_len = len(rewritten)
            compression = rewritten_len / raw_len if raw_len > 0 else 1.0

            status_mark = "PASS" if not cliche_violations and not is_truncated else f"WARN({len(cliche_violations)})"
            if is_truncated:
                status_mark = "TRUNCATED"
            print(f"      Status: [{status_mark}] Raw: {raw_len} chars -> Rewritten: {rewritten_len} chars (ratio: {compression:.2f})", flush=True)
            if cliche_violations:
                print(f"      [!] Clichés found: {cliche_violations}", flush=True)

            results.append({
                "sample_id": row["id"],
                "source_bucket": row["source_bucket"],
                "source_model": row["model"],
                "domain": domain,
                "rewriter_model": model,
                "raw_text": raw_text,
                "raw_char_len": raw_len,
                "raw_word_count": len(raw_text.split()),
                "rewritten_text": rewritten,
                "rewritten_char_len": rewritten_len,
                "rewritten_word_count": len(rewritten.split()),
                "compression_ratio": round(compression, 3),
                "cliche_violations": cliche_violations
            })
        except Exception as e:
            print(f"      [!] Error invoking gateway: {e}")

    # Save JSON results
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[✓] Saved pilot JSON results to {OUTPUT_JSON}")

    # Generate Markdown comparison
    md_lines = [
        "# Pilot Rewriter Evaluation Report (20 Samples — 100% FREE Models)",
        "",
        "This report compares raw agent trace conclusions against humanized rewrites generated strictly via 100% FREE Nvidia NIM models (`nv-z-ai-glm-5-3`, `nv-moonshotai-kimi-k3`, and `nv-nvidia-nemotron-3-ultra-550b-a55b`), conditioned on our 34 style exemplars and the Anti-Slop Specification.",
        "",
        "---",
        "",
        "## Summary Metrics",
        "",
        f"- **Total Samples Evaluated**: {len(results)}",
        f"- **Tech Docs**: {sum(1 for r in results if r['domain'] == 'tech_docs')}",
        f"- **Changelogs / PR Notes**: {sum(1 for r in results if r['domain'] == 'changelogs')}",
        f"- **Mean Raw Length**: {int(sum(r['raw_char_len'] for r in results) / len(results))} chars",
        f"- **Mean Rewritten Length**: {int(sum(r['rewritten_char_len'] for r in results) / len(results))} chars",
        f"- **Mean Compression Ratio**: {sum(r['compression_ratio'] for r in results) / len(results):.2f}",
        f"- **Banned Cliché Violations**: {sum(len(r['cliche_violations']) for r in results)} total",
        "",
        "---",
        ""
    ]

    for idx, r in enumerate(results, 1):
        md_lines.extend([
            f"### Sample {idx:02d}: {r['sample_id']} ({r['domain'].upper()})",
            f"- **Original Source**: `{r['source_model']}` ({r['source_bucket']})",
            f"- **Rewriter**: `{r['rewriter_model']}`",
            f"- **Length**: Raw `{r['raw_char_len']}` chars -> Rewritten `{r['rewritten_char_len']}` chars (ratio `{r['compression_ratio']}`)",
            f"- **Cliché Violations**: `{r['cliche_violations'] if r['cliche_violations'] else 'None (Clean)'}`",
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
    print(f"[✓] Saved readable comparison report to {OUTPUT_MD}")

if __name__ == "__main__":
    main()
