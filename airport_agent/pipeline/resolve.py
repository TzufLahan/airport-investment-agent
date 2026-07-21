"""Edge 2 (deterministic): natural airport name -> IATA code.

The poka-yoke of the design (doc step 3): the LLM may propose a natural name, but
this map -- never the LLM -- decides the code, so a hallucinated 'SAN vs SNA' can't
slip through. The LLM often appends generic words ("SFO airport", "the Anchorage
airport"), so we retry after stripping them; a light fuzzy pass then tolerates
typos. Names we still can't map are returned as unresolved, so the caller tells
the user honestly rather than guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from difflib import get_close_matches

from .. import reference

# Generic words the LLM tends to add to an airport name but that are not part of
# any alias key. Stripped only as a fallback, after an exact match is tried.
_GENERIC = {"airport", "airfield", "international", "intl", "regional", "field",
            "the", "a", "an"}


@dataclass
class Resolution:
    resolved: dict[str, str] = field(default_factory=dict)  # surface name -> IATA
    unresolved: list[str] = field(default_factory=list)


def _strip_generic(key: str) -> str:
    tokens = [t for t in re.split(r"\s+", key.strip().lower()) if t and t not in _GENERIC]
    return " ".join(tokens)


def resolve(names: list[str]) -> Resolution:
    alias_map = reference.build_alias_map()
    keys = list(alias_map.keys())
    out = Resolution()
    for name in names:
        raw = name.strip().lower()
        stripped = _strip_generic(raw)
        iata = (
            alias_map.get(raw)                 # exact
            or alias_map.get(stripped)         # exact after dropping "airport" etc.
            or _fuzzy(alias_map, keys, raw)    # typo tolerance
            or _fuzzy(alias_map, keys, stripped)
        )
        if iata:
            out.resolved[name] = iata
        else:
            out.unresolved.append(name)
    return out


def _fuzzy(alias_map: dict[str, str], keys: list[str], key: str) -> str | None:
    if not key:
        return None
    close = get_close_matches(key, keys, n=1, cutoff=0.88)  # strict, to avoid wrong hits
    return alias_map[close[0]] if close else None
