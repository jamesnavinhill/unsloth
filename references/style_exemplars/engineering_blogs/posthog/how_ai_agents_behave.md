# How AI agents behave: lessons from 63M MCP tool calls

**Source**: [https://posthog.com/blog/how-ai-agents-behave](https://posthog.com/blog/how-ai-agents-behave)  
**Style Profile**: Empirical data breakdown across 63M tool calls, cynical pattern observations

---

Copy page

# How AI agents behave: lessons from 63M MCP tool calls

  * [Natalia Amorim](/community/profiles/35321)

Sep 30, 2026

  * [Studies](/blog/studies)

#### Contents

  * Half of all agent traffic is Anthropic
  * Agents ignore 95% of what we built
  * Agents create 2.5x more insights than humans
  * Codex makes the fewest mistakes
  * 0.5% of calls cost 18% of the tokens
  * You can't improve what you're not measuring

 _(in my best David Attenborough voice):_ And here, in its natural habitat, we observe a new species of user emerging. It has no face and needs no mouse, it does not doomscroll or rage-click. Instead, the AI agent approaches quietly through an [MCP server](/docs/model-context-protocol), reaching into the product to forage for data on behalf of its human. 

We're not describing a particularly mature ecosystem, but rather one that's being born, in real time, on our doorsteps. 

And so, like any responsible naturalists, we began observing it (by which we mean digging through our data to see what these agents are up to).

In the 90 days up to to September 16, agents made **63 million tool calls** to [PostHog's MCP](/mcp), coming from **130,000 people**.1

## Half of all agent traffic is Anthropic

 _First, a caveat: when we first looked into the data, almost half of it traffic was us.[PostHog Desktop](/desktop), the [CLI](/docs/cli), the [Slack app](/slack), and our [Signals scouts](/docs/self-driving/signals) all reach the same MCP server as everyone else, and the scouts in particular never sleep. So for this section we've set our own agents aside and looked only at the **55%** that comes from people using their own tools.2_

In this timeframe, **Claude Code** was the biggest caller, making up **32% of third-party calls**. OpenAI's **Codex** was second at **22%** , then **Cursor** at 10%, **Cowork** at 7%, and a long tail of Claude Desktop, Claude.ai, ChatGPT, and Claude's Agent SDK at 2–3% each.

Roll it up by vendor and it's simpler: **Anthropic surfaces make up about 50% of all third-party calls, OpenAI 25%** , Cursor 10%, and everyone else fights over what's left.

About **14%** of calls come from clients we can't place at all: homegrown scripts, unnamed bots, and agents that don't introduce themselves (rude).

Include our own agents and the picture inverts, by the way: our scouts run on Codex, which makes Codex 62% of _all_ traffic. Just not a very interesting 62%.

The agent poking at your product almost certainly isn't in a chat window; it's in someone's code editor or terminal, running commands. **Only about 7% of calls come from a chat window.**

##  Agents ignore 95% of what we built

What do agents want? Turns out, not much (at least not in terms of variety). Sixty-three million calls, and it mostly comes down to two moves: **running a SQL query** (15.6 million calls – 25% of everything) and **reading the schema** to find out what's queryable in the first place (another 7%).

Between them, those two are 32% of all traffic. 

It's worth knowing there are three doors an agent can take to ask our MCP a data question:

  1. It can write raw SQL. 
  2. It can call one of our typed **query wrappers** – trends, funnels, retention – and skip the SQL entirely (3% of calls).
  3. It can go through **product analytics** proper: creating, reading, and updating saved insights (another 3%). 

Agents overwhelmingly pick the first door. SQL gets about four times the traffic of the other two put together.

Reading the schema tells an agent what's in your data (which events you capture, what properties they carry). But another **4.5%** of calls is the step before that: pulling up a skill, or searching the docs to work out how a particular tool wants to be called. 

So **about 5% of calls are an agent looking something up rather than doing something.**

A lot of our tools barely register, which is a little tragic, because [PostHog's MCP](/mcp) has hundreds of different functionalities available. 

Give an agent a single prompt and it could [spin up an A/B test](/experiments) today and ship the winning variant next week. It could open an error, [read the stack trace](/error-tracking), jump to the [exact replay](/session-replay) of the user who hit it, and patch the code. It could [point an AI at a week of sessions and ask questions about it](/replay-vision). The list goes on.

This is partly a note to self (we should advertise these better) and partly advice for anyone building an MCP: the good stuff needs to be discoverable.

If you want agents near the best parts of your product, you have to surface those tools legibly enough that a person remembers to point at them, but also so that an agent can find them without being told. 

Otherwise the best thing you built stays underwater, and nobody knows it's there.

## Agents create 2.5x more insights than humans

In the last 30 days, **agents created 252,000 insights through the MCP. People created 99,000 in the web app.**

Add [PostHog AI](/ai) on top and more than half of every insight made last month came from an AI of some kind.

It's the same story for dashboards, actions, and experiments: the MCP is the single biggest creation surface for all of them. 

[Feature flags](/feature-flags) are the last product where humans still lead, and only by a few points.

## Codex makes the fewest mistakes

Before anyone fights me: this measures how carefully each client forms its requests to our MCP, not how smart the agent is. A chattier, more exploratory agent will "error" more simply because it pokes at more things. 

That said, **Codex is the standout** : among third-party callers it errors on just **2%** of calls. **Cursor** sits at **3.5%** , **Cowork** at **5.3%** , and **Claude Code** at **5.7%**. Grouped by vendor, the gap holds: OpenAI clients error about **2%** of the time, Anthropic clients about **5.5%**.

The one thing we can't tell you yet is which _model_ is most reliable. Agents can self-report their model to our MCP, but nothing verifies it, so we're not charting it until something does.

Here's a bit that made us sit up, though. Our own agents also run on Codex, against the same server, and they error just **1%** of the time – half the rate of everyone else on the same model. The likeliest explanation is boring and useful: our prompts and tool descriptions were tuned against this exact MCP.

The more interesting question, though, isn't who errors, but what they get wrong. 

Agents almost never fail at finding data: reading the schema errors just **1.5%** of the time, about 1 in 66. It's the querying that trips them up. The actual SQL call fails **4.4%** of the time, nearly three times as often.

That said, agents don't panic: when one hits an error and the session keeps going, **39%** of the time its very next move is to call the exact same tool again, and **75%** of those retries work.

## 0.5% of calls cost 18% of the tokens

In the last 30 days our MCP handed agents **84 billion tokens** , roughly thirty out for every one in.

A typical call is cheap: the median response is **440 tokens**. But the tail is long; 5% of calls return more than 7,800 tokens, and 1% return more than 16,000.

And the tail isn't where you'd expect it. `execute-sql` is 23% of calls and 19% of tokens, which seems fair. But three dashboard tools (get, update, and reorder tiles) are **0.5% of calls and 18% of all tokens returned**. 

A single `dashboard-reorder-tiles` call returns a median of 14,600 tokens, and at p95, **144,000**. That's an entire context window just to move a tile.

## You can't improve what you're not measuring

If your newest power user is a robot, you should probably know what it's doing; you can't improve an experience you're not measuring, and agents don't fill out NPS surveys.

So we launched a new analytics tool to help monitor MCP traffic. [It was born from one of our internal hackathons](/newsletter/hackathons), and was built to answer the questions we were asking ourselves.

It's called [MCP analytics](/docs/mcp-analytics) (currently in beta!) and it shows you who's calling, what they're calling, what's erroring and what isn't, how many calls each agent is making, what did they want that you don't have, and more. 

You can also step through any agent session tool call by tool call – the agent equivalent of a session replay – if you want to watch a robot think.

Every number in this post came out of those views, pointed at our own server.

There's also no separate system to learn. Every call lands as a single `$mcp_tool_call` event on your normal events table, so the purpose-built views are there if you want them – and if you'd rather write SQL, build a dashboard, or point product analytics at it like any other event, that works too.

And it doesn't just watch. Your tool calls can serve as a signal source for [Self-driving](/self-driving). A scout watches `$mcp_tool_call` telemetry for tools that need attention – high failure rates, agents retrying the same call, slow or bloated responses – weighs them by volume and reach, and files a report. If it's a server you own, that report can hand off to a coding agent that opens a pull request. 

Instrument MCP Analytics with one command

The wizard sets up the SDK and starts capturing tool calls.

`npx @posthog/wizard mcp-analytics`

[Learn more](/docs/mcp-analytics/installation)

* * *

* * *

  1. All figures are from PostHog's own MCP server (the `$mcp_tool_call` event), so read them as "what we see on one busy server," not a census of all MCP everywhere. Headline counts cover the 90 days to September 16, 2026, and include our own traffic: PostHog Desktop, CLI, Slack app, and Signals scouts account for about 45% of every call. The other 55% comes from roughly 126,000 people using their own agents. Per-tool error rates and retry behavior use the last 30 days. We deliberately used only tool names, categories, client names, and counts, not the free-text "intent" agents send, so nothing here contains user data.↩
  2. Client breakdowns and per-client error rates use the last 14 days, exclude calls where PostHog's own surfaces identify themselves as the consumer, and use PostHog's resolved harness label rather than the raw client name the SDK reports – that raw property only rides the session's `initialize` handshake, so grouping on it directly buckets most calls as unknown. Reliable client identification only landed in August 2026, which is why the client window is shorter than the headline window. Error rate reflects how a client forms requests, not the agent's underlying quality.↩

> PostHog is your product's context layer. With a full suite of developer tools – [AI observability](/ai-observability), [product analytics](/product-analytics), [session replay](/session-replay), [feature flags](/feature-flags), [experiments](/experiments), [error tracking](/error-tracking), [logs](/logs), and more – PostHog ingests and stores all the data agents need to diagnose problems, uncover opportunities, and ship fixes. A [data warehouse](/context-warehouse) and [CDP](/cdp) tie it all together, unifying that context into one source agents can read across. You can steer it all from [Slack](/slack), [the web app](/ai), the desktop ([PostHog Desktop](/desktop)), or your own editor via [the MCP](/mcp).

### Community questions

Ask a question