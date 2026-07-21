"""Central configuration: filesystem paths and model settings.

Declarative on purpose — no data is loaded here. Every module imports these
constants so that paths and tunable settings live in exactly one place.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env (if present) so ANTHROPIC_API_KEY becomes available via os.environ.
# A missing key is NOT fatal: the pipeline degrades to a deterministic fallback
# (see pipeline/understand.py and pipeline/respond.py).
load_dotenv()

# --- Filesystem layout -------------------------------------------------------
# BASE_DIR is the repository root (the parent of the airport_agent package).
BASE_DIR = Path(__file__).resolve().parent.parent

REFERENCE_DIR = BASE_DIR / "reference"        # curated source-of-truth CSVs
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"                     # large BTS downloads (gitignored)
PROCESSED_DIR = DATA_DIR / "processed"         # small committed snapshot

# Reference tables (built in Step 1)
AIRPORTS_CSV = REFERENCE_DIR / "airports.csv"
FAA_CAPACITY_CSV = REFERENCE_DIR / "faa_capacity.csv"

# Processed per-airport metrics snapshot (built once by scripts/fetch_data.py,
# committed to the repo; the agent reads this, never the live endpoints).
AIRPORT_METRICS = PROCESSED_DIR / "airport_metrics.csv"

# --- Data-acquisition parameters ---------------------------------------------
# Latest complete year (volume/ops/long-haul) and the base year for the growth
# trend. Growth = CAGR of BTS passengers between the two (design decision: recent
# post-recovery momentum; short window can flatter airports still rebounding).
LATEST_YEAR = 2024
GROWTH_BASE_YEAR = 2022
# A market is "long-haul" if its distance exceeds this many statute miles.
LONG_HAUL_MILES = 3000

# --- LLM settings ------------------------------------------------------------
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
# Small, fast model: the LLM does only light entity/intent extraction and
# phrasing at the edges — never numeric work — so a compact model suffices.
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"


def llm_available() -> bool:
    """True if an API key is configured. When False, the pipeline takes its
    deterministic fallback path so the core still runs end-to-end."""
    return bool(ANTHROPIC_API_KEY)


def ensure_dirs() -> None:
    """Create data directories if missing (called by the loader before writes)."""
    for directory in (RAW_DIR, PROCESSED_DIR):
        directory.mkdir(parents=True, exist_ok=True)
