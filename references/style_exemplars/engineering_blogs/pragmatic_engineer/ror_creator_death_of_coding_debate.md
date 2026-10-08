# The Pulse: RoR creator sparks new “death of coding by hand” debate - The Pragmatic Engineer

**Source**: [https://blog.pragmaticengineer.com/the-pulse-ror-creator-sparks-new-death-of-coding-by-hand-debate/](https://blog.pragmaticengineer.com/the-pulse-ror-creator-sparks-new-death-of-coding-by-hand-debate/)  
**Style Profile**: High-level industry analysis, contextualized engineering debate, balanced realism

---

Before we start: if you happen to be in San Francisco on Thursday, 5 November, join me on the [_System Update with The Pragmatic Engineer_](https://luma.com/systemupdate?coupon=TPESUB26&ref=blog.pragmaticengineer.com) event. This is an evening with OpenAI, Linear and DoorDash and myself, organized by Sentry. We get into what AI-augmented automations they’re running in prod, and how it’s going, in an off-the record (that is: not recorded!) and raw conversation. Seats are limited, and you can [_RSVP here_](https://luma.com/systemupdate?coupon=TPESUB26&ref=blog.pragmaticengineer.com).

* * *

_Hi, this is Gergely with a bonus, free issue of the Pragmatic Engineer Newsletter. In every issue, I cover Big Tech and startups through the lens of senior engineers and engineering leaders. Today, we cover one out of four topics from_[ _the last week’s issue of The Pulse_](https://pragmaticengineer.substack.com/p/the-pulse-end-of-coding-by-hand) _. Full subscribers received the article below seven days ago. If you’ve been forwarded this email, you can_[ _subscribe here_](https://newsletter.pragmaticengineer.com/about?ref=blog.pragmaticengineer.com) _._

  
The creator of Ruby on Rails, David Heinemeier Hansson, caused quite a stir last week with comments in [his Rails World keynote](https://www.youtube.com/watch?v=vDjW_dRyKXY&ref=blog.pragmaticengineer.com), when he revealed that coding by hand is dead at his company, 37signals.

This is a big deal because 37signals created Ruby on Rails, and they are known for their software craft there, especially when it comes to code quality. It’s also a business that’s 27 years old and is profitable. Despite that pedigree, DHH caused a stir among the dev community, saying:

> “**At 37signals, a couple of weeks ago, we made the decision that it clearly means we’re done writing code by hand.** We have gone pencils down on the idea that we were gonna write code by hand, as a normal course of business creating things.  
>   
> Writing code by hand at 37signals is now an exceptional state. It is like seeing a bug in Sentry: something here went wrong; why was the agent not able to produce what we wanted? Okay, maybe for a little while, we’ll still get the old pencil out and dot it down for them, but then we fix the machine, we fix the factory, we get things going again. This is a recognition of what’s already happening.”

DHH compared the maturation of AI tools into being highly capable at coding with the impact upon the craft of painting of the arrival of the camera:

> “On November 24th, 2025, we got the “Kodak Brownie” of our era. We got Opus 4.5. AI technology, accessible in a harness that many people could afford to use and experience for the first time what it’s like to create software in pairing with a new form of intelligence. This was the tipping point for me. There was everything before November 24th, and then there was everything after. This is going to be the date that history books going forward will mark as the inflection point for the age of agents.”

He shared how 37signals has embraced a future where coding by hand is almost entirely absent:

  * **Embracing native mobile apps instead of web:** famously, 37signals is bearish on native iOS and Android apps and has built web versions instead. With AI, they are betting on native apps being much easier to be built with a small team and are already building new ones.
  * **Moving backend services to Rust, not Ruby** : This is due to performance reasons and because agents write good enough Rust. That’s remarkable to hear from the creator of Ruby on Rails!
  * **Ruby on Rails remains for web apps** : 37signals is not leaving RoR behind, but only because Ruby on Rails’ convention-over-configuration design makes it easy for agents to work with it.

DHH closed by revealing that he no longer even thinks of himself as a professional programmer (emphasis mine):

> “I have retired from being a professional programmer. I think it was somewhere around 4 to 5 months ago, maybe March. I spent a quarter of a damn century chiseling code by hand and loving every moment of it. This is not something to look back upon with regret; this is something to look back upon with joy and accept that it is over.  
>   
> **Writing code by hand is no longer an economically productive enterprise for the vast majority of programmers working at the vast majority of companies**. On the other side of that is a new career as a professional maker of things, steering intelligence that was only available in science fiction up until a few moments ago.  
>   
> One of the things we’re gonna have to revisit is everything we think we know about software architecture. The main tool that we’ve used for a very long time is abstractions. Abstractions don’t make quite the same sense in the age of agents. The reason we did abstractions was in part not to repeat ourselves; well, now the price of repetition has gone to near zero.”

It’s worth noting DHH’s keynote chose a spicy topic for a conference attended by engineers who are personally and professionally invested in the craft of building software!

### **Decline of coding by hand is long predicted**

In the first issue in The Pragmatic Engineer this year, on 6 January, I [wrote](https://newsletter.pragmaticengineer.com/p/when-ai-writes-almost-all-code-what?ref=blog.pragmaticengineer.com):

> “**When AI writes almost all code, what happens to software engineering?** No longer a hypothetical question, this is a mega-trend set to hit the tech industry. (...)  
>   
> The bad news is that change will probably be rapid. It’s barely been a year since the idea of Claude Code was born in Boris Cherny’s head, and already similar tools like OpenCode, Codex, Factory, Amp, Cursor, and more capable agents are changing how software is written. Change has always been part of working in tech, but I cannot recall it being this fast, or happening across the whole industry at once!”

I concluded that this change was on its way, based on my own experience of building software with Opus-4.6 and GPT-5.2, and from talking with experienced engineers who had resisted “AI hype” for good reason, but who had come to see that AI can now generate code that’s “good enough” in many cases.

Back then, I made a few predictions about what will happen when AI agents are producing most of the code for engineers:

  * Sloppier code
  * Weak software engineering practices hurting sooner
  * “Coders” who are not software engineers see less demand
  * Tougher work-life balance for engineers
  * Junior engineers pushed to become seniors, fast
  * Computer science education increasingly required for new hires
  * A massive explosion in code and software, for which someone must be accountable

So far, it’s a messy transition and we engineers are responsible and accountable for a lot more code that we didn’t write, but which is in production anyway.

### **Non-engineers also getting into agents**

At the end of January, I [shared a deepdive](https://newsletter.pragmaticengineer.com/p/ai-first-makeover-craft?ref=blog.pragmaticengineer.com) that was pretty close to home for me: my brother’s 30-person, 15-engineer startup, Craft Docs, made its own sharp pivot to AI by building their own AI harness for non-engineers – called Craft Agents – two weeks before Claude Cowork was released, and months before ChatGPT Work launched.

Craft resisted the temptation to use AI when it did not feel productive, but with the model releases of November 2025, they found LLMs are not only useful for coding, but also for non-engineering work like customer support. In the deepdive, I went into more detail about non-engineering use cases (which engineers enabled) like:

  * Automatic triaging of bug reports with agents
  * Data enrichments added to all workflows
  * Customer support “skills” like processing feature requests
  * The marketing team building websites without devs
  * HR automating tedious work
  * Finance automating personal workflows

Craft Docs seemed early to a trend that has become more widespread, by having both their own engineering and non-engineering folks onboard to an AI harness. Now, there are signs other companies are doing the same: at OpenAI, non-engineering units like finance, recruitment, and legal moved over to Codex in June 2026:

__Non-engineering teams moved over to use OpenAI’s AI harness, Codex (now renamed to ChatGPT Work.) Source:__[__Inside OpenAI’s software factory__](https://newsletter.pragmaticengineer.com/p/openai-software-factory?ref=blog.pragmaticengineer.com)

In some ways, it could be comforting to know that it’s not only software engineering where the tools and workflows are quickly changing: every other function in tech is experiencing the same!

### **It’s messy right now**

Just last weekend, a rant by an anonymous engineer in Big Tech hit a nerve with many people in the industry. An engineer with the username voxium [posted](https://x.com/v0xium/status/2101526107128529120?ref=blog.pragmaticengineer.com) (emphasis mine):

> “The state of engineering right now is horrible. It has been half a month since I started a new role at a big company.  
>   
> Nobody knows anything here. The specs, code, tests, PRDs, tickets, resolution of those tickets, reports, etc., everything is made by Claude Code. Nobody on my team likes this.  
>   
> They are being forced to ship as much as they can. I have heard multiple times from higher management that pushing code is not a bottleneck, so why are we slow?  
>   
> People are working 12 to 13 hours a day just to press enter. Nobody is reading anything. Humans in corporate are doing nothing on their own.  
>   
> Everyone, literally everyone, from an L1 to an L7 engineer here is doing the same thing. Talk to Claude.  
>   
> **There is no sense of victory. Nobody is resolving bugs. In reality, nobody is thinking anymore.** Everything is done by LLMs. It is so soul-sucking.  
>   
> I would not mind it, to be honest, if we were at least given the time to check out the code and see what is going where. But no, the goal is to just ship. No matter what happens.”

This post rings true because it _is_ happening at many places where there’s more AI usage, engineers do “outsource” thinking to LLMs, and end up not caring about anything else except shipping _something_ to production.

### **Quality in decline**

Since the beginning of the year, [the quality of software has been degrading](https://newsletter.pragmaticengineer.com/p/are-ai-agents-actually-slowing-us?ref=blog.pragmaticengineer.com) pretty much everywhere, much of it caused by over-reliance on AI, or perhaps more accurately, the outsourcing of thinking and decision making to AI. In July, I moved my video podcast off of Spotify after a [series of unexplainable outages](https://newsletter.pragmaticengineer.com/p/the-pulse-quitting-spotify-podcasts?ref=blog.pragmaticengineer.com), and Spotify’s engineering team seemed to take no real pride or accountability in fixing the root causes of the issue.

Only this week, Uber shipped a new feature to production in the Uber Eats app – a new way to select extras with your food order – with seemingly no QA testing:

Uber Eats this week, when I attempting to order a burger. Can you spot two obvious, sloppy bugs on this page?

Inside this new “add-ons selector” in Uber Eats, I noticed three bugs at once:

  * **“Choose up to 999”** : no engineer, designer, or PM bothered to check what happens when a restaurant does not fill out a number on how many toppings to add, or adds a ridiculously large number. The most toppings that my screen allowed to be selected was six and not 999, so I could not even choose the option of 999 buns for my burger.
  * **Sloppy overflow.** A rule of thumb, during my time at Uber, was that text will never overflow, even when localized. Basilcummaynaise (basil mayo in Dutch) broke this rule but still shipped.
  * **Functional bugs in the selector.** I originally tried to order from my favorite Mexican place: a bowl with no rice or bulgur as the base. There’s the option to select “rice”, “bulgur” or “nothing” as the base, but selecting “nothing” counts as an extra side, and the app doesn’t allow the ordering of a bowl with no base.

I’ve used the Uber Eats app for years, and this was the first time I saw such a sloppy feature release. I assume that devs and PMs building it have all “checked out”, stopped doing proper QA, and assume that the agent will take care of all of it. There’s no other way to explain three bugs shipped to all customers but seemingly noticed by nobody until I [posted](https://x.com/GergelyOrosz/status/2102710141581992280?s=20&ref=blog.pragmaticengineer.com) about it. _To the Uber Eats team’s credit, they reached out and are looking into fixing all three issues._

### **Software engineering to be more important than ever**

I’m personally past the shock and grief stages of agents taking over the activity of coding. At first, I assumed this change would reduce the amount of work for engineers. But, counter-intuitively, that actually seems to be growing:

  * **We need to understand the characteristics of LLMs better.** LLMs feel familiar as they can produce text in a way only humans could do before. But they are less reliable, still prone to hallucination, suffer from capability gaslighting, and many other problems. They can also be expensive and slow.
  * **New systems need to be engineered.** Agentic “software factories” can now produce code, based on the input provided. But how is this code validated? How much can detecting defects or various issues be automated? This is a brand new area, and we need to build new types of systems, often based on old ideas. One such example is [OpenAI’s software factory](https://newsletter.pragmaticengineer.com/p/openai-software-factory?ref=blog.pragmaticengineer.com), the other one is Ramp’s [Inspect internal coding harness.](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect?ref=blog.pragmaticengineer.com)
  * **Nondeterministic LLMs can generate deterministic code.** An area I feel is under-explored and under-appreciated is the use of LLMs to substitute LLMs usage in agentic “software factories” with deterministic code they generate. For example: instead of running AI code review that is expensive and slow on all PR requests, could AI generate linters that catch the majority of common issues? If this is possible, complex lint rules would run faster, be more reliable and cheaper to execute than LLM calls.

**New categories of systems and products will be built by engineers who “get” LLMs and AI engineering.** We are seeing the majority of venture funding pour into AI companies because AI creates new business models, new revenue streams, and disrupts “traditional” software. For example, who would have thought that companies would spend tens of thousands of dollars, per engineer, on AI coding tools? Or that the category of AI inference providers would become as massive as it already is from barely existing two years ago?

This technological change will re-jig parts of the tech industry: the winners will surely win big, and teams and companies choosing inaction could be out-executed and displaced by nimble competitors. And in many ways, this is great news for us software engineers who keep up with the technology. Companies are now investing in innovation and are willing to pay top-of-market for software engineers who can help them build AI products or become AI-native.

* * *

Read the full issue of [**The Pulse this is from**](https://pragmaticengineer.substack.com/p/the-pulse-end-of-coding-by-hand)**,** or check out [**this week’s The Pulse**](https://newsletter.pragmaticengineer.com/p/the-pulse-firebases-global-outage?ref=blog.pragmaticengineer.com). This week’s issue covers:

  1. **Firebase: global outage & poor handling by Google. **The Firebase iOS SDK crashed after a backend change, crashing all apps which used Firebase analytics for 2-6 hours. Google did not update the status page or offer any postmortem, which is a head-scratcher from a company known for standout incident management practices.
  2. **OpenAI’s platform play from AWS playbook?** OpenAI is becoming a platform where it’s possible to allocate ChatGPT spend on open models and AI offerings from among 16 partners, not just OpenAI models. It’s fair to ask if Anthropic will consider a similar platform play.
  3. **More data on companies moving to open models.** Vercel’s AI gateway shows 60% of model spend goes to open weight models, and OpenRouter also shows open models are being more used than closed ones.
  4. **Why CTOs and VPEs are quitting en masse: another take.** What if it’s not “founder mode”, but about people who love building software, feeling like they can do it solo (or with a small team) with AI tools?

[Subscribe to my weekly newsletter](https://newsletter.pragmaticengineer.com/about) to get articles like this in your inbox. It's a pretty good read - and the [#1 software engineering newsletter](https://substack.com/top/technology) on Substack. 
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