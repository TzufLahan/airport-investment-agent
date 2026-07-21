"""Deterministic scoring: sub-scores, weighted total, and tier-aware ranking.

Pure, reproducible Python -- no LLM ever touches these numbers. Same input always
produces the same output (locked by tests/test_scoring.py).
"""

from .score import score_airports, ranked
from .weights import WEIGHTS

__all__ = ["score_airports", "ranked", "WEIGHTS"]
