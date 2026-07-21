"""Edge 3 (deterministic): tag each resolved airport with its data tier.

Tier is a property of the airport (design doc 3.3): Tier 1 has an FAA capacity
profile (full scoring, including congestion); Tier 2 does not (demand only).
Routing just reads it from the reference table so downstream code answers within
each airport's confidence level.
"""

from .. import reference


def tier_of(iata: str) -> int:
    row = reference.get_airport(iata)
    return int(row["tier"]) if row is not None else 0


def split_by_tier(iatas) -> tuple[list[str], list[str]]:
    codes = list(iatas)
    return [c for c in codes if tier_of(c) == 1], [c for c in codes if tier_of(c) == 2]
