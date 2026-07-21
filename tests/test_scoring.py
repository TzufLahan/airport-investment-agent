"""Unit tests locking the deterministic scoring math.

These use small synthetic frames (no data files, no network) so the core is
provably reproducible in isolation from the LLM and the live data sources.
"""

import numpy as np
import pandas as pd

from airport_agent.scoring import normalize, score
from airport_agent.scoring.weights import WEIGHTS


# --- normalization -----------------------------------------------------------

def test_minmax_basic():
    assert list(normalize.minmax(pd.Series([0.0, 5.0, 10.0]))) == [0.0, 50.0, 100.0]


def test_minmax_two_points():
    assert list(normalize.minmax(pd.Series([10.0, 20.0]))) == [0.0, 100.0]


def test_minmax_all_equal_is_neutral():
    assert list(normalize.minmax(pd.Series([7.0, 7.0, 7.0]))) == [50.0, 50.0, 50.0]


def test_minmax_handles_negatives():
    # growth can be negative; the minimum must map to 0.
    out = normalize.minmax(pd.Series([-9.0, 0.0, 11.0]))
    assert out.iloc[0] == 0.0 and out.iloc[2] == 100.0


def test_minmax_preserves_nan_and_normalizes_over_present():
    out = normalize.minmax(pd.Series([1.0, np.nan, 3.0]))
    assert out.iloc[0] == 0.0 and out.iloc[2] == 100.0
    assert np.isnan(out.iloc[1])


def test_log_lifts_midrange_vs_linear():
    # The whole point of log for volume: a mid value is not crushed to ~0.
    s = pd.Series([1.0, 10.0, 1000.0])
    assert normalize.log_minmax(s).iloc[1] > normalize.minmax(s).iloc[1]


# --- scoring -----------------------------------------------------------------

def _synthetic() -> pd.DataFrame:
    # AAA/BBB are Tier-1 (have capacity); CCC is Tier-2 (none).
    return pd.DataFrame({
        "iata": ["AAA", "BBB", "CCC"],
        "tier": [1, 1, 2],
        "capacity_visual_min": [90.0, 180.0, np.nan],
        "capacity_visual_max": [110.0, 220.0, np.nan],
        "ops": [200000.0, 200000.0, 150000.0],
        "growth_cagr_pct": [2.0, 10.0, 6.0],
        "enplanements_cy24": [1_000_000.0, 50_000_000.0, 10_000_000.0],
    })


def test_congestion_raw_is_ops_over_capacity_midpoint():
    df = score.score_airports(_synthetic()).set_index("iata")
    assert df.loc["AAA", "congestion_raw"] == 200000.0 / 100.0  # 2000
    assert df.loc["BBB", "congestion_raw"] == 200000.0 / 200.0  # 1000
    assert np.isnan(df.loc["CCC", "congestion_raw"])            # Tier-2: no capacity


def test_congestion_normalized_only_over_tier1():
    df = score.score_airports(_synthetic()).set_index("iata")
    assert df.loc["AAA", "congestion_norm"] == 100.0  # busiest per slot
    assert df.loc["BBB", "congestion_norm"] == 0.0
    assert np.isnan(df.loc["CCC", "congestion_norm"])


def test_tier2_has_no_investment_score_but_has_demand():
    df = score.score_airports(_synthetic()).set_index("iata")
    assert np.isnan(df.loc["CCC", "investment_score"])
    assert not np.isnan(df.loc["CCC", "demand_score"])


def test_weighted_total_matches_manual_formula():
    row = score.score_airports(_synthetic()).set_index("iata").loc["AAA"]
    manual = (
        WEIGHTS["congestion"] * row["congestion_norm"]
        + WEIGHTS["growth"] * row["growth_norm"]
        + WEIGHTS["volume"] * row["volume_norm"]
    )
    assert abs(row["investment_score"] - manual) < 1e-9


def test_scoring_is_deterministic():
    a = score.score_airports(_synthetic())
    b = score.score_airports(_synthetic())
    pd.testing.assert_frame_equal(a, b)
