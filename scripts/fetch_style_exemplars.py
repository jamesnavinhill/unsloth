#!/usr/bin/env python3
"""
Style Exemplar Harvester
Pulls representative documentation, changelogs, and engineering lore from all 14 target sources:
  1. Tech Docs: Stripe, Linear, Plaid, Render, Docker, Fly.io
  2. Changelogs: Linear, Stripe, Fly.io
  3. Engineering Lore & Blogs: PostHog (non-Ian), Joel on Software, Dan Luu,
     Travis Downs, Julia Evans, Simon Willison, Pragmatic Engineer, The Daily WTF

Organizes into references/style_exemplars/<domain>/<source>/
"""

import os
import sys
import re
import shutil
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_BASE = ROOT_DIR / "references" / "style_exemplars"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = True
h2t.body_width = 0

def clean_html_to_markdown(raw_html: str, url: str, title: str, style_profile: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    # Strip scripts, styles, navs, footers
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()
    
    # Target main content area
    main = (
        soup.find("main") or
        soup.find("article") or
        soup.find("div", {"role": "main"}) or
        soup.find("div", {"class": re.compile(r"content|post|article|entry", re.I)}) or
        soup.find("body")
    )
    
    body_md = h2t.handle(str(main) if main else raw_html).strip()
    
    # Strip excessive newlines
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)
    # Sanitize dummy example API keys to pass GitHub Push Protection
    body_md = re.sub(r"sk_test_[a-zA-Z0-9]{20,}", "sk_test_mock_placeholder", body_md)
    body_md = re.sub(r"sk_live_[a-zA-Z0-9]{20,}", "sk_live_mock_placeholder", body_md)
    body_md = re.sub(r"rk_test_[a-zA-Z0-9]{20,}", "rk_test_mock_placeholder", body_md)
    
    header = f"# {title}\n\n**Source**: [{url}]({url})  \n**Style Profile**: {style_profile}\n\n---\n\n"
    return header + body_md

def download_and_save(category: str, source_name: str, doc_name: str, url: str, style_profile: str):
    target_dir = OUTPUT_BASE / category / source_name
    target_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_dir / f"{doc_name}.md"

    print(f"[*] Fetching {source_name} / {doc_name} from {url}...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read().decode("utf-8", errors="ignore")
            
            # If raw markdown
            if "markdown" in content_type or url.endswith(".md"):
                md = f"# {doc_name.replace('_', ' ').title()}\n\n**Source**: [{url}]({url})  \n**Style Profile**: {style_profile}\n\n---\n\n" + raw
            else:
                soup = BeautifulSoup(raw, "html.parser")
                page_title = soup.title.string.strip() if soup.title and soup.title.string else doc_name.replace('_', ' ').title()
                md = clean_html_to_markdown(raw, url, page_title, style_profile)

            with open(out_file, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"[✓] Saved {out_file.relative_to(ROOT_DIR)} ({len(md)} chars)")
    except Exception as err:
        print(f"[!] Failed to fetch {url}: {err}")

def main():
    print("=" * 70)
    print("Starting Style Exemplar Harvester")
    print("=" * 70)

    # 1. Tech Docs
    tech_docs = [
        # Stripe
        ("tech_docs", "stripe", "idempotent_requests", "https://docs.stripe.com/api/idempotent_requests", "High-precision technical clarity, respect for engineer time, zero fluff"),
        ("tech_docs", "stripe", "webhooks_overview", "https://docs.stripe.com/webhooks", "Architectural guidance, concrete causal reasoning, defensive edge cases"),
        # Linear
        ("tech_docs", "linear", "github_integration", "https://linear.app/docs/github", "Opinionated developer workflows, crisp active verbs, seamless scannability"),
        ("tech_docs", "linear", "start_guide", "https://linear.app/docs/start-guide", "Fast-onboarding clarity, modern minimalist phrasing"),
        # Plaid
        ("tech_docs", "plaid", "link_quickstart", "https://plaid.com/docs/link/", "Developer-first onboarding, clean step sequences, explicit parameter docs"),
        ("tech_docs", "plaid", "auth_product", "https://plaid.com/docs/auth/", "Protocol mechanics, structured error contracts, zero boilerplate"),
        # Render
        ("tech_docs", "render", "deploy_hooks", "https://render.com/docs/deploy-hooks", "Direct cloud primitives, clear curl/webhook examples, pragmatic operations"),
        ("tech_docs", "render", "web_services", "https://render.com/docs/web-services", "Infrastructure architecture, transparent defaults, operational clarity"),
        # Docker
        ("tech_docs", "docker", "multi_stage_builds", "https://docs.docker.com/build/building/multi-stage/", "Production optimization, step-by-step causal tradeoffs"),
        ("tech_docs", "docker", "what_is_a_container", "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/", "Foundational architecture, concrete analogies, clear boundary definitions"),
        # Fly.io
        ("tech_docs", "fly_io", "fly_machines_overview", "https://fly.io/docs/machines/overview/", "Deep virtualization realism, wry conversational tone, fast microvm mechanics"),
        ("tech_docs", "fly_io", "launch_quickstart", "https://docs.fly.io/getting-started/launch.md", "Direct developer CLI onboarding, no ceremony, transparent infrastructure")
    ]

    # 2. Changelogs & Release Notes
    changelogs = [
        ("changelogs", "linear", "linear_recent_changelog", "https://linear.app/changelog", "Feature-velocity storytelling, bulleted architectural impact, zero corporate buzzwords"),
        ("changelogs", "stripe", "stripe_api_changelog", "https://docs.stripe.com/changelog", "Breaking change clarity, deterministic dates, version deprecation explanations"),
        ("changelogs", "fly_io", "fly_platform_changelog", "https://fly.io/changelog/", "Conversational infrastructure updates, engineer-to-engineer transparency")
    ]

    # 3. Engineering Lore & Blogs
    blogs = [
        # PostHog (core team, verified non-Ian Vanagas)
        ("engineering_blogs", "posthog", "clickhouse_vs_postgres", "https://posthog.com/blog/clickhouse-vs-postgres", "Pragmatic data engineering tradeoffs, raw benchmark numbers, humorous candor"),
        ("engineering_blogs", "posthog", "how_ai_agents_behave", "https://posthog.com/blog/how-ai-agents-behave", "Empirical data breakdown across 63M tool calls, cynical pattern observations"),
        ("engineering_blogs", "posthog", "self_driving_loops", "https://posthog.com/blog/self-driving-loops", "Operational product engineering, iterative execution philosophy"),
        # Dan Luu
        ("engineering_blogs", "dan_luu", "productivity_velocity", "https://danluu.com/productivity-velocity/", "Deep empirical analysis, intellectual honesty, dissection of corporate mythology"),
        ("engineering_blogs", "dan_luu", "corporate_eng_blogs", "https://danluu.com/corp-eng-blogs/", "Candid critique of sanitized PR vs genuine engineering writing"),
        # Travis Downs
        ("engineering_blogs", "travis_downs", "performance_speed_limits", "https://travisdowns.github.io/blog/2019/06/11/speed-limits.html", "Low-level CPU performance lore, microbenchmarking discipline, hardware reality"),
        # Julia Evans (jvns)
        ("engineering_blogs", "julia_evans", "learning_running_sqlite", "https://jvns.ca/blog/2026/07/17/learning-about-running-sqlite/", "Delightfully approachable curiosity, demystifying complex technical machinery"),
        ("engineering_blogs", "julia_evans", "more_nice_django_things", "https://jvns.ca/blog/2026/07/21/more-nice-django-things/", "Opinionated practitioner experience, pragmatic tooling praise"),
        # Simon Willison
        ("engineering_blogs", "simon_willison", "claude_haiku_5_5", "https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/", "Concise practitioner commentary, immediate empirical testing, personal perspective"),
        # The Pragmatic Engineer (Gergely Orosz)
        ("engineering_blogs", "pragmatic_engineer", "ror_creator_death_of_coding_debate", "https://blog.pragmaticengineer.com/the-pulse-ror-creator-sparks-new-death-of-coding-by-hand-debate/", "High-level industry analysis, contextualized engineering debate, balanced realism"),
        ("engineering_blogs", "pragmatic_engineer", "cpu_shortages_pulse", "https://blog.pragmaticengineer.com/the-pulse-a-new-trend-of-cpu-shortages/", "Hardware macro trends, direct sourcing, investigative engineering journalism"),
        # The Daily WTF
        ("engineering_blogs", "daily_wtf", "what_you_measure", "https://thedailywtf.com/articles/what-you-measure", "Dry satirical wit, cautionary engineering folklore, Goodhart's law in practice"),
        ("engineering_blogs", "daily_wtf", "part_1_of_the_process", "https://thedailywtf.com/articles/it-s-all-part-1-of-the-process", "Classic developer horror storytelling, deadpan humor, bureaucratic comedy")
    ]

    all_targets = tech_docs + changelogs + blogs
    for category, src, name, url, profile in all_targets:
        download_and_save(category, src, name, url, profile)

    # Copy cached Joel on Software articles
    joel_dir = OUTPUT_BASE / "engineering_blogs" / "joel_on_software"
    joel_dir.mkdir(parents=True, exist_ok=True)
    
    # Process Joel articles from brain step artifacts
    step_656 = Path(r"C:\Users\james\.gemini\antigravity-ide\brain\98f1980c-702b-4cf6-9701-08d168f762eb\.system_generated\steps\656\content.md")
    step_658 = Path(r"C:\Users\james\.gemini\antigravity-ide\brain\98f1980c-702b-4cf6-9701-08d168f762eb\.system_generated\steps\658\content.md")
    step_614 = Path(r"C:\Users\james\.gemini\antigravity-ide\brain\98f1980c-702b-4cf6-9701-08d168f762eb\.system_generated\steps\614\content.md")

    if step_656.exists():
        with open(step_656, "r", encoding="utf-8") as f:
            raw = f.read()
        md = clean_html_to_markdown(raw, "https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/", "Things You Should Never Do, Part I", "Iconic veteran engineering wisdom, conversational authority, witty cautionary tales")
        with open(joel_dir / "things_you_should_never_do.md", "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[✓] Saved {joel_dir / 'things_you_should_never_do.md'} ({len(md)} chars)")

    if step_658.exists():
        with open(step_658, "r", encoding="utf-8") as f:
            raw = f.read()
        md = clean_html_to_markdown(raw, "https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/", "The Law of Leaky Abstractions", "Fundamental engineering philosophy, timeless architectural insight, crystal-clear prose")
        with open(joel_dir / "law_of_leaky_abstractions.md", "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[✓] Saved {joel_dir / 'law_of_leaky_abstractions.md'} ({len(md)} chars)")

    if step_614.exists():
        with open(step_614, "r", encoding="utf-8") as f:
            raw = f.read()
        md = clean_html_to_markdown(raw, "https://www.joelonsoftware.com/author/joelonsoftware/", "Joel Spolsky Recent Essays & Musings", "Relaxed elder statesman engineering humor, candid perspective on software and business")
        with open(joel_dir / "recent_musings.md", "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[✓] Saved {joel_dir / 'recent_musings.md'} ({len(md)} chars)")

    print("\n" + "=" * 70)
    print("Harvester Complete! All reference exemplars cataloged in references/style_exemplars/")
    print("=" * 70)

if __name__ == "__main__":
    main()
