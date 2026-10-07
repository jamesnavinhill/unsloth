# DATA SPECIFICATION — High-Continuity Humanizer (v1.0)

**Date**: 2026-10-07  
**Companion Documents**: [`plan.md`](../plan.md) (Decisions D2, D5), [`datasets/LEDGER.md`](LEDGER.md), [`ORCHESTRATION.md`](../ORCHESTRATION.md).

---

## 1. Product Vision & Use Case

This project does **not** build an AI detector bypasser, nor does it generate cold, machine-like AST structures.

The target is an **Agent-to-Human & Public-Facing Engineering Prose Humanizer**:
- **Agent Work Updates**: Meaty, accumulative updates from autonomous coding agents to human operators summarizing complex multi-step work, decisions made, tradeoffs evaluated, and next steps.
- **Pull Request Descriptions**: Short executive summaries and long architectural overviews that clearly explain *why* changes occurred and their exact impact.
- **Changelogs & Release Notes**: High-context, human-readable announcements that inform users and engineers without robotic buzzwords.
- **Technical Documentation**: Authoritative, concise, and delightfully human-readable docs.
- **Editorial / Creative Copy**: Modernized longform essays, persuasive copy, and narratives that shatter the hypnotic, monotone LLM drone.

---

## 2. Benchmark Exemplars & Target Tones

### 2.1 The Engineering Continuity Benchmark (The "Top 3" Model)
We model our technical and agent-continuity outputs on the highest-caliber engineering communicators in the software industry:

| Benchmark Organization | Tone & Architectural Qualities | Target Application in Humanizer |
|---|---|---|
| **Stripe** | Effortless clarity, respectful of reader time, deep technical precision, zero corporate throat-clearing. | Documentation, API descriptions, architectural overviews. |
| **Linear** | Opinionated, crisp, high-context, fast-scannable, active verbs, zero bureaucratic fluff. | Changelogs, PR summaries, agent work progress logs. |
| **Basecamp / 37signals / Cloudflare** | Direct, human, conversational authority, explains causal reasoning (*"We changed X because Y, resulting in Z"*). | Post-mortems, accumulative agent handoffs, issue descriptions. |

#### Concrete Transformation Target:
* **Robotic LLM Baseline**:
  > *"Certainly! In this pull request, we have comprehensively implemented a multifaceted suite of optimizations across the data ingestion pipeline. It is important to note that these changes not only improve throughput, but also ensure scalability..."*
* **High-Continuity Humanizer (Target)**:
  > *"This PR resolves the 400ms ingestion bottleneck by batching database writes in 500-record chunks and pre-compiling the regex filters. Across our local benchmarks, throughput doubled without increasing peak memory. All existing integration tests pass without changes."*

---

### 2.2 The Modernized Editorial & Narrative Benchmark
For creative writing, blog posts, and longform copy, we borrow core structural principles from literary masters (burstiness, texture, asymmetry, active verbs), modernized for contemporary longform prose (e.g. *Stripe Press*, *Increment*, *The Verge* features, *Wired* longform):

1. **Syntactic Burstiness**: Sentence lengths vary dynamically from 3 words to 40+ words. The rhythm feels intentional and alive.
2. **Asymmetry**: Rejection of symmetrical tri-colon lists (*"speed, reliability, and security"*).
3. **Concrete Nouns & Verbs**: Banning corporate abstractions (*"synergy"*, *"transformative landscape"*, *"delve into the realm"*).
4. **Natural Grounding**: Eliminating throat-clearing markers (*"In conclusion"*, *"Furthermore"*, *"It is crucial to remember"*, *"A testament to"*).

---

## 3. The Dataset Pipeline Architecture

```
┌────────────────────────────────┐
│   Raw Traces (Inputs)          │
│ - LiteLLM Gateway Agent Logs   │
│ - Public Traces (WildChat/PRs) │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   Fact & Claim Extraction      │
│ - Identify invariants & facts  │
│ - Prevent hallucination/loss   │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐       ┌───────────────────────────────────┐
│   Rewriter Engine              │ <──── │   Style Packs                     │
│ (Nemotron-3 550B / GPT-OSS)    │       │ - Stripe / Linear / GitHub Packs  │
│ - Conditioned on Style Pack    │       │ - Modernized Literary Exemplars   │
└───────────────┬────────────────┘       │ - Strict Banned Lexicon (Clichés) │
                │                        └───────────────────────────────────┘
                ▼
┌────────────────────────────────┐
│   Automated Quality Gates      │
│ 1. Fact-Fidelity Judge (≥98%)  │
│ 2. 5-Gram Non-Duplication (<15)│
│ 3. Burstiness & Naturalness    │
└───────────────┬────────────────┘
                │
                ▼
┌────────────────────────────────┐
│   Training Pair Output         │
│ (Trace Input -> Human Target)  │
└────────────────────────────────┘
```

---

## 4. Implementation Tasks Mapping

* **T5 (Archive Triage)**: Filter Gutenberg and public-domain corpora to isolate high-burstiness, natural prose chunks; drop dry Victorian OCR artifacts.
* **T6 (CC Sourcing)**: Sample contemporary, high-quality technical and editorial text from the Common Crawl Creative Commons bucket.
* **T7 (Rewriter Selection)**: Benchmark Agency Gateway models (`or-nvidia-nemotron-3-ultra-550b`, `ne-gpt-oss-120b`, `or-liquid-lfm-2.5-2.6b`) on 20 sample PR/docs/agent-trace rewrites.
* **T8 (Style Pack Construction)**: Assemble the curated exemplar sets (Stripe-style docs, Linear-style changelogs, modernized essay packs).
* **T9 (Batch Production)**: Execute batch generation through Gateway, run automated gates, and upload private training datasets to Hugging Face Hub.
