"""Tunable scoring parameters, exposed at the top on purpose.

An analyst can re-weight and rerun to see how the ranking shifts -- this turns a
black-box score into a transparent analysis tool. Equal congestion/growth (0.4
each) is the neutral, defensible default absent a data-driven reason to prefer
one; volume is a secondary size multiplier (0.2).
"""

WEIGHTS = {
    "congestion": 0.4,  # actual peak load vs declared FAA capacity (most trusted)
    "growth": 0.4,      # forward-looking demand trend (the investment thesis)
    "volume": 0.2,      # size multiplier -- a big airport's problem is a bigger bet
}

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "WEIGHTS must sum to 1.0"
