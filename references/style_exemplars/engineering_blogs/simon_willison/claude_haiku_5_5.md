# Claude Haiku 5.5

**Source**: [https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/](https://simonwillison.net/2026/Oct/7/claude-haiku-5-5/)  
**Style Profile**: Concise practitioner commentary, immediate empirical testing, personal perspective

---

## Claude Haiku 5.5

7th October 2026

As previously [promised](https://simonwillison.net/2026/Sep/28/claude-sonnet-5-5/), here’s Anthropic’s new fast, low cost model: [Introducing Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5).

The previous Haiku, 4.5, was very much showing its age. It came out [almost a year ago](https://simonwillison.net/2025/Oct/15/claude-haiku-45/), and was priced at $1/million input and $5/million output—relatively expensive even back then, and a full 10x the price of OpenAI’s [GPT-6 Luna](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/#gpt-6-sol-and-luna-are-half-the-price-of-their-gpt-5-6-equivalents), released last month.

The new Haiku exactly matches the price of GPT-6 Luna—$0.10/$0.50—up to 100,000 tokens. Beyond 100,000 tokens the price increases 5x to $0.50/$2.50. Luna itself has a price increase at 272,000 tokens but only to $0.20/$0.75.

Haiku 5.5 also uses a new, less generous tokenizer. My [Claude Token Counter](https://tools.simonwillison.net/claude-token-counter) tool shows that the same long prompt uses around 1.25x as many tokens with Haiku 5.5 compared to Haiku 4.5, so there’s a hidden price increase there.

If your workloads fit in 100,000 tokens, Haiku is the same price as Luna and reports higher benchmark scores. Above 100,000 tokens, Luna looks like a much better deal.

The [most recent release of llm-anthropic](https://github.com/simonw/llm-anthropic/releases/tag/0.30) finally fixed it so I don’t need to ship a new version of that plugin for every new model. I tested the new model like this:
    
    
    llm install -U llm-anthropic
    llm anthropic refresh
    llm -m claude-haiku-5.5 "Generate an SVG of a pelican riding a bicycle" -o thinking_effort low
    

#### Pelicans

Here are [pelicans for low, medium, high, xhigh, and max](https://tools.simonwillison.net/markdown-svg-renderer?url=https%3A%2F%2Fgist.github.com%2Fsimonw%2F485dfa24b4efa1267ee2d0911594fb81). The new Haiku doesn’t let you disable reasoning, and defaults to `medium`. I got a good bicycle frame for everything beyond `low`. The [low effort pelican](https://tools.simonwillison.net/markdown-svg-renderer?url=https%3A%2F%2Fgist.github.com%2Fsimonw%2F485dfa24b4efa1267ee2d0911594fb81#response) cost 0.0936 cents and took 7 seconds.

This `max` effort pelican (with [a reasoning trace](https://tools.simonwillison.net/markdown-svg-renderer?url=https%3A%2F%2Fgist.github.com%2Fsimonw%2F485dfa24b4efa1267ee2d0911594fb81#reasoning-3) that starts “This is the classic pelican-on-bicycle SVG test...”) took 5 minutes 9 seconds to generate, but still only cost me [3.3826 cents](https://www.llm-prices.com/#it=27&ot=67647&sel=claude-haiku-5.5):

(Since the reasoning trace exhibits awareness of the benchmark, here’s [Generate an SVG of an armadillo in fishnet tights jaywalking on Mars (on xhigh)](https://tools.simonwillison.net/markdown-svg-renderer?url=https%3A%2F%2Fgist.github.com%2Fsimonw%2F375ae4f2bb68999976b8da50548c788d#response), and the same prompt against [some other recent models](https://tools.simonwillison.net/markdown-svg-renderer?url=https%3A%2F%2Fgist.github.com%2Fsimonw%2F18c9f7fc3b3705cf88514cb9170ec246). [Background on that](https://news.ycombinator.com/item?id=49977979#49982139).)

For comparison, here’s the pelican I got [a year ago](https://simonwillison.net/2025/Oct/15/claude-haiku-45/) from Haiku 4.5 (for [0.7583 cents](https://www.llm-prices.com/#it=18&ot=1513&ic=1&oc=5)—Haiku 4.5 did not support reasoning levels). It _sucked_ at drawing pelicans:

#### And a generous API credit scheme for subscribers

In addition to Haiku 5.5, Anthropic announced today that they are halving the price of cache reads for Sonnet 5.5. They’ve also added API credits to subscription plans:

> Second, this week, we’ll roll out **a new monthly API credit to all Max and Team subscribers for use on the Claude Platform**. Max 5x users will get $100 in credits per month, Max 20x users will get $200, and Team subscribers will receive up to $500, pooled across their users.

Claiming this is pleasantly easy: navigate to [Settings -> Billing](https://claude.ai/new#settings/billing) and select the API organization that should benefit from the credits every month:

The API credits exactly match the cost of the subscription itself. This is really generous—it makes it much easier for subscribers to use the API. Anthropic also let you disable auto-reload for the API, with the consequence that “API requests will stop when your balance runs out”—exactly what you want if you’re planning to burn through those API credits without [risk of a nasty billing surprise](https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/).

Note that the monthly credits [do not roll over](https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-and-team-plans#h_dfc1659cee)—use them or lose them.

OpenAI still allow you to use your Codex subscription for personal API use, which works out as a better deal for heavy API users. This new credit scheme goes at least some way to overcoming that difference.

Posted [7th October 2026](/2026/Oct/7/) at 8:56 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)
  *[ M1]: The first generally available Apple CPU ("Apple Silicon") for laptops with 4 Firestorm and 4 Icestorm cores.
  *[uop]: Micro-operation: instructions are translated into one or more uops, which are simple operations executed by the CPU's execution units.
  *[macro-fuse]: The fusing of an ALU operation and subsequent jump, such as `dec eax; jnz label` into one operation
  *[macro-fused]: The fusing of an ALU operation and subsequent jump, such as `dec eax; jnz label` into one operation
  *[uarch]: Microarchitecture: a specific implementation of an ISA, e.g., "Haswell microarchitecture".
  *[p1]: port 1 (GP and SIMD ALU, integer mul)
  *[p6]: port 6 (GP ALU, all branches)
  *[immediate]: When discussing assembly instructions an immediate is a value embedded in the instruction itself, e.g., the 1 in add eax, 1.
  *[p5]: port 5 (GP and SIMD ALU, vector shuffles)
  *[p0]: port 0 (GP and SIMD ALU, not-taken branches)
  *[M1]: The first generally available Apple CPU ("Apple Silicon") for laptops with 4 Firestorm and 4 Icestorm cores.
  *[naturally aligned]: Naturally aligned data is data whose location in memory is a multiple of its size, e.g., a 4 byte element whose address is a multiple of 4 bytes.
  *[AGU]: Address Generation Unit
  *[p2]: port 2 (load/store AGU)
  *[p3]: port 3 (load/store AGU)
  *[p7]: port 7 (limited store AGU)
  *[CNL]: Intel's Cannon Lake (client) architecture, the i3-8121U was the only SKU ever released
  *[SKX]: Intel's Skylake (server) architecture including Skylake-SP, Skylake-X and Skylake-W
  *[SKL]: Intel's Skylake (client) architecture, aka 6th Generation Intel Core i3,i5,i7
  *[HSW]: Intel's Haswell architecture, aka 4th Generation Intel Core i3,i5,i7
  *[out-of-order]: Out-of-order execution allows CPUs to execute instructions out of order with respect to the source.
  *[MSROM]: Intel's name for the microcode engine: a component handles complex instructions which require more than 4 uops using microcode which feeds uops directly into the IDQ.
  *[MITE]: Intel's name for the "legacy" decoder, i.e., the decoder that usually decodes instructions when they are not found in the MSROM.
  *[microcode]: Internal instructions and other logic forming part of a CPU which may be used to implement user-visible instructions and control other aspects of CPU behavior and which may be modified dynamically by vendor-provided updates.
  *[LSD]: Lysergic acid diethylamide or Loop stream detector, but in the context of this blog probably the latter: The so-called loop buffer that can cache small loops of up to ~64 uops on recent Intel architectures. Not actually a separate structure: the hardware justs locks the loop down in the IDQ.
  *[basic block]: a straight-line code sequence with no branches in except to the entry and no branches out except at the exit (Wikipedia).
  *[OoO]: Out-of-order execution allows CPUs to execute instructions out of order with respect to the source.
  *[Sunny Cove]: The new 7nm microarchitecture used in Ice Lake CPUs.
  *[Firestorm]: The big, high IPC cores in the Apple M1 CPU.
  *[Icestorm]: The low power efficiency cores in the Apple M1 CPU.
  *[ROB]: Re-order buffer: n ordered buffer which stores in-progress instructions on an out-of-order processor.
  *[IPC]: Instructions per cycle: calculated over an interval by measuring the number of instructions executed and the duration in cycles.
  *[MLP]: Memory level parallelism: having multiple misses to memory outstanding from a single core. When used as a metric, it refers to the average number of outstanding requests over some period.
  *[demand load]: A true load that appears in the source code or assembly, as opposed to loads initiated by software or hardware prefetch.
  *[PRF]: Physical register file: The hardware registers used for renaming architectural (source visible) registers, usually much larger in number than the architectural register count.
  *[SIMD]: Single Instruction Multiple Data: an ISA type or ISA extension like Intel's AVX or ARM's NEON that can perform multiple identical operations on elements packed into a SIMD register.
  *[GP]: General purpose: as opposed to SIMD or FP. On x86 often refers to instructions such as integer addition, or registers such as eax.
  *[delamination]: An situation where an instruction using an indexed addressing mode, that is otherwise eligible for micro-fusion, stays fused in the uop-cache, but then delaminates into two separate uops prior to issue, and so counts as two against the pipeline (rename) limit of four uops.
  *[IDQ]: Queue that collects incoming instructions from the decoder, uop cache or microcode engine and delivers them to the renamer (RAT).
  *[RMW]: Read-modify-write: an instruction that reads from a memory location, operates on the value, and writes the result back to the same location.