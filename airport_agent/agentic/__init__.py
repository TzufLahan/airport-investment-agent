"""Autonomous tool-using agent over the deterministic core.

Where the top-level `agent.ask()` is a fixed routing workflow (understand ->
resolve -> compute -> respond), this package is the *agentic* alternative: an LLM
in a loop that decides which TOOLS to call, observes results, and iterates until
it can answer. The tools wrap the same deterministic scoring core -- so every
number stays reproducible; only the control flow moves from fixed code to the model.

  tools.py    -- deterministic tools (wrap scoring/reference) + JSON schemas
  external.py -- world-facing tools (web search, url fetch)
  memory.py   -- short-term (conversation) + long-term (persistent) memory
  agent.py    -- the tool-use loop
  cli.py      -- REPL entry point:  python -m airport_agent.agentic.cli
"""
