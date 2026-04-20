import streamlit as st
from modules.llm_handler   import generate_narrative, generate_image_prompt
from modules.image_handler import generate_image
from modules.vector_db     import store_concept, search_similar, get_all_concepts
import config
import os

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem; border-radius: 12px; margin-bottom: 1.5rem;
    }
    .main-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: white !important; }
    .main-header p  { margin: 0.4rem 0 0 0; opacity: 0.75; font-size: 0.95rem; color: white !important; }

    .stat-card {
        background: #f0f4f8; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem 1.2rem; text-align: center;
    }
    .stat-card .value { font-size: 1.6rem; font-weight: 700; color: #0f3460; }
    .stat-card .label { font-size: 0.78rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }

    .section-title {
        font-size: 0.85rem; font-weight: 700; color: #0f3460;
        text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 0.5rem; padding-bottom: 0.4rem;
        border-bottom: 2px solid #0f3460; display: inline-block;
    }
    .narrative-box {
        background: #f8f9fc; border-left: 4px solid #0f3460;
        border-radius: 0 8px 8px 0; padding: 1.2rem 1.5rem;
        line-height: 1.8; font-size: 0.95rem; color: #2d3748;
    }
    .history-card {
        background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem; margin-bottom: 0.8rem;
    }
    .prompt-tag {
        background: #ebf4ff; color: #0f3460;
        padding: 0.2rem 0.6rem; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Generation Settings")
    max_tokens    = st.slider("Max Tokens", 256, 4096, 1024, 256)
    image_quality = st.radio("Image Quality", ["standard", "hd"], horizontal=True)
    save_image    = st.toggle("Save images locally", value=True)
    show_similar  = st.toggle("Show similar concepts", value=True)
    st.divider()

    st.markdown("### 🤖 Models")
    st.caption("LLM: `gpt-4o-mini`")
    st.caption("Image: `dall-e-3`")
    st.caption("DB: `ChromaDB (local)`")

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏭 Multimodal Manufacturing Creator</h1>
    <p>Transform manufacturing ideas into detailed narratives and high-fidelity visual prototypes</p>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────
all_concepts = get_all_concepts()
c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, len(all_concepts), "Concepts Generated"),
    (c2, "GPT-4o", "Mini LLM"),
    (c3, "DALL·E 3", "Image Model"),
    (c4, max_tokens, "Max Tokens"),
]:
    with col:
        st.markdown(f'<div class="stat-card"><div class="value">{val}</div><div class="label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────
tab1, tab2 = st.tabs(["✨ Generate Concept", "🖼️ History Gallery"])

# ════════════════════════════════════════════════════════════
# TAB 1 — Generate
# ════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-title">Describe Your Concept</p>', unsafe_allow_html=True)

    user_prompt = st.text_area(
        label="prompt",
        placeholder="e.g. A lightweight titanium drone frame using selective laser sintering (SLS) for aerospace applications...",
        height=130,
        label_visibility="collapsed"
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        generate_btn = st.button("🚀 Generate", type="primary", use_container_width=True)

    if user_prompt and show_similar:
        similar = search_similar(user_prompt, n_results=2)
        if similar:
            with st.expander(f"🔍 {len(similar)} Similar Concept(s) Found"):
                for s in similar:
                    st.markdown(f'<span class="prompt-tag">Past</span> **{s["metadata"]["user_prompt"]}**', unsafe_allow_html=True)
                    st.caption(s["narrative"][:250] + "...")
                    st.divider()

    if generate_btn:
        if not user_prompt.strip():
            st.warning("⚠️ Please enter a manufacturing concept first.")
        else:
            narrative    = None
            image_result = None
            concept_id   = None

            progress = st.progress(0, text="Starting generation...")

            progress.progress(15, text="📄 Generating narrative with GPT-4o-mini...")
            try:
                from openai import OpenAI
                client = OpenAI(api_key=config.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=config.LLM_MODEL,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "system", "content": "You are an expert manufacturing engineer and technical writer. Generate detailed, professional manufacturing concept descriptions with processes, materials, use cases, and engineering challenges."},
                        {"role": "user",   "content": f"Generate a detailed manufacturing concept description for: {user_prompt}"}
                    ]
                )
                narrative = response.choices[0].message.content
                progress.progress(45, text="✅ Narrative complete! Optimizing image prompt...")
            except Exception as e:
                st.error(f"Narrative generation failed: {e}")
                st.stop()

            try:
                img_prompt_resp = client.chat.completions.create(
                    model=config.LLM_MODEL,
                    max_tokens=200,
                    messages=[
                        {"role": "system", "content": "Write concise, vivid DALL·E image prompts focused on visual details."},
                        {"role": "user",   "content": f"Write a DALL·E prompt (max 150 words) for: '{user_prompt}'\nContext: {narrative[:400]}\nFocus on photorealistic appearance, materials, factory/lab setting."}
                    ]
                )
                image_prompt = img_prompt_resp.choices[0].message.content
                progress.progress(60, text="🎨 Generating image with DALL·E 3...")
            except Exception as e:
                st.error(f"Image prompt generation failed: {e}")
                st.stop()

            try:
                image_result = generate_image(image_prompt, save_locally=save_image)
                progress.progress(85, text="💾 Saving to knowledge base...")
            except Exception as e:
                st.error(f"Image generation failed: {e}")
                st.stop()

            try:
                concept_id = store_concept(user_prompt=user_prompt, narrative=narrative, image_path=image_result.get("local_path"))
                progress.progress(100, text="✅ Done!")
            except Exception as e:
                st.warning(f"Could not save to knowledge base: {e}")
                progress.progress(100, text="✅ Done!")

            st.success(f"✅ Concept generated! `ID: {concept_id}`")
            st.markdown("<br>", unsafe_allow_html=True)

            left, right = st.columns(2, gap="large")

            with left:
                st.markdown('<p class="section-title">Generated Narrative</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="narrative-box">{narrative}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button("⬇️ Download Narrative (.txt)", data=narrative,
                                   file_name=f"concept_{concept_id}.txt", mime="text/plain", use_container_width=True)

            with right:
                st.markdown('<p class="section-title">Visual Prototype</p>', unsafe_allow_html=True)
                st.image(image_result["url"], width="stretch")
                import requests as req
                img_bytes = req.get(image_result["url"]).content
                st.download_button("⬇️ Download Image (.png)", data=img_bytes,
                                   file_name=f"concept_{concept_id}.png", mime="image/png", use_container_width=True)
                with st.expander("🔍 View DALL·E prompt used"):
                    st.caption(image_result.get("revised_prompt", image_prompt))

# ════════════════════════════════════════════════════════════
# TAB 2 — History Gallery
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">Past Concepts</p>', unsafe_allow_html=True)

    if not all_concepts:
        st.info("No concepts yet. Go to **Generate Concept** tab to create your first one!")
    else:
        st.caption(f"{len(all_concepts)} concept(s) in your local knowledge base.")
        st.markdown("<br>", unsafe_allow_html=True)
        for concept in reversed(all_concepts):
            meta = concept["metadata"]
            st.markdown(f"""
            <div class="history-card">
                <span class="prompt-tag">Concept</span>&nbsp;
                <strong>{meta.get("user_prompt", "Unknown")}</strong>
                <br><small style="color:#718096">🕒 {meta.get("created_at", "")[:19].replace("T", " ")}</small>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("View Full Narrative"):
                st.markdown(concept["narrative"])
            img_path = meta.get("image_path", "")
            if img_path and os.path.exists(img_path):
                with st.expander("View Saved Image"):
                    st.image(img_path, width="stretch")
                    with open(img_path, "rb") as f:
                        st.download_button("⬇️ Download Image", data=f,
                                           file_name=os.path.basename(img_path),
                                           mime="image/png", key=f"dl_{concept['id']}")
            st.markdown("---")

# ── Footer ────────────────────────────────────────────────
st.markdown('<div style="text-align:center;opacity:0.4;font-size:0.8rem;margin-top:2rem;">Built with GPT-4o-mini · DALL·E 3 · ChromaDB · Streamlit</div>', unsafe_allow_html=True)                                                                                                                                                                                  