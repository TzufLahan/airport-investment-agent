"""Long-term (persistent) memory for the agent, as save/search tools.

Short-term memory is the conversation itself (the running `messages` list in the
loop), which is why follow-ups just work. This module is the LONG-term store that
survives across sessions: user preferences, prior conclusions, cached findings.
It is a simple JSON file with keyword search -- deliberately minimal; a vector
store with embeddings is the natural upgrade for semantic recall.
"""

from __future__ import annotations

import json
import time

from .. import config

_STORE: list[dict] | None = None


def _load() -> list[dict]:
    global _STORE
    if _STORE is None:
        try:
            _STORE = json.loads(config.AGENT_MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            _STORE = []
    return _STORE


def _persist() -> None:
    config.AGENT_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    config.AGENT_MEMORY_FILE.write_text(
        json.dumps(_load(), ensure_ascii=False, indent=2), encoding="utf-8")


def save_memory(fact: str, tags: list[str] | None = None) -> dict:
    """Persist a durable fact (a preference, a conclusion) for future sessions."""
    store = _load()
    entry = {"fact": fact, "tags": tags or [], "ts": time.strftime("%Y-%m-%d %H:%M")}
    store.append(entry)
    _persist()
    return {"saved": entry, "total_memories": len(store)}


def search_memory(query: str, top: int = 5) -> dict:
    """Recall durable facts relevant to a query (keyword overlap)."""
    store = _load()
    words = [w for w in query.lower().split() if len(w) > 2]
    scored = []
    for e in store:
        hay = (e["fact"] + " " + " ".join(e.get("tags", []))).lower()
        overlap = sum(1 for w in words if w in hay)
        if overlap:
            scored.append((overlap, e))
    scored.sort(key=lambda x: -x[0])
    return {"query": query,
            "matches": [e for _, e in scored[:top]],
            "note": None if scored else "no matching memories"}


SCHEMAS = [
    {"name": "save_memory",
     "description": "Save a durable fact for future sessions -- an analyst preference "
                    "(e.g. 'prefers weighting growth over congestion') or a conclusion "
                    "(e.g. 'flagged SFO as the top West-coast candidate'). Not for "
                    "transient chit-chat.",
     "input_schema": {"type": "object",
                      "properties": {"fact": {"type": "string"},
                                     "tags": {"type": "array", "items": {"type": "string"}}},
                      "required": ["fact"]}},
    {"name": "search_memory",
     "description": "Recall durable facts saved in earlier sessions that are relevant "
                    "to the current question (preferences, prior conclusions).",
     "input_schema": {"type": "object",
                      "properties": {"query": {"type": "string"}},
                      "required": ["query"]}},
]

DISPATCH = {"save_memory": save_memory, "search_memory": search_memory}
