"""End-to-end pipeline orchestration: a question in, an answer out.

Wires the five stages together (design doc section 4):
    understand (LLM) -> resolve (code) -> route/compute (code) -> respond (LLM)
The deterministic core (resolve -> compute) is unchanged whether or not an LLM key
is present; only the two edges swap between Claude and their fallbacks.

Light conversation memory supports follow-ups: if a turn names no airport/region,
it inherits the previous turn's, so "and why?" or "what about its growth?" resolve
against what was just discussed.
"""

from .pipeline import resolve as _resolve
from .pipeline import respond as _respond
from .pipeline import understand as _understand
from .pipeline.compute import compute


def ask(question: str, context: dict | None = None) -> tuple[str, dict]:
    """Answer one question. Returns (answer, new_context) for follow-ups."""
    query = _understand.understand(question)

    if context:  # inherit subject from the previous turn for follow-ups
        if not query.airports and context.get("airports"):
            query.airports = context["airports"]
        if not query.region and context.get("region"):
            query.region = context["region"]

    resolution = _resolve.resolve(query.airports)
    result = compute(query, resolution.resolved, resolution.unresolved)
    answer = _respond.respond(result)

    new_context = {"airports": query.airports, "region": query.region}
    return answer, new_context
