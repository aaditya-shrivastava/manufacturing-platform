import streamlit as st
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crewai import Crew, Process
from agents.researcher_agent import create_researcher_agent
from agents.writer_agent import create_writer_agent
from tasks.research_task import create_research_task
from tasks.writing_task import create_writing_task
from memory.search_history import save_memory, get_memory_context, load_memory
from tools.docx_exporter import export_to_docx

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Manufacturing System",
    page_icon="🏭",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.2rem 0;
    }
    .hero-sub {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .agent-card h4 { color: #00d4ff; margin: 0 0 0.4rem 0; }
    .agent-card p  { color: #aaa; margin: 0; font-size: 0.88rem; }

    .metric-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-val   { font-size: 1.8rem; font-weight: 700; color: #00d4ff; }
    .metric-label { font-size: 0.8rem; color: #888; margin-top: 0.2rem; }

    .status-running { color: #ffa500; font-weight: 600; }
    .status-done    { color: #00cc66; font-weight: 600; }

    .memory-entry {
        background: #1a1d27;
        border-left: 3px solid #00d4ff;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.85rem;
    }
    .memory-date  { color: #555; font-size: 0.75rem; }
    .memory-query { color: #eee; margin: 0.2rem 0; }
    .memory-sum   { color: #888; font-size: 0.78rem; }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        width: 100%;
    }
    div[data-testid="stButton"] button:hover {
        opacity: 0.85 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────
if "report_md"   not in st.session_state: st.session_state.report_md   = None
if "report_path" not in st.session_state: st.session_state.report_path = None
if "docx_path"   not in st.session_state: st.session_state.docx_path   = None
if "running"     not in st.session_state: st.session_state.running     = False
if "agent_logs"  not in st.session_state: st.session_state.agent_logs  = []
if "total_runs"  not in st.session_state: st.session_state.total_runs  = 0
if "prefill"     not in st.session_state: st.session_state.prefill     = ""


# ── Header ────────────────────────────────────────────────
st.markdown('<div class="hero-title">🏭 Multi-Agent Manufacturing System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Powered by CrewAI · Groq · Llama 3.3 70B · DuckDuckGo Search</div>', unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────
left, right = st.columns([1, 2], gap="large")

# ════════════════════════════════════════════════════════════
# LEFT PANEL
# ════════════════════════════════════════════════════════════
with left:
    st.markdown("### 🤖 Active Agents")
    st.markdown("""
    <div class="agent-card">
        <h4>🔍 Researcher Agent</h4>
        <p>Searches the web for suppliers, pricing, specs, lead times & certifications.</p>
    </div>
    <div class="agent-card">
        <h4>✍️ Writer Agent</h4>
        <p>Synthesizes research into a professional procurement report with recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Metrics
    memory = load_memory()
    total_searches = len(memory.get("searches", []))
    st.markdown("### 📊 System Stats")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{total_searches}</div>
            <div class="metric-label">Past Searches</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-val">{st.session_state.total_runs}</div>
            <div class="metric-label">This Session</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Memory history
    st.markdown("### 🧠 Search Memory")
    searches = memory.get("searches", [])
    if not searches:
        st.caption("No searches yet. Run your first query!")
    else:
        for entry in reversed(searches[-5:]):
            date = entry["timestamp"][:10]
            st.markdown(f"""
            <div class="memory-entry">
                <div class="memory-date">📅 {date}</div>
                <div class="memory-query">🔍 {entry['query']}</div>
                <div class="memory-sum">{entry['summary'][:120]}...</div>
            </div>""", unsafe_allow_html=True)

    if searches:
        if st.button("🗑️ Clear Memory"):
            os.makedirs("memory", exist_ok=True)
            with open("memory/search_history.json", "w") as f:
                json.dump({"searches": []}, f)
            st.success("Memory cleared!")
            st.rerun()


# ════════════════════════════════════════════════════════════
# RIGHT PANEL
# ════════════════════════════════════════════════════════════
with right:
    st.markdown("### 🔍 Manufacturing Research Query")

    # ── Suggestion buttons ────────────────────────────────
    st.caption("💡 Quick suggestions:")
    suggestions = [
        "Find top suppliers for carbon fiber sheets for aerospace",
        "Source lithium-ion battery components for EV manufacturing",
        "Find CNC machining service providers for precision metal parts",
        "Source stainless steel pipes for automotive manufacturing",
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        if cols[i % 2].button(s[:45] + "...", key=f"sug_{i}"):
            st.session_state.prefill = s   # ✅ store suggestion in session state
            st.rerun()                     # ✅ rerun so text area picks it up fresh

    # ── Text area — NO key= parameter ────────────────────
    # ✅ key= removed — this was the root cause of the bug.
    # Without key=, Streamlit respects the value= parameter
    # on every rerun, so session_state.prefill always shows up.
    query = st.text_area(
        "Enter your query:",
        value=st.session_state.prefill,
        height=90,
        placeholder="e.g. Find top suppliers for industrial-grade aluminum sheets for manufacturing",
        label_visibility="collapsed"
    )

    # ✅ always sync whatever is in the box back to session state
    st.session_state.prefill = query
    final_query = query.strip()

    # ── Run button ────────────────────────────────────────
    run_btn = st.button("🚀 Run Multi-Agent Research", disabled=st.session_state.running)

    # ── Validation ────────────────────────────────────────
    if run_btn and not final_query:
        st.warning("⚠️ Please enter a query first.")

    # ── Agent execution ───────────────────────────────────
    if run_btn and final_query:
        st.session_state.running    = True
        st.session_state.report_md  = None
        st.session_state.agent_logs = []

        status   = st.empty()
        progress = st.progress(0)

        try:
            status.markdown('<p class="status-running">⚙️ Initializing agents...</p>', unsafe_allow_html=True)
            progress.progress(10)

            researcher = create_researcher_agent()
            writer     = create_writer_agent()

            status.markdown('<p class="status-running">🔍 Researcher Agent searching the web...</p>', unsafe_allow_html=True)
            progress.progress(30)

            research_task = create_research_task(researcher, final_query)
            writing_task  = create_writing_task(writer)
            writing_task.context = [research_task]

            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writing_task],
                process=Process.sequential,
                verbose=False
            )

            status.markdown('<p class="status-running">✍️ Writer Agent generating report...</p>', unsafe_allow_html=True)
            progress.progress(65)

            result     = crew.kickoff()
            result_str = str(result)

            progress.progress(85)
            status.markdown('<p class="status-running">💾 Saving outputs...</p>', unsafe_allow_html=True)

            os.makedirs("outputs", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            md_path   = f"outputs/report_{timestamp}.md"
            docx_path = f"outputs/report_{timestamp}.docx"

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(result_str)

            export_to_docx(result_str, final_query, docx_path)
            save_memory(final_query, result_str)

            st.session_state.report_md   = result_str
            st.session_state.report_path = md_path
            st.session_state.docx_path   = docx_path
            st.session_state.total_runs += 1
            st.session_state.running     = False
            st.session_state.prefill     = ""  # ✅ clear box after successful run

            progress.progress(100)
            status.markdown('<p class="status-done">✅ Research complete!</p>', unsafe_allow_html=True)

        except Exception as e:
            st.session_state.running = False
            progress.empty()
            st.error(f"❌ Error: {str(e)}")

    # ── Report Display ────────────────────────────────────
    if st.session_state.report_md:
        st.markdown("---")
        st.markdown("### 📄 Generated Procurement Report")

        tab1, tab2 = st.tabs(["📋 Formatted Report", "📝 Raw Markdown"])

        with tab1:
            st.markdown(st.session_state.report_md)

        with tab2:
            st.code(st.session_state.report_md, language="markdown")

        st.markdown("### 💾 Download Report")
        dl1, dl2 = st.columns(2)

        with dl1:
            st.download_button(
                label="⬇️ Download Markdown (.md)",
                data=st.session_state.report_md,
                file_name="procurement_report.md",
                mime="text/markdown"
            )
        with dl2:
            if st.session_state.docx_path and os.path.exists(st.session_state.docx_path):
                with open(st.session_state.docx_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Word (.docx)",
                        data=f.read(),
                        file_name="procurement_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )