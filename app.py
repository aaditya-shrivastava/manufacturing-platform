import streamlit as st

st.set_page_config(
    page_title="Manufacturing AI Platform",
    page_icon="🏭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Ports — change these to match your Docker/K8s service URLs ──
MULTIMODAL_URL  = "http://13.202.61.65:8080/manufacturing-creator/"
MULTIAGENT_URL  = "http://13.202.61.65:8080/multi-agent-manufacturing/"  

st.markdown("""
<style>
    html, body, [class*="css"] { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] { display: none; }

    .badge {
        display: inline-block;
        background: #1a1d27;
        border: 0.5px solid #2a2d3a;
        border-radius: 20px;
        color: #888;
        font-size: 0.75rem;
        padding: 4px 14px;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin: 0 0 0.4rem 0;
    }
    .main-sub {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .tool-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 14px;
        padding: 1.8rem 1.6rem;
        text-align: left;
        transition: border-color 0.2s;
    }
    .tool-card:hover { border-color: #00d4ff; }
    .tool-card .icon {
        font-size: 1.8rem;
        margin-bottom: 0.8rem;
    }
    .tool-card h3 {
        color: #e8e8e8;
        font-size: 1.1rem;
        margin: 0 0 0.5rem 0;
    }
    .tool-card p {
        color: #666;
        font-size: 0.85rem;
        line-height: 1.6;
        margin: 0 0 1rem 0;
    }
    .tool-card .tags span {
        display: inline-block;
        background: #12161f;
        border: 0.5px solid #2a2d3a;
        color: #555;
        font-size: 0.72rem;
        padding: 2px 10px;
        border-radius: 20px;
        margin-right: 4px;
    }
    .footer {
        text-align: center;
        color: #333;
        font-size: 0.75rem;
        margin-top: 3rem;
    }
    div[data-testid="stLinkButton"] a {
        background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.4rem !important;
        font-size: 0.9rem !important;
        text-decoration: none !important;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div style="text-align:center"><span class="badge"> Datagami &nbsp;·&nbsp; Group 12D1</span></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🏭 Manufacturing AI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Select a tool to get started</div>', unsafe_allow_html=True)


# ── Tool Cards ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">🖼️</div>
        <h3>Multimodal Creator</h3>
        <p>Enter a manufacturing concept and get a detailed technical narrative along with a photorealistic visual prototype.</p>
        <div class="tags">
            <span>GPT-4o-mini</span>
            <span>DALL·E 3</span>
            <span>ChromaDB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Open Multimodal Creator →", MULTIMODAL_URL, use_container_width=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="icon">🔍</div>
        <h3>Multi-Agent Research</h3>
        <p>test Describe your manufacturing needs and AI agents will research suppliers, pricing, and generate a full procurement report.</p>
        <div class="tags">
            <span>CrewAI</span>
            <span>Llama 3.3</span>
            <span>DuckDuckGo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("Open Multi-Agent Research →", MULTIAGENT_URL, use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Powered by GPT-4o · DALL·E 3 · CrewAI · Llama 3.3 · Streamlit
</div>
""", unsafe_allow_html=True)


