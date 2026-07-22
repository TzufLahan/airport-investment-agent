"""Streamlit UI for the autonomous tool-using agent -- same immersive design as app.py.

Two views:
  * an immersive landing page (looping airport video background + a CTA), and
  * a chat that streams the agent's "thinking" (each tool it decides to call) and
    then the final answer, with an expandable tool trace on every past turn.

Run:  streamlit run agent_app.py
Needs ANTHROPIC_API_KEY (the agent orchestrates tool calls; there is no offline
loop). The deterministic-workflow UI is the separate `streamlit run app.py`.
"""

import json
from pathlib import Path

import streamlit as st

from airport_agent import config
from airport_agent.agentic.agent import AgenticAgent

st.set_page_config(page_title="Airport Agent (autonomous)", page_icon="🤖", layout="centered")

EXAMPLES = [
    "Compare Denver and Salt Lake City, and what does the FAA say about each?",
    "Find Tier-1 airports the FAA flags constrained by 2033 with our congestion "
    "under 65, ranked by growth.",
    "If I care about growth twice as much as congestion, who are the top 5?",
    "What's the main airport serving Silicon Valley, and how is it growing?",
    "Any recent news about SFO expansion?",
]

VIDEO_FILE = Path(__file__).parent / "static" / "airport.mp4"

st.session_state.setdefault("display", [])
st.session_state.setdefault("pending", None)
st.session_state.setdefault("entered", False)


# =============================================================================
# Landing page  (identical design to app.py)
# =============================================================================

_LANDING_CSS = """
<style>
  header[data-testid="stHeader"], [data-testid="stToolbar"] {display: none;}
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
        '<span class="eyebrow">🤖 Autonomous · Tool-using</span>'
        '<h1>An agent that<br>reasons with tools</h1>'
        '<p>Ask an open-ended question. The agent decides which tools to call — scoring, '
        'ranking, FAA NPIAS, web search, memory — and chains them to an answer. You watch '
        'every step; every number still comes from a deterministic tool.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    left, mid, right = st.columns([1, 1.4, 1])
    with mid:
        if st.button("Enter the agent  →", type="primary", use_container_width=True):
            st.session_state.entered = True
            st.rerun()
    st.markdown(
        '<div class="hero facts" style="margin-top:1rem">11 tools · deterministic core · '
        'Claude Sonnet 5</div>',
        unsafe_allow_html=True,
    )


if not st.session_state.entered:
    render_landing()
    st.stop()


# =============================================================================
# Chat view
# =============================================================================

if not config.llm_available():
    st.error("This agent needs **ANTHROPIC_API_KEY** in your `.env` — it orchestrates tool "
             "calls, so there is no offline mode. (The deterministic workflow, "
             "`streamlit run app.py`, runs without a key.)")
    st.stop()

if "agent" not in st.session_state:
    st.session_state.agent = AgenticAgent()


def _fmt(value, limit=220) -> str:
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return s if len(s) <= limit else s[:limit] + " ..."


with st.sidebar:
    st.header("🤖 Autonomous agent")
    st.caption(f"Model: {config.AGENT_MODEL}  ·  tool-using loop")

    st.subheader("Try an example")
    for example in EXAMPLES:
        if st.button(example, use_container_width=True):
            st.session_state.pending = example

    with st.expander("🧰 Tools the agent can call"):
        st.markdown(
            "**Deterministic (numbers):**\n"
            "- `resolve_airport` · `get_airport_score` · `compare_airports`\n"
            "- `rank_airports` · `set_weights` · `list_scope` · `get_npias`\n\n"
            "**External (context):** `web_search` · `fetch_url`\n\n"
            "**Memory:** `save_memory` · `search_memory`")

    with st.expander("ℹ️ How it works"):
        st.markdown(
            "The model **chooses** which tools to call and **chains** them to answer "
            "open-ended, multi-step questions. Every number comes from a deterministic "
            "tool — the model never invents figures. External/web results are shown as "
            "context beside the score, never inside it.")

    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.agent = AgenticAgent()
        st.session_state.display = []
        st.rerun()

st.title("🤖 Airport Investment — Autonomous Agent")
st.caption("The model decides which tools to call; every number comes from a deterministic "
           "tool. Expand any turn to see the tool trace.")

# --- render conversation history ---------------------------------------------
for msg in st.session_state.display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("trace"):
            with st.expander(f"🔧 {len(msg['trace'])} tool call(s)"):
                for t in msg["trace"]:
                    st.markdown(f"**{t['tool']}** &nbsp; `{_fmt(t['input'], 120)}`")
                    st.caption(t["output"])

# --- new turn ----------------------------------------------------------------
prompt = st.chat_input("Ask the agent...")
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None

if prompt:
    st.session_state.display.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        turn_trace: list[dict] = []
        with st.status("Thinking — deciding which tools to call...", expanded=True) as status:
            def on_tool(name, inp, out):
                st.markdown(f"🔧 **{name}** &nbsp; `{_fmt(inp, 120)}`")
                st.caption(_fmt(out))
                turn_trace.append({"tool": name, "input": inp, "output": _fmt(out)})

            try:
                result = st.session_state.agent.ask(prompt, on_tool=on_tool)
            except Exception as exc:
                result = {"answer": f"Sorry, I hit an error: {exc}"}
            status.update(label=f"Done — {len(turn_trace)} tool call(s)",
                          state="complete", expanded=False)
        st.markdown(result["answer"])

    st.session_state.display.append(
        {"role": "assistant", "content": result["answer"], "trace": turn_trace})
