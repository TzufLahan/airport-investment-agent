"""Compute sub-scores, the weighted investment score, and tier-aware rankings.

Two scores, by design (see design doc 3.3 and the Tier-2 handling decision):
  * investment_score -- Tier-1 only: the full 0.4/0.4/0.2 blend of congestion,
    growth and volume. High confidence: congestion is a real measurement.
  * demand_score     -- all airports: growth + volume re-normalized to sum to 1.
    It is the ranking metric for Tier-2 (which has no congestion) and is shown
    with an explicit "congestion not measured" caveat, never mixed with Tier-1.
"""

import numpy as np
import pandas as pd

from .. import loader
from . import normalize
from .weights import WEIGHTS


def score_airports(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return the dataset with sub-scores and the two composite scores added."""
    df = (loader.load_dataset() if df is None else df).copy()

    # Congestion = actual operations vs declared hourly capacity (midpoint of the
    # FAA Visual range). Tier-2 airports have no capacity -> NaN, and min-max then
    # normalizes congestion over exactly the Tier-1 airports.
    df["declared_capacity"] = (df["capacity_visual_min"] + df["capacity_visual_max"]) / 2
    df["congestion_raw"] = df["ops"] / df["declared_capacity"]

    df["congestion_norm"] = normalize.minmax(df["congestion_raw"])
    df["growth_norm"] = normalize.minmax(df["growth_cagr_pct"])
    df["volume_norm"] = normalize.log_minmax(df["enplanements_cy24"])

    # Full investment score -- Tier-1 only.
    df["investment_score"] = (
        WEIGHTS["congestion"] * df["congestion_norm"]
        + WEIGHTS["growth"] * df["growth_norm"]
        + WEIGHTS["volume"] * df["volume_norm"]
    )
    df.loc[df["tier"] != 1, "investment_score"] = np.nan

    # Demand score -- growth + volume, re-normalized to sum to 1 (the Tier-2 metric).
    demand_weight = WEIGHTS["growth"] + WEIGHTS["volume"]
    df["demand_score"] = (
        WEIGHTS["growth"] * df["growth_norm"] + WEIGHTS["volume"] * df["volume_norm"]
    ) / demand_weight

    return df


def ranked(region: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(tier1, tier2) frames, each sorted by its own score. Optionally filter by
    region. Respects Option A: the two tiers are ranked and returned separately."""
    df = score_airports()
    if region is not None:
        df = df[df["region"] == region]
    tier1 = df[df["tier"] == 1].sort_values("investment_score", ascending=False)
    tier2 = df[df["tier"] == 2].sort_values("demand_score", ascending=False)
    return tier1, tier2
