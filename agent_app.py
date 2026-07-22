"""Streamlit UI for the autonomous tool-using agent.

Run:  streamlit run agent_app.py

Shows the agent's live "thinking" -- each tool it decides to call, with its input
and a preview of the result -- inside a status box, then the final answer below.
Every past turn keeps an expandable tool trace. Needs ANTHROPIC_API_KEY (the agent
orchestrates tool calls; there is no offline loop). The deterministic workflow UI
is the separate `streamlit run app.py`.
"""

import json

import streamlit as st

from airport_agent import config
from airport_agent.agentic.agent import AgenticAgent

st.set_page_config(page_title="Airport Agent (autonomous)", page_icon="🤖", layout="centered")
st.title("🤖 Airport Investment — Autonomous Agent")
st.caption("The model decides which tools to call; every number still comes from a "
           "deterministic tool. Expand any turn to see the tool trace.")

if not config.llm_available():
    st.error("This agent needs **ANTHROPIC_API_KEY** in your `.env` — it orchestrates tool "
             "calls, so there is no offline mode. (The deterministic workflow, "
             "`streamlit run app.py`, runs without a key.)")
    st.stop()

# One agent per session = its short-term (conversation) memory.
if "agent" not in st.session_state:
    st.session_state.agent = AgenticAgent()
    st.session_state.display = []


def _fmt(value, limit=220) -> str:
    s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return s if len(s) <= limit else s[:limit] + " ..."


with st.sidebar:
    st.header("🤖 Autonomous agent")
    st.markdown("**Tools the agent can call:**")
    st.markdown(
        "- `resolve_airport` · `get_airport_score` · `compare_airports`\n"
        "- `rank_airports` · `set_weights` · `list_scope`\n"
        "- `get_npias` — FAA second opinion\n"
        "- `web_search` · `fetch_url` — external context\n"
        "- `save_memory` · `search_memory` — long-term memory")
    st.caption(f"Model: {config.AGENT_MODEL}")
    st.divider()
    st.markdown("**Try a multi-step question:**")
    st.markdown("- *Find Tier-1 airports the FAA flags constrained by 2033 with our "
                "congestion under 65, ranked by growth.*\n"
                "- *If I care about growth twice as much as congestion, who are the top 5?*\n"
                "- *Compare Denver and Salt Lake City, and what does the FAA say about each?*")
    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.agent = AgenticAgent()
        st.session_state.display = []
        st.rerun()

# --- render conversation history ---------------------------------------------
for msg in st.session_state.display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("trace"):
            with st.expander(f"🔧 {len(msg['trace'])} tool call(s)"):
                for t in msg["trace"]:
                    st.markdown(f"**{t['tool']}** &nbsp; `{_fmt(t['input'], 120)}`")
                    st.caption(_fmt(t["output"]))

# --- new turn ----------------------------------------------------------------
prompt = st.chat_input("Ask the agent...")
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
