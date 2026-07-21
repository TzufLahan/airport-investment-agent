"""Run a battery of sample questions and save every answer to sample_run.md.

Usage:  python scripts/run_test_battery.py
Writes clean Q&A for review, plus a deterministic ground-truth table so the
numbers in each answer can be verified against the scoring core. Console output
is kept ASCII-only; the rich answers go to the UTF-8 file (so a legacy Windows
console codepage can't crash the run).
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from airport_agent import config  # noqa: E402
from airport_agent.agent import ask  # noqa: E402
from airport_agent.scoring import score  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "sample_run.md"

# Each inner list is one conversation thread (context carried across its turns);
# single-item lists are standalone questions.
BATTERY = [
    ("A. Assignment questions", [
        ["Which airports in New England are strong candidates for terminal expansion?"],
        ["Compare LA and Santa Ana airport congestion levels."],
        ["What is the percentage of long-haul flights out of Anchorage airport?"],
        ["What is the unmet flight demand in SFO airport and why?"],
    ]),
    ("B. Single metrics", [
        ["How congested is JFK?"],
        ["What is the passenger growth at Nashville?"],
        ["How many passengers does Denver handle?"],
        ["What share of flights out of Honolulu are long-haul?"],
    ]),
    ("C. Ranking (overall and by region)", [
        ["Which airports are the best expansion candidates overall?"],
        ["Which Mountain region airports are the best candidates?"],
        ["Rank the New England airports."],
    ]),
    ("D. Comparisons (same-tier, cross-tier, multi-airport metros)", [
        ["Compare Denver and Salt Lake City."],
        ["Compare Boston and Bradley."],
        ["Compare Nashville and Austin."],
        ["Compare O'Hare and Midway."],
        ["Compare Dallas and Houston."],
    ]),
    ("E. Explanations", [
        ["Why is Charlotte a strong investment candidate?"],
        ["Why is LaGuardia congested?"],
    ]),
    ("F. Out-of-scope airports (not among the 65)", [
        ["How congested is Fresno?"],
        ["Compare Boise and Spokane."],
        ["How is Tucson doing?"],
        ["What about El Paso and Reno?"],
        ["Rank the airports in Wichita and Tulsa."],
    ]),
    ("G. Messy input (typos, descriptions, a factual trap)", [
        ["How congested is Chicagoo?"],
        ["What is the main airport serving Silicon Valley?"],
        ["What's the airport in the capital of Alaska?"],
    ]),
    ("H. Follow-ups (conversation memory in one thread)", [
        ["Compare LA and Santa Ana congestion.",
         "What about their growth?",
         "And volume?",
         "Why is LAX more congested?"],
    ]),
]


def main() -> None:
    mode = "Claude (LLM edges)" if config.llm_available() else "deterministic fallback (no API key)"
    out = [f"# Sample run - Airport Investment Intelligence Agent\n",
           f"Mode: **{mode}**\n"]

    total = errors = 0
    for category, threads in BATTERY:
        out.append(f"\n## {category}\n")
        for thread in threads:
            context: dict = {}
            for question in thread:
                total += 1
                try:
                    answer, context = ask(question, context)
                except Exception as exc:
                    answer, errors = f"[ERROR: {exc}]", errors + 1
                out.append(f"**Q:** {question}\n\n{answer}\n\n---\n")
            print(f"  ok: {thread[0][:60]}")

    # Deterministic ground truth, so every number above can be checked.
    df = score.score_airports()
    cols = ["iata", "tier", "hub", "region", "growth_cagr_pct", "longhaul_share_pct",
            "ops", "congestion_raw", "congestion_norm", "investment_score", "demand_score"]
    gt = df[cols].round(1)
    out.append("\n## Deterministic ground truth (verify the numbers above)\n\n```\n"
               + gt.to_string(index=False) + "\n```\n")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"\nWrote {total} answers ({errors} errors) -> {OUT.name}")


if __name__ == "__main__":
    main()
