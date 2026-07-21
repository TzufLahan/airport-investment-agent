"""Conversational CLI (design doc step 5).

Run:  python -m airport_agent.cli
A simple REPL over agent.ask(), carrying light conversation memory so follow-ups
resolve against the previous turn. Works with or without an ANTHROPIC_API_KEY --
without one, the deterministic fallback answers.
"""

import sys

from . import config
from .agent import ask
from .pipeline.compute import _DEFINITIONS as METRIC_DEFINITIONS

BANNER = """\
Airport Investment Intelligence Agent
Ask about US airport expansion candidates. Examples:
  - Which airports in New England are strong candidates for terminal expansion?
  - Compare LA and Santa Ana congestion levels.
  - What is the percentage of long-haul flights out of Anchorage?
  - What is the unmet demand at SFO and why?
Type '/metrics' for metric definitions, or 'exit' to quit.
"""


def main() -> None:
    # The LLM writes rich Unicode (em dashes, minus signs, tables); force UTF-8 so
    # a legacy Windows codepage console doesn't crash printing the answer.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    mode = "Claude (LLM edges)" if config.llm_available() else "deterministic fallback (no API key)"
    print(BANNER)
    print(f"[mode: {mode}]\n")

    context: dict = {}
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
        if question.lower() in ("/metrics", "metrics"):
            for key, text in METRIC_DEFINITIONS.items():
                print(f"  {key.replace('_', ' ').title()}: {text}")
            print()
            continue
        try:
            answer, context = ask(question, context)
        except Exception as exc:  # never crash the chat loop on one bad turn
            print(f"agent> Sorry, I hit an error: {exc}\n")
            continue
        print(f"agent> {answer}\n")


if __name__ == "__main__":
    main()
