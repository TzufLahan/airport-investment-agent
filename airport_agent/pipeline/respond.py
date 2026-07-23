"""Edge 5 (LLM): computed facts -> natural-language answer with caveats.

The LLM only phrases; every number comes from compute.py. Without a key, a
deterministic template renders the same facts. Confidence and limitations
(tier, staleness, domestic-only long-haul) are always surfaced either way.

Two responders, because a chat has two kinds of turn:
  * respond()      -- a data question: FACTS phrased, with the earlier turns passed
                      alongside so back-references ("it", "those") resolve.
  * respond_meta() -- a message about the conversation itself ("summarize what you
                      told me"): answered from the transcript, with no FACTS at all.
"""

from __future__ import annotations

import json

from .. import config
from .compute import Result


def respond(result: Result, history: list[dict] | None = None) -> str:
    if config.llm_available():
        try:
            return _llm_respond(result, history)
        except Exception:
            pass
    return _template_respond(result)


def _as_dict(result: Result) -> dict:
    return {
        "intent": result.intent, "question": result.question,
        "airports": result.airports, "ranking": result.ranking,
        "unresolved": result.unresolved, "notes": result.notes,
    }


_SYSTEM = (
    "You assist an analyst at a firm that invests in US airport expansion. You are given "
    "the user's question and FACTS that were already computed deterministically. Write a "
    "clear, concise answer.\n"
    "RULES: use ONLY the numbers in FACTS -- never invent or alter a figure. Reproduce "
    "each value EXACTLY as given, including decimals and sign (a long-haul share of 0.4 "
    "is 0.4%, never 40%; do not rescale or round away a leading zero). Each airport "
    "includes a 'score_breakdown' (the formula, each sub-score 0-100, its weight, and "
    "its contribution = sub_score x weight, summing to the total). When you state a "
    "composite score (investment_score or demand_score), SHOW this breakdown -- ideally "
    "a small table with columns metric / sub-score / weight / contribution -- so the "
    "reader sees exactly how the number was built. Use the contribution values as given; "
    "never recompute them. Do NOT output a standalone metric glossary/definitions list -- "
    "the app shows metric definitions separately; keep the answer about THIS question. "
    "Surface "
    "confidence and limitations honestly: Tier 2 airports have no FAA capacity profile "
    "(demand signal only; congestion not measured and not comparable to Tier 1); a "
    "'staleness' flag means the 2014 capacity may understate today's; long-haul share is "
    "domestic-passenger-based. congestion_ratio is annual operations per declared hourly "
    "runway slot (higher = more congested); investment_score and demand_score are 0-100. "
    "If an airport is unresolved/out of scope, say so plainly.\n"
    "CONVERSATION: you may also be given the earlier turns of this chat. Use them to read "
    "the question in context -- to resolve back-references ('it', 'those airports', 'the "
    "one you just mentioned'), to avoid repeating a caveat you already gave, and to stay "
    "consistent with what you already said. FACTS remains the ONLY source of figures for "
    "the current question: never lift a number out of an earlier turn into a new claim "
    "unless it is also in FACTS, and if the two disagree, FACTS wins."
)

# The transcript is passed as plain text rather than as prior assistant messages: the
# earlier answers are evidence to reason over here, not a role-play to continue.
_HISTORY_HEADER = ("CONVERSATION SO FAR (earlier turns of this same chat, oldest first). "
                   "Context only -- the current question is below.")


def _history_block(history: list[dict] | None) -> str:
    if not history:
        return ""
    parts = [_HISTORY_HEADER]
    for i, turn in enumerate(history, 1):
        parts.append(f"[Turn {i}] Analyst asked: {turn.get('question', '')}\n"
                     f"[Turn {i}] You answered:\n{turn.get('answer', '')}")
    return "\n\n".join(parts)


def _llm_respond(result: Result, history: list[dict] | None = None) -> str:
    from .. import llm

    blocks = [b for b in (_history_block(history),) if b]
    blocks.append(f"Question: {result.question}\n\n"
                  f"FACTS (JSON):\n{json.dumps(_as_dict(result), ensure_ascii=False)}")
    resp = llm.get_client().messages.create(
        model=llm.MODEL, max_tokens=700, system=_SYSTEM,
        messages=[{"role": "user", "content": "\n\n---\n\n".join(blocks)}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


# --- meta turns: answered from the transcript, never from a new computation ----

_META_SYSTEM = (
    "You assist an analyst at a firm that invests in US airport expansion. Their latest "
    "message is ABOUT THE CONVERSATION so far -- a request to summarize, recap, restate, "
    "translate or clarify what you already told them -- not a request for new data.\n"
    "RULES: answer from the CONVERSATION SO FAR and nothing else. Reuse every figure "
    "EXACTLY as it already appears there -- never recompute, re-derive, update or round a "
    "number -- and keep each figure's LABEL as well as its value: a Tier-1 airport has an "
    "investment_score, a Tier-2 airport has a demand_score, and calling one by the other's "
    "name misstates what was measured. Never bring in an airport that was not already "
    "discussed. Carry forward "
    "the caveats that applied to those numbers (Tier 2 = demand signal only, congestion "
    "not measured; a staleness flag; long-haul share is domestic-passenger-based). If the "
    "conversation does not contain what is being asked about, say so plainly and name what "
    "you would need to compute -- do not guess.\n"
    "Reply in the language the analyst wrote in, but translate only the PROSE: figures, "
    "units and identifiers stay exactly as they were (miles stay miles -- never convert to "
    "kilometres; $ stays $; IATA codes and airport names stay in Latin script). A converted "
    "unit is a wrong number.\n"
    "Structure a summary as a short through-line first, then the per-airport specifics."
)


def respond_meta(question: str, history: list[dict] | None = None) -> str:
    """Answer a message about the conversation itself (summarize, recap, restate)."""
    if config.llm_available():
        try:
            return _llm_meta(question, history)
        except Exception:
            pass
    return _template_meta(history)


def _llm_meta(question: str, history: list[dict] | None) -> str:
    from .. import llm

    block = _history_block(history) or (
        "CONVERSATION SO FAR: (empty -- this is the analyst's first message)")
    resp = llm.get_client().messages.create(
        model=config.CONVERSATION_MODEL, max_tokens=900, system=_META_SYSTEM,
        messages=[{"role": "user",
                   "content": f"{block}\n\n---\n\nAnalyst's latest message: {question}"}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _template_meta(history: list[dict] | None) -> str:
    """No-key fallback: replay the transcript verbatim rather than paraphrase it.

    Paraphrasing needs a model; repeating what was already computed does not, and a
    verbatim recap can never drift from the figures the analyst was actually shown.
    """
    if not history:
        return ("There is nothing to summarize yet — this is the start of the "
                "conversation. Ask about an airport or a region first.")
    blocks = [f"**Recap of this conversation** ({len(history)} "
              f"{'turn' if len(history) == 1 else 'turns'}, most recent last)"]
    for i, turn in enumerate(history, 1):
        blocks.append(f"**{i}. You asked:** {turn.get('question', '')}\n\n"
                      f"{turn.get('answer', '')}")
    return "\n\n---\n\n".join(blocks)


# --- deterministic template (renders as clean markdown, like the LLM path) ----

def _template_respond(result: Result) -> str:
    blocks: list[str] = []
    if result.intent == "rank" and result.ranking:
        blocks.append(_rank_md(result.ranking))
    else:
        blocks.extend(_airport_md(a) for a in result.airports)
    for name in result.unresolved:
        blocks.append(f"**{name}** could not be identified among the in-scope airports "
                      "(out of scope).")
    if result.notes:
        blocks.append("\n".join(f"> {note}" for note in result.notes))
    blocks = [b for b in blocks if b]
    return "\n\n".join(blocks) if blocks else "No airports identified in the question."


def _rank_md(rk: dict) -> str:
    scope = rk["region"] or "all in-scope airports"
    out = [f"### Top expansion candidates — {scope}"]
    if rk["tier1"]:
        out.append("**Tier 1 — FAA capacity measured (full score)**")
        out += [_ranked_md(i, a) for i, a in enumerate(rk["tier1"], 1)]
    if rk["tier2"]:
        out.append("**Tier 2 — demand signal only (congestion not measured)**")
        out += [_ranked_md(i, a) for i, a in enumerate(rk["tier2"], 1)]
    return "\n\n".join(out)


def _ranked_md(i: int, a: dict) -> str:
    label = "investment score" if a["tier"] == 1 else "demand score"
    head = f"**{i}. {a['iata']} — {a['name']}**  ·  {label} **{a['score']}/100**"
    return head + "\n\n" + _score_table(a["score_breakdown"])


def _airport_md(a: dict) -> str:
    if "error" in a:
        return f"**{a['iata']}**: {a['error']}."
    label = "investment score" if a["tier"] == 1 else "demand score"
    score = a.get("investment_score") if a["tier"] == 1 else a.get("demand_score")
    parts = [f"**{a['iata']} — {a['name']} (Tier {a['tier']})**  ·  {label} **{score}/100**"]
    highlight = _metric_highlight(a)
    if highlight:
        parts.append(highlight)
    parts.append(_score_table(a["score_breakdown"]))
    if a.get("note"):
        parts.append(f"_{a['note']}_")
    return "\n\n".join(parts)


def _metric_highlight(a: dict) -> str | None:
    """A one-line lead for a specifically-requested metric."""
    metric = a.get("requested_metric")
    if metric == "long_haul":
        return f"**Long-haul share: {a['longhaul_share_pct']}%** of departing domestic passengers."
    if metric == "congestion" and a["tier"] == 1:
        return (f"**Congestion: {a['congestion_ratio']}** annual ops per declared hourly slot "
                f"(declared capacity {a['declared_capacity_ops_hr']} ops/hr).")
    if metric == "growth":
        return f"**Growth (2022-2024 CAGR): {a['growth_cagr_pct']}%**."
    if metric == "volume":
        return f"**Annual passengers (CY24): {a['annual_passengers_cy24']:,}**."
    return None


def _score_table(bd: dict) -> str:
    rows = ["| Metric | Sub-score (0-100) | Weight | Contribution |",
            "|---|---|---|---|"]
    for c in bd["components"]:
        rows.append(f"| {c['metric'].title()} | {c['sub_score_0_100']} | "
                    f"{c['weight']} | {c['contribution']} |")
    rows.append(f"| **Total** |  |  | **{bd['total']}** |")
    return "\n".join(rows)
