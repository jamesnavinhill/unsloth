# Style Exemplar Library — Reference Index

This directory contains curated, authentic human prose from leading engineering teams and classic technical essayists. These exemplars ground our rewriter prompts and fine-tuning targets for `LiquidAI/LFM2.5-2.6B`.

---

## Directory Layout

```
references/style_exemplars/
├── tech_docs/
│   ├── docker/               # Multi-stage builds, container foundations
│   ├── fly_io/               # MicroVM Fly Machines, CLI app launch
│   ├── linear/               # GitHub sync workflow, getting started guide
│   ├── plaid/                # Plaid Link onboarding, Auth product mechanics
│   ├── render/               # Deploy hooks, Web services architecture
│   └── stripe/               # Idempotent requests, Webhooks architectural guide
├── changelogs/
│   ├── fly_io/               # Platform releases
│   ├── linear/               # High-velocity product changelog
│   └── stripe/               # API version release notes and deprecation logs
└── engineering_blogs/
    ├── daily_wtf/            # Goodhart's law satirical lore, process horror
    ├── dan_luu/              # Productivity & velocity analysis, corporate blog dissection
    ├── fly_io/               # MCP agent infrastructure, defensive agent architecture, SQLite VFS
    ├── joel_on_software/     # "Things You Should Never Do", "Law of Leaky Abstractions", modern musings
    ├── julia_evans/          # SQLite internals curious walkthrough, Django pragmatic tooling
    ├── posthog/              # ClickHouse vs Postgres benchmarks, 63M MCP agent analysis, product loops (non-Ian)
    ├── pragmatic_engineer/   # Coding by hand debate, hardware CPU shortage analysis
    ├── simon_willison/       # Fast practitioner evaluation of frontier models
    └── travis_downs/         # Hardware speed limits, low-level CPU cache and memory benchmarks
```

---

## 1. Technical Documentation

| Source | File | Key Style Profile |
|---|---|---|
| **Stripe** | [`idempotent_requests.md`](tech_docs/stripe/idempotent_requests.md) | High-precision technical clarity, respect for engineer time, zero fluff. |
| **Stripe** | [`webhooks_overview.md`](tech_docs/stripe/webhooks_overview.md) | Architectural guidance, concrete causal reasoning, defensive edge cases. |
| **Linear** | [`github_integration.md`](tech_docs/linear/github_integration.md) | Opinionated developer workflows, crisp active verbs, seamless scannability. |
| **Linear** | [`start_guide.md`](tech_docs/linear/start_guide.md) | Fast-onboarding clarity, modern minimalist phrasing. |
| **Plaid** | [`link_quickstart.md`](tech_docs/plaid/link_quickstart.md) | Developer-first onboarding, clean step sequences, explicit parameter docs. |
| **Plaid** | [`auth_product.md`](tech_docs/plaid/auth_product.md) | Protocol mechanics, structured error contracts, zero boilerplate. |
| **Render** | [`deploy_hooks.md`](tech_docs/render/deploy_hooks.md) | Direct cloud primitives, clear curl/webhook examples, pragmatic operations. |
| **Render** | [`web_services.md`](tech_docs/render/web_services.md) | Infrastructure architecture, transparent defaults, operational clarity. |
| **Docker** | [`multi_stage_builds.md`](tech_docs/docker/multi_stage_builds.md) | Production optimization, step-by-step causal tradeoffs. |
| **Docker** | [`what_is_a_container.md`](tech_docs/docker/what_is_a_container.md) | Foundational architecture, concrete analogies, clear boundary definitions. |
| **Fly.io** | [`fly_machines_overview.md`](tech_docs/fly_io/fly_machines_overview.md) | Deep virtualization realism, wry conversational tone, fast microvm mechanics. |
| **Fly.io** | [`launch_quickstart.md`](tech_docs/fly_io/launch_quickstart.md) | Direct developer CLI onboarding, no ceremony, transparent infrastructure. |

---

## 2. Changelogs & Release Notes

| Source | File | Key Style Profile |
|---|---|---|
| **Linear** | [`linear_recent_changelog.md`](changelogs/linear/linear_recent_changelog.md) | Feature-velocity storytelling, bulleted architectural impact, zero corporate buzzwords. |
| **Stripe** | [`stripe_api_changelog.md`](changelogs/stripe/stripe_api_changelog.md) | Breaking change clarity, deterministic dates, version deprecation explanations. |
| **Fly.io** | [`fly_platform_changelog.md`](changelogs/fly_io/fly_platform_changelog.md) | Platform update summaries, engineer-to-engineer transparency. |

---

## 3. Engineering Lore & Blogs

| Author / Org | File | Key Style Profile |
|---|---|---|
| **Fly.io** | [`sprites_mcp.md`](engineering_blogs/fly_io/sprites_mcp.md) | Wry, irreverent, brilliant infrastructure commentary; treating AI tooling with veteran systems realism. |
| **Fly.io** | [`building_agents_that_dont_break.md`](engineering_blogs/fly_io/building_agents_that_dont_break.md) | Defensive software engineering, agent autonomy limits, clear causality. |
| **Fly.io** | [`litestream_writable_vfs.md`](engineering_blogs/fly_io/litestream_writable_vfs.md) | Deep database systems internals, SQLite virtual filesystem engineering. |
| **PostHog** | [`clickhouse_vs_postgres.md`](engineering_blogs/posthog/clickhouse_vs_postgres.md) | Pragmatic data engineering tradeoffs, raw benchmark numbers, humorous candor. |
| **PostHog** | [`how_ai_agents_behave.md`](engineering_blogs/posthog/how_ai_agents_behave.md) | Empirical data breakdown across 63M tool calls, cynical pattern observations. |
| **PostHog** | [`self_driving_loops.md`](engineering_blogs/posthog/self_driving_loops.md) | Operational product engineering, iterative execution philosophy. |
| **Joel Spolsky** | [`things_you_should_never_do.md`](engineering_blogs/joel_on_software/things_you_should_never_do.md) | Iconic veteran engineering wisdom, conversational authority, witty cautionary tales. |
| **Joel Spolsky** | [`law_of_leaky_abstractions.md`](engineering_blogs/joel_on_software/law_of_leaky_abstractions.md) | Fundamental engineering philosophy, timeless architectural insight, crystal-clear prose. |
| **Joel Spolsky** | [`recent_musings.md`](engineering_blogs/joel_on_software/recent_musings.md) | Relaxed elder statesman engineering humor, candid perspective on software and business. |
| **Dan Luu** | [`productivity_velocity.md`](engineering_blogs/dan_luu/productivity_velocity.md) | Deep empirical analysis, intellectual honesty, dissection of corporate mythology. |
| **Dan Luu** | [`corporate_eng_blogs.md`](engineering_blogs/dan_luu/corporate_eng_blogs.md) | Candid critique of sanitized PR vs genuine engineering writing. |
| **Travis Downs** | [`performance_speed_limits.md`](engineering_blogs/travis_downs/performance_speed_limits.md) | Low-level CPU performance lore, microbenchmarking discipline, hardware reality. |
| **Julia Evans** | [`learning_running_sqlite.md`](engineering_blogs/julia_evans/learning_running_sqlite.md) | Wonderfully approachable curiosity, demystifying complex technical machinery. |
| **Julia Evans** | [`more_nice_django_things.md`](engineering_blogs/julia_evans/more_nice_django_things.md) | Opinionated practitioner experience, pragmatic tooling praise. |
| **Simon Willison** | [`claude_haiku_5_5.md`](engineering_blogs/simon_willison/claude_haiku_5_5.md) | Concise practitioner commentary, immediate empirical testing, personal perspective. |
| **Pragmatic Eng.** | [`ror_creator_death_of_coding_debate.md`](engineering_blogs/pragmatic_engineer/ror_creator_death_of_coding_debate.md) | High-level industry analysis, contextualized engineering debate, balanced realism. |
| **Pragmatic Eng.** | [`cpu_shortages_pulse.md`](engineering_blogs/pragmatic_engineer/cpu_shortages_pulse.md) | Hardware macro trends, direct sourcing, investigative engineering journalism. |
| **The Daily WTF** | [`what_you_measure.md`](engineering_blogs/daily_wtf/what_you_measure.md) | Dry satirical wit, cautionary engineering folklore, Goodhart's law in practice. |
| **The Daily WTF** | [`part_1_of_the_process.md`](engineering_blogs/daily_wtf/part_1_of_the_process.md) | Classic developer horror storytelling, deadpan humor, bureaucratic comedy. |
