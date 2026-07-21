"""Thin Claude client for the two LLM edges (understand, respond).

All Anthropic SDK usage is isolated here. The client is constructed lazily and
only when config.llm_available() is True -- so the deterministic fallback path
(and the tests) never import the SDK or need a key.
"""

from functools import lru_cache

from . import config


@lru_cache(maxsize=1)
def get_client():
    """Return a cached Anthropic client. Reads ANTHROPIC_API_KEY from the env,
    which config.load_dotenv() has already populated from .env."""
    import anthropic  # imported lazily so the no-key path has no hard dependency

    return anthropic.Anthropic()


MODEL = config.ANTHROPIC_MODEL  # Haiku 4.5: light entity/intent + phrasing work
