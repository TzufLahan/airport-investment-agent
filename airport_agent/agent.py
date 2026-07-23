"""End-to-end pipeline orchestration: a question in, an answer out.

Wires the five stages together (design doc section 4):
    understand (LLM) -> resolve (code) -> route/compute (code) -> respond (LLM)
The deterministic core (resolve -> compute) is unchanged whether or not an LLM key
is present; only the two edges swap between Claude and their fallbacks.

Conversation memory lives in the opaque `context` dict that ask() returns and the
caller hands back on the next turn. It carries two different things, because
follow-ups need both:

  * the SUBJECT (airports / region / metric) of the last turn, so a question that
    names none of its own inherits it -- "and why?", "what about its growth?";
  * the TRANSCRIPT (the last few question/answer pairs), so the responder can read
    a question in context and so a message about the conversation itself
    ("summarize the previous answers") has something to summarize.

Subject alone is not enough: a ranking question names no airport, so after one the
subject is empty and only the transcript remembers what was actually shown.
"""

from .pipeline import resolve as _resolve
from .pipeline import respond as _respond
from .pipeline import second_opinion as _second_opinion
from .pipeline import understand as _understand
from .pipeline.compute import Result, compute
from .pipeline.understand import Query

# How much conversation to carry. Both caps exist to keep the prompt bounded: the
# answers are table-heavy, so a long chat would otherwise grow without limit.
MAX_HISTORY_TURNS = 6
MAX_ANSWER_CHARS = 2000
# Airports inherited from a ranking (which lists up to 6 per tier); enough for a
# follow-up to stay on topic without re-answering for a dozen airports.
MAX_INHERITED_IATAS = 6


def ask(question: str, context: dict | None = None) -> tuple[str, dict]:
    """Answer one question. Returns (answer, new_context) for follow-ups."""
    context = context or {}
    history: list[dict] = list(context.get("history") or [])

    query = _understand.understand(question)
    _inherit_subject(query, context)

    result: Result | None = None
    if query.intent != "meta":
        resolution = _resolve.resolve(query.airports)
        result = compute(query, resolution.resolved, resolution.unresolved)
        if _is_empty(result) and history:
            # Nothing to say from the data and the subject could not be recovered --
            # but there IS a conversation. Answer from it instead of reporting that
            # no airport was found, which is what the analyst actually asked about.
            result = None

    if result is None:
        answer = _respond.respond_meta(question, history)
        iatas = list(context.get("iatas") or [])
    else:
        answer = _respond.respond(result, history)
        # An independent FAA-NPIAS "second opinion" beside the score; a failure here
        # must never break the primary answer, so it is best-effort.
        try:
            extra = _second_opinion.second_opinion(result)
        except Exception:
            extra = None
        if extra:
            answer = f"{answer}\n\n---\n\n{extra}"
        iatas = _subject_iatas(result)

    return answer, _next_context(query, context, history, question, answer, iatas)


def _inherit_subject(query: Query, context: dict) -> None:
    """Carry the previous turn's subject into a follow-up that names none of its own.

    A 'meta' turn is skipped: it is answered from the transcript, so giving it a
    subject would only invite the responder to compute something new.
    """
    if query.intent == "meta":
        return
    if not query.airports:
        # The previous turn's natural names -- or, after a ranking (which names no
        # airport of its own), the codes that answer actually showed. Codes resolve
        # through the same alias map, so the deterministic core is unchanged.
        query.airports = list(context.get("airports") or context.get("iatas") or [])
    if not query.region:
        query.region = context.get("region")
    if not query.metric:
        query.metric = context.get("metric")


def _is_empty(result: Result) -> bool:
    """True when the turn produced nothing to talk about: no airport, no ranking,
    and not even a name to report as out of scope."""
    return not result.airports and not result.ranking and not result.unresolved


def _subject_iatas(result: Result) -> list[str]:
    """The airports this answer actually discussed -- the subject a follow-up inherits."""
    if result.ranking:
        entries = result.ranking["tier1"] + result.ranking["tier2"]
        return [e["iata"] for e in entries][:MAX_INHERITED_IATAS]
    return [a["iata"] for a in result.airports if "error" not in a]


def _next_context(query: Query, context: dict, history: list[dict], question: str,
                  answer: str, iatas: list[str]) -> dict:
    """The context the caller hands back on the next turn.

    A meta turn talks ABOUT the conversation without changing what it is about, so it
    passes the previous subject through untouched -- otherwise a "summarize that" in
    the middle of a thread would orphan the follow-up after it.
    """
    if query.intent == "meta":
        airports = list(context.get("airports") or [])
        region, metric = context.get("region"), context.get("metric")
    else:
        airports, region, metric = query.airports, query.region, query.metric

    turn = {"question": question, "answer": _trim(answer)}
    return {
        "airports": airports,
        "region": region,
        "metric": metric,
        "iatas": iatas,
        "history": (history + [turn])[-MAX_HISTORY_TURNS:],
    }


def _trim(answer: str) -> str:
    """Bound the stored copy of an answer; the tables at the end are the expendable
    part, so a head truncation keeps the substance."""
    if len(answer) <= MAX_ANSWER_CHARS:
        return answer
    return answer[:MAX_ANSWER_CHARS].rstrip() + "\n[... answer truncated ...]"
