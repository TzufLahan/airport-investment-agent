# Airport Investment Intelligence Agent

An AI agent that helps analysts identify US airports where renovation/expansion
would be most profitable, using **deterministic scoring** (not LLM output) over
public aviation data, with a conversational CLI.

## Architecture at a glance

The LLM is used only at the edges — understanding the question and phrasing the
answer. Every number, ranking, and comparison is pure, reproducible Python.

```
user question
  -> understand (LLM)   : natural language -> {intent, airports}
  -> resolve   (code)   : natural name -> IATA code
  -> route     (code)   : Tier 1 (has FAA capacity profile) / Tier 2
  -> compute   (code)   : congestion / growth / volume -> weighted score
  -> respond   (LLM)    : numbers -> natural language + confidence & limitations
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

Uses a committed, pre-processed snapshot of BTS T-100 and On-Time data for the
~34 airports that have an official FAA Airport Capacity Profile. Re-fetch with:

```bash
python scripts/fetch_data.py
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

See [DESIGN.md](DESIGN.md) for the scoring methodology, key tradeoffs, data
limitations, and exactly where/how AI is used.
