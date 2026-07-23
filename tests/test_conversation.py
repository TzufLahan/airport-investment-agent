"""Deterministic tests for multi-turn conversation memory (no LLM required).

Every test forces the no-key path so the keyword parser and the template responder
answer -- the routing being tested (subject inheritance, meta detection, transcript
carry-over) is deterministic and must hold on both paths.
"""

import pytest

from airport_agent import config
from airport_agent.agent import MAX_HISTORY_TURNS, ask
from airport_agent.pipeline import understand as u


@pytest.fixture(autouse=True)
def no_llm(monkeypatch):
    monkeypatch.setattr(config, "ANTHROPIC_API_KEY", None)


# --- intent classification ----------------------------------------------------

@pytest.mark.parametrize("question", [
    "Please summarize the previous answers",
    "summarize what you just told me",
    "Can you recap everything so far?",
    "what did you say earlier?",
])
def test_meta_questions_are_classified_as_meta(question):
    assert u.understand(question).intent == "meta"


@pytest.mark.parametrize("question", [
    "Summarize the congestion at SFO",          # names an airport -> a data question
    "Summarize the New England candidates",     # names a region  -> a data question
    "What is the growth at Anchorage?",
])
def test_data_questions_are_not_meta(question):
    assert u.understand(question).intent != "meta"


# --- subject inheritance ------------------------------------------------------

def test_followup_inherits_the_previous_airport():
    _, ctx = ask("What is the percentage of long-haul flights out of Anchorage?")
    answer, _ = ask("And what about its growth?", ctx)
    assert "ANC" in answer


def test_followup_after_a_ranking_recovers_the_ranked_airports():
    """A ranking names no airport, so the subject can only come from what it showed."""
    _, ctx = ask("Which airports in New England are strong candidates?")
    assert ctx["airports"] == []          # the ranking question itself named none
    assert ctx["iatas"]                   # but the answer did show airports
    answer, _ = ask("What are their growth rates?", ctx)
    assert answer != "No airports identified in the question."
    assert any(code in answer for code in ctx["iatas"])


def test_new_subject_replaces_the_inherited_one():
    _, ctx = ask("What is the congestion at SFO?")
    answer, ctx2 = ask("What about Santa Ana?", ctx)
    assert "SNA" in answer
    assert ctx2["airports"] == ["santa ana"]


# --- transcript ---------------------------------------------------------------

def test_summarize_answers_from_the_transcript():
    _, ctx = ask("What is the percentage of long-haul flights out of Anchorage?")
    answer, _ = ask("Please summarize the previous answers", ctx)
    # The recap replays what was actually shown -- not a fresh "no airports" report.
    assert "Recap of this conversation" in answer
    assert "ANC" in answer
    assert "No airports identified" not in answer


def test_summarize_with_no_history_says_so_plainly():
    answer, _ = ask("Please summarize the previous answers")
    assert "nothing to summarize" in answer.lower()


def test_meta_turn_preserves_the_subject_for_the_next_followup():
    _, ctx = ask("What is the congestion at SFO?")
    _, ctx2 = ask("Summarize that for me", ctx)
    assert ctx2["airports"] == ctx["airports"]     # the thread is still about SFO
    answer, _ = ask("And its growth?", ctx2)
    assert "SFO" in answer


def test_history_is_recorded_and_bounded():
    ctx: dict = {}
    for _ in range(MAX_HISTORY_TURNS + 3):
        _, ctx = ask("What is the congestion at SFO?", ctx)
    assert len(ctx["history"]) == MAX_HISTORY_TURNS
    assert set(ctx["history"][0]) == {"question", "answer"}
