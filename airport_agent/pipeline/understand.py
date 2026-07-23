"""Edge 1 (LLM): natural-language question -> a structured Query.

The LLM extracts the intent, the airports mentioned *by natural name*, an optional
region, and an optional metric. It never resolves codes and never computes -- that
is the deterministic core's job (resolve/route/compute). Without an API key, a
keyword parser produces the same Query shape, so the whole pipeline still runs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .. import config, reference

INTENTS = ("metric", "compare", "rank", "explain", "meta")
METRICS = ("congestion", "growth", "volume", "long_haul")


@dataclass
class Query:
    intent: str                      # one of INTENTS
    airports: list[str] = field(default_factory=list)  # natural names OR codes
    region: str | None = None
    metric: str | None = None        # one of METRICS, or None
    raw: str = ""
    source: str = "fallback"         # "llm" or "fallback" -- for transparency


_SYSTEM = (
    "You extract structured parameters from an analyst's question about investing in "
    "US airport modernization. Return intent, airports, region, metric.\n"
    "- intent: 'metric' (a specific figure for an airport), 'compare' (two or more "
    "airports set side by side), 'rank' (which airports in a region/group are the best "
    "candidates), 'explain' (why something is the case), or 'meta' (see below).\n"
    "- 'meta' is for a message ABOUT THE CONVERSATION ITSELF rather than a request for new "
    "data: 'summarize the previous answers', 'recap what you told me', 'what did you just "
    "say?', 'repeat that in Hebrew', 'which of those did you prefer?'. These are answered "
    "from the conversation, not by computing anything, so for 'meta' leave airports, region "
    "and metric EMPTY even if the message names one. A message that asks for a NEW figure, "
    "ranking or comparison is never 'meta', even when it refers back ('and what about its "
    "growth?' is 'metric', not 'meta').\n"
    "- This is a multi-turn chat: a follow-up often leaves its subject implicit. Extract "
    "only what THIS message names -- the caller carries the previous turn's subject "
    "forward -- and never invent an airport to fill the gap.\n"
    "- airports: the airports the question is about. Use the natural wording when an "
    "airport is named (e.g. 'Santa Ana', 'the Anchorage airport'). If an airport is "
    "identified only by DESCRIPTION -- a city/metro/landmark it serves or a nickname -- "
    "extract the specific CITY that description actually denotes (e.g. 'the airport "
    "serving Silicon Valley' -> 'San Jose'; 'the airport near Disney World' -> 'Orlando'). "
    "Resolve the description to the CORRECT city; do NOT default to a region's most "
    "prominent airport (e.g. 'the capital of Alaska' is Juneau, NOT Anchorage). If you are "
    "not confident which specific city the description denotes, leave 'airports' empty "
    "rather than guess -- a wrong-but-confident airport is worse than none. This is for a "
    "SINGLE airport picked out by location; for a broad multi-state area to rank across, "
    "use 'region' instead. Empty list if no airport is referenced.\n"
    "- region: a US region if the question scopes to one (e.g. 'New England'), else null.\n"
    "- metric: the measure asked about if any -- 'congestion', 'growth', 'volume', or "
    "'long_haul' -- else null.\n"
    "Never output airport codes and never compute anything."
)


def understand(question: str) -> Query:
    """Parse a question into a Query, via Claude if available, else keywords."""
    if config.llm_available():
        try:
            return _llm_understand(question)
        except Exception:
            pass  # any SDK/parse failure degrades gracefully to the keyword parser
    return _fallback_understand(question)


def _llm_understand(question: str) -> Query:
    from pydantic import BaseModel  # lazy: only needed on the LLM path

    from .. import llm

    class _Extraction(BaseModel):
        intent: str
        airports: list[str]
        region: str | None = None
        metric: str | None = None

    resp = llm.get_client().messages.parse(
        model=llm.MODEL,
        max_tokens=400,
        system=_SYSTEM,
        messages=[{"role": "user", "content": question}],
        output_format=_Extraction,
    )
    e = resp.parsed_output
    intent = e.intent if e.intent in INTENTS else "metric"
    metric = e.metric if e.metric in METRICS else None
    if intent == "meta":  # answered from the conversation; a subject would only mislead
        return Query(intent, [], None, None, question, source="llm")
    return Query(intent, list(e.airports), e.region, metric, question, source="llm")


# --- deterministic fallback ---------------------------------------------------

# Phrases that point back at the conversation rather than at the data. Only treated
# as 'meta' when the message names no airport and no region of its own -- "summarize
# the congestion at SFO" is a data question that happens to use the word "summarize".
_META_PHRASES = (
    "summar", "recap", "sum up", "in short", "tl;dr", "so far",
    "previous answer", "previous answers", "previous response", "last answer",
    "earlier answer", "you just said", "you said", "you told me", "just told me",
    "what did you say", "say that again", "repeat that", "everything above",
)


def _fallback_understand(question: str) -> Query:
    low = question.lower()
    airports = _match_airports(low)
    region = _match_region(low)
    metric = _match_metric(low)

    if not airports and not region and any(p in low for p in _META_PHRASES):
        return Query("meta", [], None, None, question, source="fallback")

    if any(w in low for w in ("compare", " vs ", " vs.", "versus")) or (
        " or " in low and len(airports) >= 2
    ):
        intent = "compare"
    elif any(w in low for w in ("why", "unmet", "explain", "reason")):
        intent = "explain"
    elif region or any(
        w in low for w in ("which", "rank", "top ", "best", "candidate", "candidates")
    ):
        intent = "rank"
    else:
        intent = "metric"
    return Query(intent, airports, region, metric, question, source="fallback")


def _match_airports(low: str) -> list[str]:
    """Find airport mentions by scanning the alias map; dedupe by resolved IATA."""
    alias_map = reference.build_alias_map()
    found: dict[str, str] = {}  # iata -> the surface form that matched
    for key, iata in alias_map.items():
        if re.search(rf"\b{re.escape(key)}\b", low):
            found.setdefault(iata, key)
    return list(found.values())


def _match_region(low: str) -> str | None:
    for region in reference.load_airports()["region"].unique():
        if region.lower() in low:
            return region
    return None


def _match_metric(low: str) -> str | None:
    if "long" in low and "haul" in low:
        return "long_haul"
    if "congest" in low:
        return "congestion"
    if "growth" in low or "growing" in low:
        return "growth"
    if "volume" in low or "size" in low or "biggest" in low or "largest" in low:
        return "volume"
    return None
