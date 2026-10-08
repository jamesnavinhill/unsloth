# The Pulse: a new trend of CPU shortages - The Pragmatic Engineer

**Source**: [https://blog.pragmaticengineer.com/the-pulse-a-new-trend-of-cpu-shortages/](https://blog.pragmaticengineer.com/the-pulse-a-new-trend-of-cpu-shortages/)  
**Style Profile**: Hardware macro trends, direct sourcing, investigative engineering journalism

---

_Hi, this is Gergely with a bonus, free issue of the Pragmatic Engineer Newsletter. In every issue, I cover Big Tech and startups through the lens of senior engineers and engineering leaders. Today, we cover one out of four topics from_[ _a past issue of The Pulse_](https://pragmaticengineer.substack.com/p/the-pulse-191-a-new-trend-of-cpu) _. Full subscribers received the article below fourteen days ago. If you’ve been forwarded this email, you can_[ _subscribe here_](https://newsletter.pragmaticengineer.com/about?ref=blog.pragmaticengineer.com) _._

I was at dinner with a bunch of CTOs and Head of Infrastructure folks recently, and from the conversation it was clear that many companies are struggling to source CPUs in the current climate, and are coming to terms with the end of juicy discounts from cloud providers for machines in the new era of surging demand fueled by AI.

The ‘memory crisis’ afflicting sectors like video gaming is well established and has been extensively covered in terms of shortages of GPUs, but now it seems like things are just as hard for businesses in need of CPUs from cloud providers.

In a sign of how things are changing, the disappearance of CPU spot pricing was mentioned at the table. Customers used to be able to pay up to 90% less than the standard price for CPUs, as cloud providers slashed CPU prices for machines that were lying dormant and unused. But that’s no longer the case. It seems that spot pricing has vanished because there’s no longer any lack of demand for CPUs – quite the opposite.

I was surprised, but a lot of people chimed in; apparently, it’s now nearly impossible to get CPUs on spot instances without long-running connections with cloud providers. Also, reserving specific CPUs now needs to be done months in advance, and cloud providers will even turn down certain reservations because they don’t have enough CPUs or the right type of CPUs.

### **Even big players struggle to reserve CPUs**

I have asked turbopuffer CEO Simon Eskildsen about their experience of CPU availability in the cloud, since turbopuffer, as a product, runs on CPUs, not GPUs. They operate in AWS, GCP, and Azure, so I asked how easy it is to get CPUs these days. Simon’s response:

> “**Getting CPUs is not easy anymore.** As Reinforcement Learning (RL) is becoming a large amount of the workloads: RL needs a lot of CPUs. So the labs are sucking up a lot of CPUs. During RL, they need to teach the models how to do things, like searching, and then they need the model to run software, which then takes CPUs to run.  
>   
> Then, outside of RL, agents need to do all kinds of very general purpose things on a CPU. So as the demand curve is shifting to general purpose agents, CPU demand is also going up.  
>   
> **Even the big companies are fighting each other for the right to get the CPU allocations.** I would assume that it gets a lot worse before it gets better on the CPU side.”

I was able to confirm what Simon said about larger companies struggling; a VP of Engineering at a large inference provider told me they are at the limit on how much GPU and CPU capacity they can buy from their cloud providers. They have cash to spend and want to rent more capacity, and are willing to accept the longest leases. Despite that, cloud providers tell them no more is available!

### **AI hogging CPUs**

Katelyn Lesse, Head of Platform Engineering for Claude Platform, has [written about](https://x.com/katelyn_lesse/status/2097092193194541234?ref=blog.pragmaticengineer.com) the reasons for the massive CPU demand increase:

> “In the past few years, AI-fueled demand has skyrocketed, and these few companies suddenly needed multiple years and tens of billions of dollars to actually add enough capacity. We ended up with 3 separate bottlenecks in factory capacity that AI is exacerbating. At TSMC, GPUs are competing with CPUs (and with Apple, Qualcomm, and Broadcom) for production lines. And at SK Hynix, Samsung, and Micron, HBM [High Bandwidth Memory] is competing with regular DRAM for wafers.  
>   
> What we’ve ended up with is CPUs getting squeezed from both sides. AMD doesn’t own fabs [semiconductor fabrication plants], so its CPUs need to come out of TSMC’s constrained allocation. Intel does own fabs, but it’s been working through yield problems and is now pulling some of its capacity from PC chips in order to make more server chips. And CPUs need DRAM which has gotten more expensive because memory production has shifted toward HBM. Analysts are expecting CPU supply to add more comfortable headroom before memory does, but their expectation is that it’s still going to be multiple quarters away.”

AI-fueled demand does increase CPU load, as shown in this graph from Uber, displaying the growth in agent requests over the past six months:

__Ninefold increase in agentic requests over six months. Source:__[__Uber__](https://www.uber.com/us/en/blog/efficient-software-factory/?ref=blog.pragmaticengineer.com)

Increasingly, “agent requests” not only generate code which is inference-heavy – and therefore needs GPUs – but they also run tools that compile the code, run tests, run linters, and all of this is CPU-heavy. At companies like Uber, Ramp, and others, AI agents no longer run on the dev’s local machine, but on a dedicated instance in the cloud. So, the companies reserve more CPUs on their respective cloud providers for agentic workloads. _We recently covered_[ _how Ramp built and runs its cloud agent, Inspect._](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect?ref=blog.pragmaticengineer.com)

Basically, the problem is:

  * **AI applications use more and more CPUs,** thanks to agents running a lot more software. AI data centers used to have a ratio of 1 CPU to 8 GPUs. Now the ratio is more 1:4, and it could shrink to 1:1.
  * **Companies that can manufacture more CPUs are busy on other hardware.** TSMC is busy producing GPUs, which might be more profitable than CPUs. Meanwhile, CPUs also need DRAM, but DRAM manufacturers (SK Hynix, Samsung, and Micron) are instead producing high-bandwidth memory (HBM) because it’s more profitable. This is why [memory prices are spiking](https://newsletter.pragmaticengineer.com/i/183931240/spiking-memory-prices-and-big-tech-unable-to-buy-ram?ref=blog.pragmaticengineer.com); even Big Tech is unable to buy RAM, as previously covered.

**To secure CPUs, it’s necessary to do capacity planning up to 12 months in advance.** Katelyn says that server orders are being fulfilled in ~six months, instead of 1-2 weeks’ time as previously, and that prices are up by between 10-20%. So, it’s probably time for capacity planning. [Katelyn](https://x.com/katelyn_lesse/status/2097092193194541234?ref=blog.pragmaticengineer.com):

> “Most of us have never capacity-planned CPUs. We planned databases, we maybe planned accelerators if we needed them, and we autoscaled on-demand into CPU capacity as much as our budgets allowed us to. But general purpose compute is now something many teams will need to commit to ahead of time, which means you should probably start to forecast and plan around it. If you’re operating at scale, there are some things to spend your energy on.”

**Using existing CPUs more efficiently is something to do, as of now.** The CPU capacity shortage won’t go away, and any new CPU allocations requested could take months to turn up. So, what can we do if new capacity lags? One option is utilizing current resources more efficiently!

This is a great time to review and to establish now which services are CPU-intensive, and whether or not they _need_ to be. Also check on services which are utilizing little CPU: can they run on fewer nodes, so that some CPU capacity can be allocated to services that need it more?

**The best time to secure more CPU capacity is most certainly _right now_. **I’m hearing rumors that certain cloud regions no longer accept new tenants because all CPU capacity is leased, or negotiations elsewhere are difficult. I’m also hearing that customers are already paying _today_ to reserve capacity that will only come online in data centers from December. This seems predatory by providers, but demand is so high that this is how they likely prioritize new capacity allocation – _while_ _earning much higher profits than usual._

If your company has dynamic workloads, and you’ve used spot instances in the past, now could be a good time to allocate fixed capacity – even if it’s more expensive. If you expect meaningful growth, doing so now might mean having options at some cloud providers or in some regions.

It seems like this issue has spread everywhere as a corollary of widespread AI adoption. There’s a GPU shortage, memory shortage, and now a growing CPU shortage as well. Back at the end of last year, there was even an [hard drive shortage](https://www.tomshardware.com/pc-components/hdds/ai-triggers-hard-drive-shortage-amidst-dram-squeeze-enterprise-hard-drives-on-backorder-by-2-years-as-hyperscalers-switch-to-qlc-ssds?ref=blog.pragmaticengineer.com). _The only compute primitive not in short supply seems to be networking!_

* * *

Read the full issue of [**The Pulse this is from**](https://pragmaticengineer.substack.com/p/the-pulse-191-a-new-trend-of-cpu)**,** or check out [**this week’s The Pulse**](https://newsletter.pragmaticengineer.com/p/the-pulse-end-of-coding-by-hand?ref=blog.pragmaticengineer.com). This week’s issue covers:

  1. **Writing code by hand: is it over?** In his Rails World keynote, David Heinemeier Hansson (DHH) declared the end for writing code by hand for professional work – at 37Signals at least. Is this change now unstoppable?
  2. **Amazon and Meta struggle to hire and keep engineers.** Both Big Tech companies are scrambling to hire engineers who they previously laid off or enforced job reassignment upon. It seems experienced engineers remain in demand after all.
  3. **Opus 5.5 released and it’s good.** Anthropic has released its new model that’s 40% the cost of using Fable 5.1 and has superior coding capability.
  4. **Code reviews to vanish sooner rather than later?** Marc Brooker, Distinguished Engineer at AWS, believes that humans will have no role in routinely reviewing code by hand, and explains why this is all but inevitable.

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