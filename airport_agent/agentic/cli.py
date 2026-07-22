"""REPL for the autonomous tool-using agent.

Run:  python -m airport_agent.agentic.cli
Shows each tool the agent chooses to call (the trace), then its final answer, so
you can watch the loop reason step by step. One conversation = one agent, so
follow-ups use the short-term memory. Needs ANTHROPIC_API_KEY.
"""

import sys

from .. import config
from .agent import AgenticAgent

BANNER = """\
Airport Investment -- Autonomous Agent (tool-using)
The model chooses which tools to call; every number comes from a deterministic tool.
Try, for example:
  - Compare Denver and Salt Lake City, and tell me what the FAA says about each.
  - Find Tier-1 airports with low congestion that the FAA still flags as constrained,
    then rank them by growth.
  - If I care about growth twice as much as congestion, who are the top 5?
  - Any recent news about SFO expansion?
Type 'exit' to quit.
"""


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if not config.llm_available():
        print("This agent needs ANTHROPIC_API_KEY in .env -- it orchestrates tool calls, "
              "so there is no offline mode. (The deterministic workflow, "
              "python -m airport_agent.cli, runs without a key.)")
        return

    print(BANNER)
    agent = AgenticAgent()
    while True:
        try:
            question = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue
        if question.lower() in ("exit", "quit", ":q"):
            break
        print("  (thinking / calling tools...)")
        result = agent.ask(question, verbose=True)
        print(f"\nagent> {result['answer']}\n[{result['steps']} step(s), "
              f"{len(result['trace'])} tool call(s)]\n")


if __name__ == "__main__":
    main()
