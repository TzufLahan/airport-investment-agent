# Airport Investment Intelligence Agent

Helps analysts identify **US airports where renovation/expansion would be most
profitable**, using **deterministic scoring** (never LLM-invented numbers) over
public FAA + BTS data. It ships in **two forms over the same deterministic core**:

1. **Routing workflow** — the LLM sits only at the *edges* (understand the question,
   phrase the answer); a fixed pipeline computes the score. Reproducible and simple.
2. **Autonomous tool-using agent** — the LLM runs in a *loop*, deciding which tools to
   call and chaining them to answer open-ended, multi-step questions. It reasons out
   loud and can reach the web and a persistent memory.

Both guarantee the same thing: **every number comes from deterministic code** — the
model orchestrates and phrases, it never invents a figure.

## The two approaches

| | Routing workflow | Autonomous agent |
|---|---|---|
| **Control flow** | fixed pipeline (code decides) | LLM decides which tools to call, in a loop |
| **Best for** | the four intents (metric / compare / rank / explain), reproducibly | open-ended, multi-step, compositional questions |
| **Runs without a key?** | yes (deterministic fallback) | no (the loop is LLM-driven) |
| **Entry points** | `app.py` · `airport_agent.cli` | `agent_app.py` · `airport_agent.agentic.cli` |
| **Model** | Haiku 4.5 (edges) + Sonnet 5 (NPIAS view) | Sonnet 5 (the loop) |

The workflow is the reliable answer for well-defined questions; the agent shows how
the *same* deterministic core becomes **tools** for open-ended analysis. The
workflow-vs-agent tradeoff is discussed in [DESIGN.md](DESIGN.md).

## Architecture

**Workflow** — LLM at the edges, deterministic core:
```
user question
  -> understand (LLM)    : natural language -> {intent, airports, region, metric}
  -> resolve   (code)    : natural name -> IATA code   (never LLM-guessed)
  -> route     (code)    : Tier 1 (has FAA capacity) / Tier 2
  -> compute   (code)    : congestion / growth / volume -> weighted score
  -> respond   (LLM)     : numbers -> natural language + confidence & limitations
  -> second_opinion (LLM): an independent FAA NPIAS view beside the score
```

**Conversation memory** — `ask()` returns a `context` the caller hands back next turn.
It carries the previous **subject** (so *"and its growth?"* knows what "it" is) *and* a
capped **transcript** (so *"summarize the previous answers"* has something to summarize).
A message about the conversation rather than the data is classified `meta` and skips the
compute path entirely — it restates what was already shown, and is forbidden to
recompute, relabel or re-round a figure. See [DESIGN.md](DESIGN.md) §2.1.

**Agent** — the LLM loops over tools that wrap that same core:
```
question + conversation + long-term memory
  -> LLM decides which tool(s) to call   (resolve / score / rank / compare / npias /
     set_weights / web_search / fetch_url / save_memory / search_memory)
  -> run tool (deterministic or external) -> observe -> repeat -> final answer
     (narrates its reasoning between steps; numbers only from deterministic tools)
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate            # Windows (use source venv/bin/activate on *nix)
pip install -r requirements.txt
cp .env.example .env             # add ANTHROPIC_API_KEY
```

- The **workflow** runs **with or without** an API key (no key → a deterministic
  fallback; all scoring/ranking is unchanged).
- The **agent** needs `ANTHROPIC_API_KEY` (it orchestrates tool calls — no offline loop).
- Optional: `BRAVE_API_KEY` makes the agent's `web_search` reliable; without it, it
  falls back to a keyless, best-effort search.

## Data

Committed, pre-processed snapshots for all **65 in-scope airports** (33 Tier-1 with an
FAA capacity profile + 32 Tier-2, demand-only). **No fetching is needed to run** — the
snapshots ship with the repo. Re-build them with:

```bash
python scripts/fetch_data.py    # BTS T-100 metrics (passengers, growth, ops, long-haul)
python scripts/fetch_npias.py   # FAA NPIAS second-opinion data (dev cost + capacity outlook)
```

## Run

```bash
# Routing workflow (runs with or without a key)
streamlit run app.py                    # web UI
python -m airport_agent.cli             # terminal

# Autonomous agent (needs ANTHROPIC_API_KEY)
streamlit run agent_app.py              # web UI — streams the live reasoning + tool trace
python -m airport_agent.agentic.cli     # terminal
```

## Scoring (the shared core)

A weighted blend of three deterministic sub-scores, each normalized to 0-100:

| Sub-score | Definition | Weight |
|-----------|-----------|--------|
| **Congestion** | annual ops ÷ declared hourly runway capacity (Tier 1 only) | 0.40 |
| **Growth** | passenger CAGR 2022 → 2024 | 0.40 |
| **Volume** | annual enplanements (log-scaled) | 0.20 |

Tier 1 gets the full `investment_score`; Tier 2 (no FAA capacity profile) gets a
`demand_score` (growth + volume, re-normalized), always ranked **separately** — never
compared as if equal. Weights are tunable at the top of
`airport_agent/scoring/weights.py`.

## FAA NPIAS second opinion

Beside every score, an independent read from the FAA's *National Plan of Integrated
Airport Systems* (NPIAS 2025-2029): a per-airport **5-year development cost** and the
FAA's **2028/2033 runway-capacity outlook**. It *corroborates*, *diverges from*, or
*fills a gap* the score could not measure — and never changes a number.

## The autonomous agent (`airport_agent/agentic/`)

A tool-using loop over the same deterministic core:

- **11 tools** — deterministic (`resolve_airport`, `get_airport_score`, `rank_airports`,
  `compare_airports`, `get_npias`, `list_scope`, `set_weights`), external
  (`web_search`, `fetch_url`), and memory (`save_memory`, `search_memory`).
- **Memory** — short-term is the conversation itself (follow-ups just work); long-term
  is a persistent store that survives across sessions.
- **Reasoning** — the agent narrates what it understands before each round of tool
  calls (streamed live in the Streamlit UI and the CLI).
- **Guardrails** — numbers only from deterministic tools; external/web results are shown
  as context *beside* the score, never inside it; a step cap; per-tool error capture.

Validated by `scripts/validate_agent.py` (10/10 automated checks: grounding against the
deterministic ground truth, tool selection, out-of-scope handling, and 3× consistency)
→ [agent_validation.md](agent_validation.md).

## Tests

```bash
python -m pytest                  # 31 tests (scoring core + NPIAS overlay + conversation memory)
python scripts/validate_agent.py  # agent battery (needs a key; makes real LLM + tool calls)
```

## Design

See [DESIGN.md](DESIGN.md) for the scoring methodology, key tradeoffs, the FAA-NPIAS
second opinion, the workflow-vs-agent decision, data limitations, and exactly
where/how AI is used.
