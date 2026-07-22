"""Loads and validates the reference tables (the source of truth).

Two CSVs, joined on IATA:
  - reference/airports.csv      : one row per in-scope airport (Tier 1 and Tier 2)
  - reference/faa_capacity.csv  : one row per Tier-1 airport (has an FAA profile)

Tier is a property of the airport, defined by the data: an airport is Tier 1 iff
it has an FAA capacity profile (a row in faa_capacity.csv). We store `tier`
explicitly for readability but VALIDATE it against capacity presence, so a silent
inconsistency -- the worst outcome for a join-based tool -- fails loudly instead
of producing a quietly wrong answer.

All identifiers are normalized to upper-case IATA on load (design doc 3.7), which
is the single key every downstream join uses.
"""

from functools import lru_cache

import pandas as pd

from . import config


@lru_cache(maxsize=1)
def load_airports() -> pd.DataFrame:
    """Return the airports reference table, indexed for lookup by IATA."""
    df = pd.read_csv(config.AIRPORTS_CSV, dtype=str)
    df["iata"] = df["iata"].str.strip().str.upper()
    df["tier"] = df["tier"].astype(int)
    df["staleness_flag"] = df["staleness_flag"].astype(int)
    df["enplanements_cy24"] = df["enplanements_cy24"].astype(int)
    df["notes"] = df["notes"].fillna("")
    _validate(df, load_capacity())
    return df


@lru_cache(maxsize=1)
def load_capacity() -> pd.DataFrame:
    """Return the FAA declared-capacity table (Tier-1 airports only)."""
    df = pd.read_csv(config.FAA_CAPACITY_CSV, dtype={"iata": str})
    df["iata"] = df["iata"].str.strip().str.upper()
    return df


def _validate(airports: pd.DataFrame, capacity: pd.DataFrame) -> None:
    """Fail loudly if tier and capacity-presence disagree (silent join guard)."""
    all_iatas = set(airports["iata"])
    tier1 = set(airports.loc[airports["tier"] == 1, "iata"])
    tier2 = set(airports.loc[airports["tier"] == 2, "iata"])
    with_capacity = set(capacity["iata"])

    problems = []
    if dupes := airports["iata"][airports["iata"].duplicated()].tolist():
        problems.append(f"Duplicate IATA codes in airports.csv: {sorted(set(dupes))}")
    if missing := tier1 - with_capacity:
        problems.append(f"Tier-1 airports missing a capacity row: {sorted(missing)}")
    if orphan := with_capacity - all_iatas:
        problems.append(f"Capacity rows with no airport entry: {sorted(orphan)}")
    if leaked := tier2 & with_capacity:
        problems.append(f"Tier-2 airports that carry capacity data: {sorted(leaked)}")
    if problems:
        raise ValueError(
            "Reference data inconsistency (silent-join risk):\n  " + "\n  ".join(problems)
        )


@lru_cache(maxsize=1)
def build_alias_map() -> dict[str, str]:
    """Map every natural name/alias/code -> IATA (lower-cased keys).

    This is the deterministic backbone of name resolution (design doc step 3):
    the LLM extracts a natural name, and this map -- never the LLM -- decides the
    code. Includes the IATA code itself, the airport name, the city, and each
    pipe-separated alias.

    Collisions (a name several airports share, like a multi-airport metro) resolve
    deterministically to the larger hub; the airport's own IATA code always wins.
    """
    airports = load_airports()
    alias_map: dict[str, str] = {}
    rank_of: dict[str, int] = {}

    def add(key: str, iata: str, rank: int) -> None:
        key = key.strip().lower()
        if not key:
            return
        if key not in alias_map or rank > rank_of[key]:
            alias_map[key] = iata
            rank_of[key] = rank

    for row in airports.itertuples(index=False):
        # Rank by actual passenger volume so an ambiguous metro name resolves to
        # the primary airport (e.g. "Chicago" -> ORD 38.6M over MDW 10.4M).
        rank = int(row.enplanements_cy24)
        add(row.iata, row.iata, 10**15)  # the code itself always resolves to itself
        add(row.name, row.iata, rank)
        add(row.city, row.iata, rank)
        for alias in str(row.aliases).split("|"):
            add(alias, row.iata, rank)
    return alias_map


def get_airport(iata: str) -> pd.Series | None:
    """Return the airport row for an IATA code, or None if out of scope."""
    airports = load_airports()
    hit = airports.loc[airports["iata"] == iata.strip().upper()]
    return hit.iloc[0] if len(hit) else None


def get_capacity(iata: str) -> pd.Series | None:
    """Return the capacity row for a Tier-1 IATA code, or None (Tier 2)."""
    capacity = load_capacity()
    hit = capacity.loc[capacity["iata"] == iata.strip().upper()]
    return hit.iloc[0] if len(hit) else None


@lru_cache(maxsize=1)
def load_npias() -> pd.DataFrame:
    """FAA NPIAS 'second opinion' table (5-year dev cost + capacity outlook), one
    row per in-scope airport. Read only by the second-opinion layer -- never by the
    deterministic score. Built by scripts/fetch_npias.py."""
    df = pd.read_csv(config.NPIAS_CSV)
    df["iata"] = df["iata"].str.strip().str.upper()
    df["dev_cost_2025_2029"] = df["dev_cost_2025_2029"].astype("Int64")
    for col in ("capacity_2028", "capacity_2033"):
        df[col] = df[col].astype(int)
    return df


def get_npias(iata: str) -> pd.Series | None:
    """Return the NPIAS row for an IATA code, or None if absent."""
    df = load_npias()
    hit = df.loc[df["iata"] == iata.strip().upper()]
    return hit.iloc[0] if len(hit) else None


def in_scope_iatas() -> list[str]:
    """All in-scope IATA codes (both tiers)."""
    return load_airports()["iata"].tolist()
