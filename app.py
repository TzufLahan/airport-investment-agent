"""Streamlit UI for the Airport Investment Intelligence Agent.

Two views:
  * an immersive landing page (looping airport video background + a CTA), and
  * the chat, a thin view over agent.ask().
The deterministic core and LLM pipeline are unchanged; conversation memory for
follow-ups lives in st.session_state (Streamlit re-runs this script per interaction).

Run:  streamlit run app.py
The landing video is served from static/airport.mp4 (drop your own clip there).
"""

from pathlib import Path

import streamlit as st

from airport_agent import config, reference
from airport_agent.agent import ask
from airport_agent.pipeline.compute import _DEFINITIONS as METRIC_DEFINITIONS

st.set_page_config(page_title="Airport Investment Agent", page_icon="✈️", layout="centered")

EXAMPLES = [
    "Which airports in New England are strong candidates for terminal expansion?",
    "Compare LA and Santa Ana congestion levels.",
    "What is the percentage of long-haul flights out of Anchorage?",
    "What is the unmet demand at SFO and why?",
    "Which airport serves Silicon Valley?",
]

VIDEO_FILE = Path(__file__).parent / "static" / "airport.mp4"

st.session_state.setdefault("messages", [])
st.session_state.setdefault("context", {})
st.session_state.setdefault("pending", None)
st.session_state.setdefault("entered", False)


# =============================================================================
# Landing page
# =============================================================================

_LANDING_CSS = """
<style>
  header[data-testid="stHeader"], [data-testid="stToolbar"] {display: none;}
  /* Dark backdrop goes on <body> (behind the fixed video). Every Streamlit
     container above the video must be transparent, or it covers the video. */
  body {background: #05070d;}
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
  section.main, [data-testid="stMainBlockContainer"], .block-container {
    background: transparent !important;
  }
  .block-container {padding-top: 0 !important; max-width: 920px;}

  #bgvid {
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    object-fit: cover; z-index: -2; filter: saturate(1.1) brightness(0.62);
  }
  .hero-overlay {
    position: fixed; inset: 0; z-index: -1;
    background:
      radial-gradient(1100px 560px at 50% -12%, rgba(56,132,255,.28), transparent 60%),
      linear-gradient(180deg, rgba(5,7,13,.30) 0%, rgba(5,7,13,.58) 45%, rgba(5,7,13,.94) 100%);
  }
  .hero {
    text-align: center; margin-top: 15vh; padding: 0 1rem; color: #fff;
    animation: fadeUp .9s ease both;
  }
  .hero .eyebrow {
    display: inline-block; padding: .42rem .95rem; margin-bottom: 1.4rem;
    border: 1px solid rgba(255,255,255,.18); border-radius: 999px;
    font-size: .78rem; letter-spacing: .16em; text-transform: uppercase;
    color: #cfe0ff; background: rgba(255,255,255,.06); backdrop-filter: blur(6px);
  }
  .hero h1 {
    font-size: clamp(2.4rem, 6vw, 4.4rem); line-height: 1.04; font-weight: 800;
    letter-spacing: -.02em; margin: 0 0 1.1rem;
    background: linear-gradient(180deg, #ffffff, #b9d0ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .hero p {
    font-size: clamp(1rem, 2.1vw, 1.28rem); max-width: 660px; margin: 0 auto 2.2rem;
    color: #c6ccd8; line-height: 1.62;
  }
  .hero .facts {
    color: #8b93a7; font-size: .92rem; margin-top: 2.4rem; letter-spacing: .02em;
  }
  /* premium CTA (the only button on this view) */
  .stButton > button {
    background: linear-gradient(180deg, #3b82f6, #2563eb); color: #fff; border: 0;
    padding: .95rem 1.7rem; font-size: 1.06rem; font-weight: 600; border-radius: 12px;
    box-shadow: 0 12px 34px rgba(37,99,235,.45); transition: transform .15s, box-shadow .15s;
  }
  .stButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 18px 44px rgba(37,99,235,.62);
  }
  @keyframes fadeUp {from {opacity: 0; transform: translateY(22px);} to {opacity: 1; transform: none;}}
</style>
"""


def render_landing() -> None:
    video = ('<video id="bgvid" autoplay muted loop playsinline>'
             '<source src="app/static/airport.mp4" type="video/mp4"></video>'
             if VIDEO_FILE.exists() else "")
    st.markdown(
        _LANDING_CSS + video + '<div class="hero-overlay"></div>'
        '<div class="hero">'
        '<span class="eyebrow">✈ Airport Investment Intelligence</span>'
        '<h1>Where should the next<br>runway dollar go?</h1>'
        '<p>An AI analyst that ranks US airports for expansion potential — congestion, '
        'demand growth, and volume, computed deterministically from real FAA and BTS '
        'data. Ask in plain English; get a transparent, sourced answer.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    left, mid, right = st.columns([1, 1.4, 1])
    with mid:
        if st.button("Start the analysis  →", type="primary", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown(
        '<div class="hero facts" style="margin-top:1rem">65 airports · deterministic '
        'scoring · FAA capacity + BTS T-100</div>',
        unsafe_allow_html=True,
    )


if not st.session_state.entered:
    render_landing()
    st.stop()


# =============================================================================
# Chat view
# =============================================================================

with st.sidebar:
    st.header("✈️ Airport Investment Agent")
    st.caption("Mode: " + ("Claude (LLM edges)" if config.llm_available()
                           else "Deterministic fallback (no API key)"))

    st.subheader("Try an example")
    for example in EXAMPLES:
        if st.button(example, use_container_width=True):
            st.session_state.pending = example

    airports = reference.load_airports()
    st.subheader(f"Scope: {len(airports)} airports")
    with st.expander("Which airports?"):
        for tier, label in [(1, "Tier 1 - FAA capacity, full score"),
                            (2, "Tier 2 - demand signal only")]:
            sub = airports[airports.tier == tier].sort_values("iata")
            lines = "\n".join(f"- `{code}` — {name}"
                              for code, name in zip(sub["iata"], sub["name"]))
            st.markdown(f"**{label}**\n\n{lines}")

    with st.expander("📖 What the metrics mean"):
        for key, text in METRIC_DEFINITIONS.items():
            st.markdown(f"**{key.replace('_', ' ').title()}** — {text}")

    with st.expander("🏛️ About the FAA NPIAS view"):
        st.markdown(
            "An independent **second opinion** shown beside our score — never part of it. "
            "Two signals from the FAA's **NPIAS 2025-2029**:\n\n"
            "- **Development cost** — the FAA's own 5-year $ estimate of each airport's "
            "build-out need (shown as a percentile across the 65 airports).\n"
            "- **Capacity outlook** — the FAA's projected runway status for 2028 & 2033: "
            "not flagged → congested → capacity constrained → severe.\n\n"
            "_\"Not flagged\" means an airport isn't on the FAA's constrained list — "
            "not proof it's fine._"
        )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.context = {}
        st.rerun()

st.title("Airport Investment Intelligence Agent")
st.caption("Ask which US airports are the best expansion investments. Every score is "
           "computed deterministically; the assistant only phrases the numbers.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about US airport expansion...")
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                answer, st.session_state.context = ask(prompt, st.session_state.context)
            except Exception as exc:  # never let one bad turn break the app
                answer = f"Sorry, I hit an error: {exc}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
