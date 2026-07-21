"""Per-feature normalization to a 0-100 scale.

The transform is chosen per feature by its distribution (design doc 5): linear
min-max for the bounded ratio features (congestion, growth), and log min-max for
the heavy-tailed volume feature -- a few giants (ATL, LAX) would otherwise crush
mid-size airports to near zero.

NaN inputs are ignored when finding the range and stay NaN in the output, so a
feature that exists only for Tier-1 (congestion) is normalized over exactly the
airports that have it, with no special-casing by the caller.
"""

import numpy as np
import pandas as pd

NEUTRAL = 50.0  # score when a feature has no spread (all values equal)


def minmax(values: pd.Series) -> pd.Series:
    """Linear min-max of a series to 0-100. NaNs pass through as NaN."""
    lo = values.min(skipna=True)
    hi = values.max(skipna=True)
    if pd.isna(lo) or hi == lo:
        return values.notna().map({True: NEUTRAL, False: np.nan}).astype(float)
    return 100.0 * (values - lo) / (hi - lo)


def log_minmax(values: pd.Series) -> pd.Series:
    """Min-max on a log10 scale, for heavy-tailed features (volume)."""
    return minmax(np.log10(values))
