"""Deterministic tests for the NPIAS second-opinion layer (no LLM required)."""

from airport_agent import config, reference
from airport_agent.pipeline import second_opinion as so
from airport_agent.pipeline.compute import Result


def test_npias_covers_every_in_scope_airport():
    df = reference.load_npias()
    assert set(df["iata"]) == set(reference.in_scope_iatas())
    # A development cost must be parsed for every airport; a hole would leave a
    # blank overlay for a real question.
    assert df["dev_cost_2025_2029"].notna().all()


def test_capacity_outlook_matches_faa_published_counts():
    """The manual Figure-1 transcription must reproduce the FAA's stated totals."""
    df = reference.load_npias()
    constrained_2028 = int((df["capacity_2028"] >= 2).sum())
    constrained_2033 = int((df["capacity_2033"] >= 2).sum())
    at_risk = int((df[["capacity_2028", "capacity_2033"]].max(axis=1) == 1).sum())
    assert (constrained_2028, constrained_2033, at_risk) == (11, 14, 13)


def test_relationship_classification():
    assert so._relationship(1, 80, 2) == "corroborate"          # FAA + we both hot
    assert so._relationship(1, 20, 3) == "faa_more_concerned"    # FAA hotter
    assert so._relationship(1, 80, 1) == "we_more_concerned"     # we hotter, FAA only congested
    assert so._relationship(1, 20, 1) == "faa_notes_congestion"  # FAA congested, we cool
    assert so._relationship(1, 20, 0) == "both_quiet"            # FAA not flagged at all
    assert so._relationship(2, None, 1) == "fills_gap"           # Tier 2, FAA flags
    assert so._relationship(2, None, 0) == "both_quiet_t2"       # Tier 2, both quiet


def test_dev_cost_percentile_is_monotonic():
    df = reference.load_npias()
    costs = sorted(int(x) for x in df["dev_cost_2025_2029"])
    lo, hi = df.loc[df["dev_cost_2025_2029"].idxmin()], df.loc[df["dev_cost_2025_2029"].idxmax()]
    subj = {"tier": 1, "our_score": 50, "congestion_norm": 50}
    f_lo = so._facts_for({**subj, "iata": lo["iata"], "name": lo["iata"]}, lo, costs)
    f_hi = so._facts_for({**subj, "iata": hi["iata"], "name": hi["iata"]}, hi, costs)
    assert f_lo["faa_dev_cost_percentile"] < f_hi["faa_dev_cost_percentile"]
    assert f_hi["faa_dev_cost_percentile"] == 100


def test_second_opinion_fills_gap_for_tier2(monkeypatch):
    """A Tier-2 airport the FAA flags should surface the gap-fill note (template path)."""
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", None)  # force deterministic template
    result = Result(intent="metric", question="q",
                    airports=[{"iata": "SJC", "name": "Mineta San Jose",
                               "tier": 2, "demand_score": 40.0}])
    block = so.second_opinion(result)
    assert block is not None
    assert "FAA NPIAS" in block and "SJC" in block
    # SJC is a Tier-2 airport the FAA flags -> the gap-fill note must appear.
    assert "no congestion number" in block


def test_second_opinion_none_when_no_airports():
    assert so.second_opinion(Result(intent="rank", question="q")) is None
