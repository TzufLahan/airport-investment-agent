"""Single data entry point for the scoring layer and pipeline.

Joins the committed metrics snapshot (data/processed/airport_metrics.csv) with the
reference tables into one analysis frame, keyed by IATA. Nothing downstream reads
raw sources; they all consume load_dataset(). A coverage guard fails loudly if the
join left holes -- a quietly missing value is the worst outcome for the tool.
"""

from functools import lru_cache

import pandas as pd

from . import config, reference


@lru_cache(maxsize=1)
def load_metrics() -> pd.DataFrame:
    """Per-airport BTS metrics: passengers (base/latest), growth, long-haul, ops."""
    df = pd.read_csv(config.AIRPORT_METRICS)
    df["iata"] = df["iata"].str.strip().str.upper()
    return df


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    """One row per in-scope airport: identity + classification (reference),
    declared capacity (Tier 1 only), and BTS demand metrics -- joined on IATA."""
    airports = reference.load_airports()
    metrics = load_metrics()
    capacity = reference.load_capacity()[
        ["iata", "capacity_visual_min", "capacity_visual_max"]
    ]

    df = airports.merge(metrics, on="iata", how="left", validate="one_to_one")
    df = df.merge(capacity, on="iata", how="left", validate="one_to_one")

    _check_coverage(df)
    return df


def _check_coverage(df: pd.DataFrame) -> None:
    """Fail loudly on silent join gaps that would corrupt a score downstream."""
    problems = []
    no_ops = df.loc[df["ops"].isna(), "iata"].tolist()
    no_vol = df.loc[df["pax_latest"].isna(), "iata"].tolist()
    tier1_no_cap = df.loc[(df["tier"] == 1) & df["capacity_visual_min"].isna(), "iata"].tolist()
    if no_ops:
        problems.append(f"airports missing operations data: {no_ops}")
    if no_vol:
        problems.append(f"airports missing passenger data: {no_vol}")
    if tier1_no_cap:
        problems.append(f"Tier-1 airports missing capacity after join: {tier1_no_cap}")
    if problems:
        raise ValueError("Dataset coverage gap (silent-join risk):\n  " + "\n  ".join(problems))
