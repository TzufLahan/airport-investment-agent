# Airport Investment Intelligence Agent

An AI agent that helps analysts identify US airports where renovation/expansion
would be most profitable, using **deterministic scoring** (not LLM output) over
public aviation data, with a conversational CLI / web UI and an independent
FAA-NPIAS second opinion.

## Architecture at a glance

The LLM is used only at the edges — understanding the question, phrasing the
answer, and adding an independent second opinion. Every number, ranking, and
comparison is pure, reproducible Python.

```
user question
  -> understand (LLM)   : natural language -> {intent, airports}
  -> resolve   (code)   : natural name -> IATA code
  -> route     (code)   : Tier 1 (has FAA capacity profile) / Tier 2
  -> compute   (code)   : congestion / growth / volume -> weighted score
  -> respond   (LLM)    : numbers -> natural language + confidence & limitations
  -> second_opinion (LLM): an independent FAA NPIAS view beside the score
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate            # Windows (use source venv/bin/activate on *nix)
pip install -r requirements.txt
cp .env.example .env             # then add your ANTHROPIC_API_KEY (optional)
```

Without an API key the agent still runs, via a deterministic fallback.

## Data

Uses committed, pre-processed snapshots for all **65 in-scope airports** (33 Tier-1
with an FAA capacity profile + 32 Tier-2, demand-only). **No fetching is needed to
run** — the snapshots ship with the repo. Re-build them with:

```bash
python scripts/fetch_data.py    # BTS T-100 metrics (passengers, growth, ops, long-haul)
python scripts/fetch_npias.py   # FAA NPIAS second-opinion data (dev cost + capacity outlook)
```

## Run

Terminal chat:

```bash
python -m airport_agent.cli
```

Or the web chat UI (browser):

```bash
streamlit run app.py
```

Both are thin views over the same `agent.ask()` pipeline and work with or without
an API key.

## Design

See [DESIGN.md](DESIGN.md) for the scoring methodology, key tradeoffs, the
independent FAA-NPIAS second opinion, data limitations, and exactly where/how AI
is used.
