"""The autonomous tool-use loop.

Claude is given the tool schemas and DECIDES which to call; we execute them and
feed results back until it produces a final answer. Short-term memory is the
running `messages` list (so follow-ups just work); long-term memory is reached
through the save_memory/search_memory tools. Guardrails: a step cap, per-tool
error capture, and a system prompt that forbids inventing numbers -- every figure
must come from a deterministic tool.
"""

from __future__ import annotations

import json

from .. import config
from . import external, memory, tools

ALL_SCHEMAS = tools.SCHEMAS + external.SCHEMAS + memory.SCHEMAS
DISPATCH = {**tools.DISPATCH, **external.DISPATCH, **memory.DISPATCH}

_SYSTEM = (
    "You are an autonomous analyst agent for a firm investing in US airport "
    "modernization and expansion. Answer the analyst's question by CALLING TOOLS, then "
    "reasoning over the results.\n"
    "RULES:\n"
    "- Every number, score, ranking, or comparison MUST come from a deterministic tool "
    "(get_airport_score, rank_airports, compare_airports, get_npias, set_weights). Never "
    "invent or estimate a figure yourself.\n"
    "- Names to codes: call resolve_airport for any airport named in words or by "
    "description; never guess an IATA code.\n"
    "- Multi-step questions: break them down and CHAIN tools (e.g. rank_airports, then "
    "get_npias on the candidates, then filter). Take as many tool steps as you need.\n"
    "- Two separate data worlds: deterministic tools give the SCORE; web_search and "
    "fetch_url give QUALITATIVE external context (recent news, an FAA page). Present "
    "external findings BESIDE the score with their source; never let them change a number.\n"
    "- Tiers: Tier 1 has an FAA capacity profile (full investment_score incl. congestion); "
    "Tier 2 has demand_score only (congestion not measured). Never treat a Tier-2 "
    "demand_score as equal to a Tier-1 investment_score; state the distinction.\n"
    "- Memory: consider search_memory for the analyst's saved preferences/conclusions; use "
    "save_memory when they state a durable preference or you reach a notable conclusion.\n"
    "- Honesty: if resolve_airport returns null, say the airport is out of scope. State "
    "assumptions and limitations. A confident wrong answer is the worst outcome.\n"
    "- Be concise and concrete, and show the key numbers you used."
)


def _preview(out: dict, n: int = 160) -> str:
    s = json.dumps(out, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + " ..."


class AgenticAgent:
    """A multi-turn tool-using agent. `messages` is its short-term memory."""

    def __init__(self) -> None:
        if not config.llm_available():
            raise RuntimeError(
                "The autonomous agent needs ANTHROPIC_API_KEY -- it orchestrates tool "
                "calls, so there is no offline loop (unlike the workflow's fallback).")
        from .. import llm
        self._client = llm.get_client()
        self.messages: list[dict] = []  # short-term conversation memory

    def ask(self, question: str, verbose: bool = False, on_tool=None) -> dict:
        """Run the tool-use loop for one question. Returns {answer, trace, steps}.

        on_tool(name, input, output) is called after each tool runs -- used by the
        Streamlit UI to stream the agent's 'thinking' (its tool calls) live.
        """
        self.messages.append({"role": "user", "content": question})
        trace: list[dict] = []

        for step in range(config.AGENT_MAX_STEPS):
            resp = self._client.messages.create(
                model=config.AGENT_MODEL, max_tokens=2000,
                system=_SYSTEM, tools=ALL_SCHEMAS, messages=self.messages,
            )
            self.messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                answer = "".join(b.text for b in resp.content if b.type == "text").strip()
                return {"answer": answer, "trace": trace, "steps": step + 1}

            tool_results = []
            for block in resp.content:
                if block.type != "tool_use":
                    continue
                out = self._run_tool(block.name, dict(block.input))
                trace.append({"step": step + 1, "tool": block.name,
                              "input": dict(block.input), "output": _preview(out)})
                if verbose:
                    print(f"  [{step + 1}] {block.name}({json.dumps(block.input, ensure_ascii=False)})"
                          f" -> {_preview(out)}")
                if on_tool is not None:
                    try:
                        on_tool(block.name, dict(block.input), out)
                    except Exception:
                        pass  # a UI callback must never break the loop
                tool_results.append({"type": "tool_result", "tool_use_id": block.id,
                                     "content": json.dumps(out, ensure_ascii=False)})
            self.messages.append({"role": "user", "content": tool_results})

        return {"answer": "[stopped: reached the tool-step limit]",
                "trace": trace, "steps": config.AGENT_MAX_STEPS}

    def _run_tool(self, name: str, args: dict) -> dict:
        fn = DISPATCH.get(name)
        if fn is None:
            return {"error": f"unknown tool: {name}"}
        try:
            return fn(**args)
        except Exception as exc:  # hand the error back so the model can recover
            return {"error": f"{type(exc).__name__}: {exc}"}


def run_once(question: str, verbose: bool = False) -> dict:
    """Convenience: answer a single question with a fresh agent."""
    return AgenticAgent().ask(question, verbose=verbose)
