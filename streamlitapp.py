import streamlit as st
import joblib
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sentinel AI | Content Moderation", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input {
        background-color: #1f2937;
        color: white;
        border-radius: 10px;
        border: 1px solid #3b82f6;
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .safe { background-color: #065f46; color: #a7f3d0; border: 2px solid #10b981; }
    .toxic { background-color: #7f1d1d; color: #fecaca; border: 2px solid #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD MODEL ---
@st.cache_resource
def load_assets():
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    return model, vectorizer

try:
    model, vectorizer = load_assets()
except:
    st.error("❌ Model files not found! Please run 'python model_trainer.py' first.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1067/1067561.png", width=100)
    st.title("Sentinel AI")
    st.markdown("---")
    st.write("🛠️ **Settings**")
    sensitivity = st.slider("Sensitivity Threshold", 0.0, 1.0, 0.5)
    st.info("Higher sensitivity flags more content as toxic.")

# --- MAIN UI ---
st.title("🛡️ Real-Time Content Moderation Dashboard")
st.markdown("Enter text below to analyze for toxicity, hate speech, or offensive language.")

# Layout: Input and Analysis
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Enter content to moderate:", placeholder="Type something here...", height=200)
    analyze_btn = st.button("Analyze Content 🔍", use_container_width=True)

with col2:
    st.markdown("### 📊 Analysis Result")
    if analyze_btn and user_input:
        # Prediction logic
        text_vec = vectorizer.transform([user_input])
        prediction = model.predict(text_vec)[0]
        probability = model.predict_proba(text_vec)[0][1]

        # Design logic for results
        if prediction == 1 or probability > sensitivity:
            st.markdown('<div class="status-card toxic">⚠️ TOXIC CONTENT</div>', unsafe_allow_html=True)
            st.metric(label="Toxicity Score", value=f"{round(probability*100, 2)}%", delta="High Risk", delta_color="inverse")
        else:
            st.markdown('<div class="status-card safe">✅ SAFE CONTENT</div>', unsafe_allow_html=True)
            st.metric(label="Toxicity Score", value=f"{round(probability*100, 2)}%", delta="Low Risk")
        
        # Detailed Breakdown
        st.write("---")
        st.write("**Breakdown:**")
        st.progress(probability)
        st.caption(f"Confidence level: {round(probability*100, 1)}%")
    else:
        st.info("Waiting for input...")

# Footer
st.markdown("---")
st.markdown("<center>Built with Python & Streamlit | Sentinel AI Engine v1.0</center>", unsafe_allow_html=True)