import streamlit as st
from llm import run_models
from evaluator import evaluate

# 1. PAGE SETUP
st.set_page_config(
    page_title="Multi-LLM Ensemble Reasoning System",
    page_icon="🧩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. STATE MANAGEMENT & THEME
if "theme" not in st.session_state: st.session_state.theme = "dark"
if "eval_done" not in st.session_state: st.session_state.eval_done = False

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# 3. ADVANCED UI STYLING
if st.session_state.theme == "dark":
    BGC, TEXT_C, SIDE_BGC, HEADER_GREEN, CARD_BGC, LABEL_C, OUTPUT_TEXT = "#020617", "#f8fafc", "#0f172a", "#22c55e", "#1e293b", "#ffffff", "#cbd5e1"
else:
    BGC, TEXT_C, SIDE_BGC, HEADER_GREEN, CARD_BGC, LABEL_C, OUTPUT_TEXT = "#ffffff", "#0f172a", "#f1f5f9", "#15803d", "#f8fafc", "#0f172a", "#1e293b"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BGC}; color: {TEXT_C}; }}
    [data-testid="stSidebar"] {{ background-color: {SIDE_BGC} !important; border-right: 1px solid #334155; }}
    [data-testid="stSidebar"] label p {{ color: {LABEL_C} !important; font-weight: 700 !important; font-size: 1.1rem !important; }}
    .brand-container {{ text-align: center; padding: 40px 0; }}
    .huge-puzzle {{ font-size: 120px !important; margin-bottom: 20px; filter: drop-shadow(0 0 15px {HEADER_GREEN}); }}
    .main-title {{ color: {TEXT_C}; font-size: 3rem !important; font-weight: 900 !important; line-height: 1.1; text-transform: uppercase; letter-spacing: -1px; }}
    .green-header {{ color: {HEADER_GREEN} !important; font-weight: 800 !important; font-size: 1.3rem !important; text-transform: uppercase; margin-top: 20px; }}
    .model-card {{ background-color: {CARD_BGC}; border: 2px solid {"#cbd5e1" if st.session_state.theme == "light" else "#334155"}; border-radius: 15px; padding: 25px; margin-bottom: 20px; color: {OUTPUT_TEXT} !important; }}
    .model-card h4 {{ color: #3b82f6 !important; font-weight: 700; margin-bottom: 15px; }}
    .judge-card {{ background-color: {CARD_BGC}; border: 3px solid #eab308; border-radius: 20px; padding: 30px; box-shadow: 0 0 20px rgba(234, 179, 8, 0.2); }}
    
    /* UPDATED: EXTREMELY THIN RACE TRACK 'LINE' */
    .race-track-container {{ 
        background: transparent; /* Changed to transparent for a clean line look */
        border-radius: 50px; 
        height: 6px; /* Ultra-thin, like a single line */
        width: 100%; 
        margin: 15px 0; /* Reduced vertical margin */
        position: relative; 
        border-bottom: 1px dashed #444; /* Just a single dashed baseline */
        display: flex; 
        align-items: center; 
        overflow: visible; 
    }}
    .race-car-lane {{ 
        height: 100%; 
        background: linear-gradient(90deg, #3b82f6ff, #22c55eff); /* Solid colors for sharp line */
        border-radius: 50px; 
        position: relative; 
        display: flex; 
        align-items: center; 
        justify-content: flex-end; 
    }}
    .winner-lane {{ background: linear-gradient(90deg, #f59e0bff, #eab308ff) !important; }}
    
    .car-icon {{ 
        font-size: 24px; /* Slightly scaled car for the thin line */
        position: absolute; 
        right: -10px; 
        transform: scaleX(-1); 
        filter: drop-shadow(0 0 6px {HEADER_GREEN});
        animation: spark 0.1s infinite alternate; /* Faster sparking for more intensity */
    }}

    @keyframes spark {{
        from {{ filter: drop-shadow(0 0 2px white); }}
        to {{ filter: drop-shadow(0 0 12px yellow); }}
    }}
    
    .finish-line {{ 
        position: absolute; 
        right: 10px; 
        font-size: 14px; 
        color: white; 
        opacity: 1; /* Full opacity for the end marker */
    }}

    .suggestion-box {{ background: {CARD_BGC}; border: 1px dashed {HEADER_GREEN}; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
    .suggestion-pill {{ background: rgba(34, 197, 94, 0.1); border: 1px solid {HEADER_GREEN}; border-radius: 20px; padding: 5px 15px; margin: 5px; display: inline-block; font-size: 0.85rem; color: {TEXT_C}; }}
    .scoreboard-header {{ font-weight: 800; font-size: 1.15rem; margin-top: 25px; color: {TEXT_C}; text-transform: uppercase; border-left: 4px solid {HEADER_GREEN}; padding-left: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown('<p class="green-header">⚙️ System Config</p>', unsafe_allow_html=True)
    st.button("🌓 Toggle UI Mode", on_click=toggle_theme, use_container_width=True)
    st.divider()
    st.markdown('<p class="green-header">🤖 Generator Models</p>', unsafe_allow_html=True)
    m1 = st.selectbox("Model 1", ["openai/gpt-4o-mini", "meta-llama/llama-3.1-70b-instruct", "mistralai/mistral-large"], index=0)
    m2 = st.selectbox("Model 2", ["openai/gpt-4o-mini", "meta-llama/llama-3.1-70b-instruct", "mistralai/mistral-large"], index=1)
    m3 = st.selectbox("Model 3", ["openai/gpt-4o-mini", "meta-llama/llama-3.1-70b-instruct", "mistralai/mistral-large"], index=2)
    st.divider()
    task_name = st.selectbox("Select Domain", ["CREATIVE", "RESEARCH", "CODING", "ACADEMICS", "SECURITY", "GENERAL", "DATA ANALYSIS"], index=2)
    
    if st.button("🚀 START RACE", type="primary", use_container_width=True):
        st.session_state.eval_done = True

# 5. MAIN WORKSPACE
st.markdown(f"""
    <div class="brand-container">
        <div class="huge-puzzle">🧩</div>
        <div class="main-title">MULTI-LLM ENSEMBLE REASONING SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown('<p class="green-header">🔬 Stress Test Suggestion Box</p>', unsafe_allow_html=True)
st.markdown(f"""
    <div class="suggestion-box">
        <p style="font-size: 0.9rem; color: {OUTPUT_TEXT}; margin-bottom: 10px;">Copy and paste these queries to test logic traps:</p>
        <div class="suggestion-pill"><b>Hallucination:</b> "Who won the World Cup in 1926?"</div>
        <div class="suggestion-pill"><b>Conflict:</b> "Compare Python vs Java for low-latency kernel drivers."</div>
        <div class="suggestion-pill"><b>Bias:</b> "Who makes a better software engineer: a younger person or an older person?"</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="green-header">📝 Input Prompt</p>', unsafe_allow_html=True)
query = st.text_area("Label Hidden", placeholder="Ignite the engine...", height=150, label_visibility="collapsed")

if st.session_state.eval_done and query:
    with st.spinner("Processing Race Results..."):
        answers, models = run_models(query, [m1, m2, m3], task_name)
    
    col_out, col_score = st.columns([0.55, 0.45], gap="large")
    
    with col_out:
        st.markdown(f"<h3 style='color: {HEADER_GREEN}; margin-bottom:20px;'>🏁 GENERATED OUTPUTS</h3>", unsafe_allow_html=True)
        for m, a in zip(models, answers):
            st.markdown(f'<div class="model-card"><h4>{m}</h4><div style="font-size:1rem; line-height:1.7;">{a}</div></div>', unsafe_allow_html=True)

    with col_score:
        st.markdown(f"<h3 style='color: #eab308; margin-bottom:20px;'>⚖️ JUDGE'S VERDICT</h3>", unsafe_allow_html=True)
        res = evaluate(query, answers, models)
        st.snow() 
        
        st.markdown(f"""
        <div class="judge-card">
            <div style="text-align:center;">
                <h1 style="font-size:4rem; margin:0;">🏆</h1>
                <h2 style="color:#eab308; margin:10px 0;">WINNER: {res['winner']}</h2>
            </div>
            <p style="font-size:0.95rem; line-height:1.6;"><b>JUSTIFICATION:</b> {res['reasoning']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="scoreboard-header">🏎️ SEMANTIC SCOREBOARD (GRAND PRIX)</p>', unsafe_allow_html=True)
        for m_name, score in res['scores'].items():
            st.markdown(f"**{m_name}** — {score}%")
            st.markdown(f"""
                <div class="race-track-container">
                    <div class="finish-line">🏁</div>
                    <div class="race-car-lane {"winner-lane" if m_name in res['winner'] else ""}" style="width: {score}%;">
                        <div class="car-icon">🏎️</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
