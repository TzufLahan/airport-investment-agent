"""Comprehensive validation harness for the autonomous agent.

Run:  python scripts/validate_agent.py         (needs ANTHROPIC_API_KEY; it makes
real LLM + tool calls, so it costs money -- roughly $1.5-2.5 for the full battery).

Because the agent is stochastic (the model chooses tool calls), we do not check
"same input -> same output". Instead each case runs automated checks:

  * no_crash    -- the loop finished without an error and below the step cap.
  * tools_ok    -- an expected tool actually appears in the tool trace.
  * substr_ok   -- an expected phrase appears (e.g. "out of scope").
  * grounding   -- deterministic values computed here from score_airports()/NPIAS
                   appear in the answer (proof the agent used real numbers, not
                   invented ones). Shown for review; prose formatting can vary.

Plus a CONSISTENCY check: one question is run 3x and the key numbers must match
every time (they must -- they come from deterministic tools). Results, traces and
answers are written to agent_validation.md.
"""

import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from airport_agent import config  # noqa: E402

# Isolate the agent's long-term memory to a throwaway file for the run.
config.AGENT_MEMORY_FILE = pathlib.Path(tempfile.gettempdir()) / "agent_validation_memory.json"
if config.AGENT_MEMORY_FILE.exists():
    config.AGENT_MEMORY_FILE.unlink()

from airport_agent.agentic import tools  # noqa: E402
from airport_agent.agentic.agent import AgenticAgent  # noqa: E402
from airport_agent.pipeline.compute import _num  # noqa: E402
from airport_agent.scoring import score  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "agent_validation.md"


def gt_reps(iata: str, field: str) -> list[str]:
    """String representations of the deterministic ground-truth value for (iata, field)."""
    if field == "dev_cost_percentile":
        return [str(tools.get_npias(iata)["dev_cost_percentile"])]
    df = score.score_airports()
    row = df[df["iata"] == iata].iloc[0]
    value = _num(row[field], 2 if field == "growth_cagr_pct" else 1)
    reps = {str(value)}
    if isinstance(value, float):
        if value == int(value):
            reps.add(str(int(value)))       # 100.0 -> also "100"
        reps.add(str(round(value, 1)))       # growth 3.59 -> also "3.6"
    return list(reps)


# --- battery ------------------------------------------------------------------
# Each case: id, question, tools we expect to see, values to look for, phrases.
CASES = [
    {"id": "compare-tier1", "q": "Compare LA and Santa Ana on our investment score.",
     "tools": ["compare_airports", "get_airport_score"],
     "values": [("LAX", "investment_score"), ("SNA", "investment_score")]},
    {"id": "metric-congestion", "q": "How congested is JFK?",
     "tools": ["get_airport_score"], "values": [("JFK", "congestion_norm")]},
    {"id": "rank-region", "q": "Rank the New England airports as expansion candidates.",
     "tools": ["rank_airports"], "values": [("BOS", "investment_score")]},
    {"id": "npias", "q": "What does the FAA NPIAS say about SFO's development cost and capacity outlook?",
     "tools": ["get_npias"], "values": [("SFO", "dev_cost_percentile")]},
    {"id": "custom-weights",
     "q": "If growth matters twice as much as congestion and volume is minor, who are the top 3 Tier-1 airports?",
     "tools": ["set_weights"], "values": []},
    {"id": "tier2-demand", "q": "What is the demand score for Nashville?",
     "tools": ["get_airport_score"], "values": [("BNA", "demand_score")]},
    {"id": "messy-typo", "q": "How congested is Chicagoo?",
     "tools": ["get_airport_score"], "values": [("ORD", "congestion_norm")]},
    {"id": "descriptive", "q": "What is the passenger growth of the main airport serving Silicon Valley?",
     "tools": ["get_airport_score"], "values": [("SJC", "growth_cagr_pct")]},
    {"id": "out-of-scope", "q": "How congested is Fresno?",
     "tools": ["resolve_airport"],
     "substr": ["out of scope", "not among", "not in scope", "isn't in", "not in our"]},
    {"id": "compositional",
     "q": "Which Tier-1 airports does the FAA flag as capacity-constrained by 2033 while our "
          "congestion score is under 65? Rank those by growth.",
     "tools": ["get_npias"], "values": []},
]


def run_case(case: dict) -> dict:
    result = AgenticAgent().ask(case["q"])
    answer, trace = result["answer"], result["trace"]
    called = {t["tool"] for t in trace}
    low = answer.lower()

    no_crash = ("hit an error" not in low and not answer.startswith("[stopped")
                and result["steps"] < config.AGENT_MAX_STEPS)
    tools_ok = (not case.get("tools")) or bool(called & set(case["tools"]))
    substr_ok = (not case.get("substr")) or any(s in low for s in case["substr"])

    grounded = []
    for iata, field in case.get("values", []):
        reps = gt_reps(iata, field)
        grounded.append({"target": f"{iata}.{field}", "expected_any": reps,
                         "found": any(r in answer for r in reps)})

    hard_pass = no_crash and tools_ok and substr_ok
    return {"answer": answer, "trace": trace, "steps": result["steps"], "called": sorted(called),
            "no_crash": no_crash, "tools_ok": tools_ok, "substr_ok": substr_ok,
            "grounded": grounded, "pass": hard_pass}


def consistency_check(question: str, targets: list[tuple[str, str]], runs: int = 3) -> dict:
    """Run one question `runs` times; the deterministic values must appear every time."""
    per_run = []
    for _ in range(runs):
        ans = AgenticAgent().ask(question)["answer"]
        hits = {f"{i}.{f}": any(r in ans for r in gt_reps(i, f)) for i, f in targets}
        per_run.append(hits)
    stable = all(all(run.values()) for run in per_run)
    return {"question": question, "runs": runs, "per_run": per_run, "stable": stable}


def main() -> None:
    if not config.llm_available():
        print("Needs ANTHROPIC_API_KEY in .env -- the agent makes real LLM calls.")
        return

    lines = ["# Autonomous agent -- validation report\n",
             f"Model: **{config.AGENT_MODEL}**  ·  {len(CASES)} cases + a consistency check.\n"]
    passed = 0
    for case in CASES:
        print(f"  running: {case['id']} ...")
        r = run_case(case)
        passed += int(r["pass"])
        flag = "PASS" if r["pass"] else "FAIL"
        lines.append(f"\n## [{flag}] {case['id']}\n")
        lines.append(f"**Q:** {case['q']}\n")
        lines.append(f"- no_crash: {r['no_crash']} · tools_ok: {r['tools_ok']} "
                     f"(saw {r['called']}) · substr_ok: {r['substr_ok']} · steps: {r['steps']}")
        for g in r["grounded"]:
            mark = "OK" if g["found"] else "REVIEW"
            lines.append(f"- grounding {g['target']}: [{mark}] expected one of {g['expected_any']}")
        lines.append(f"\n**Answer:**\n\n{r['answer']}\n")
        lines.append("**Tool trace:** " + " -> ".join(t["tool"] for t in r["trace"]) + "\n")

    print("  running: consistency (3x) ...")
    con = consistency_check("Compare LA and Santa Ana on our investment score.",
                            [("LAX", "investment_score"), ("SNA", "investment_score")])
    lines.insert(2, f"\n**Consistency (3x, LAX/SNA scores identical every run): "
                    f"{'STABLE' if con['stable'] else 'UNSTABLE'}**  ·  {con['per_run']}\n")

    summary = f"\n**Hard-check pass rate: {passed}/{len(CASES)}  ·  consistency: " \
              f"{'STABLE' if con['stable'] else 'UNSTABLE'}**\n"
    lines.insert(2, summary)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{summary}Wrote {OUT.name}")


if __name__ == "__main__":
    main()
