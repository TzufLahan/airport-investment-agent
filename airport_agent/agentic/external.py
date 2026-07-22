"""World-facing tools: web search + URL fetch.

These bring in fresh, qualitative context (recent news, an FAA page) that the
cached deterministic data cannot. They are best-effort and degrade gracefully:
on failure they return an empty/`note` result so the agent can carry on. Their
output is qualitative -- the agent must present it BESIDE the deterministic score
with its source, never let it drive a number (the same rule as the NPIAS view).
"""

from __future__ import annotations

import html as _html
import re
import urllib.parse

import requests

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def _strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return _html.unescape(re.sub(r"\s+", " ", s)).strip()


def _ddg_unwrap(href: str) -> str:
    """DuckDuckGo wraps result links in a redirect; pull out the real URL."""
    full = href if href.startswith("http") else "https:" + href
    params = urllib.parse.parse_qs(urllib.parse.urlparse(full).query)
    return params.get("uddg", [full])[0]


def web_search(query: str, num_results: int = 5) -> dict:
    """Keyless web search via the DuckDuckGo HTML endpoint (best-effort)."""
    try:
        resp = requests.post("https://html.duckduckgo.com/html/",
                             data={"q": query}, headers={"User-Agent": _UA}, timeout=15)
        page = resp.text
    except Exception as exc:  # network/endpoint issue -> honest empty result
        return {"query": query, "results": [], "note": f"search unavailable ({exc})"}

    results = []
    for m in re.finditer(r'result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
        results.append({"title": _strip_tags(m.group(2)), "url": _ddg_unwrap(m.group(1))})
        if len(results) >= num_results:
            break
    snippets = [_strip_tags(s) for s in
                re.findall(r'result__snippet"[^>]*>(.*?)</a>', page, re.S)]
    for i, r in enumerate(results):
        if i < len(snippets):
            r["snippet"] = snippets[i][:300]

    if not results:
        return {"query": query, "results": [], "note": "no results (may be rate-limited)"}
    return {"query": query, "results": results}


def fetch_url(url: str, max_chars: int = 3000) -> dict:
    """Fetch a page and return its readable text (tags stripped, truncated)."""
    try:
        resp = requests.get(url, headers={"User-Agent": _UA}, timeout=20)
    except Exception as exc:
        return {"url": url, "error": str(exc)}
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", resp.text)
    return {"url": url, "status": resp.status_code, "text": _strip_tags(body)[:max_chars]}


SCHEMAS = [
    {"name": "web_search",
     "description": "Search the web for recent, qualitative context an investment "
                    "analyst would want -- news, a new terminal announcement, a funding "
                    "bill. Returns title/url/snippet. Present findings as external context "
                    "with the source; never let them change a computed score.",
     "input_schema": {"type": "object",
                      "properties": {"query": {"type": "string"},
                                     "num_results": {"type": "integer"}},
                      "required": ["query"]}},
    {"name": "fetch_url",
     "description": "Fetch the readable text of a specific URL (e.g. an FAA page found "
                    "via web_search). Returns truncated page text.",
     "input_schema": {"type": "object",
                      "properties": {"url": {"type": "string"},
                                     "max_chars": {"type": "integer"}},
                      "required": ["url"]}},
]

DISPATCH = {"web_search": web_search, "fetch_url": fetch_url}
