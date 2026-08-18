import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/moderate"

st.set_page_config(
    page_title="Content Moderation",
    page_icon="🛡️",
    layout="wide"
)

# ── Icons (inline SVG — no emoji, works everywhere) ───────────────────────────
ICON_SHIELD = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3l8 4v5c0 5-3.5 9.7-8 11C7.5 21.7 4 17 4 12V7l8-4z"/>
</svg>"""

ICON_PEN = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
</svg>"""

ICON_CLIPBOARD = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
  <rect x="9" y="3" width="6" height="4" rx="1"/>
</svg>"""

ICON_CHECK = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  <polyline points="9 12 11 14 15 10"/>
</svg>"""

ICON_BAN = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
</svg>"""

ICON_ALERT = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
  <line x1="12" y1="9" x2="12" y2="13"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>"""

ICON_SEARCH = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
</svg>"""

ICON_CPU = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <rect x="4" y="4" width="16" height="16" rx="2"/>
  <rect x="9" y="9" width="6" height="6"/>
  <line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/>
  <line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/>
  <line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/>
  <line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>
</svg>"""

ICON_ZAP = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
</svg>"""

ICON_TARGET = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>
</svg>"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
}
.topbar-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.shield-wrap {
    width: 42px;
    height: 42px;
    background: #EEEDFE;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #534AB7;
    flex-shrink: 0;
}
.app-title {
    font-size: 18px;
    font-weight: 600;
    color: #0f111a;
    margin: 0;
    letter-spacing: -0.2px;
}
.app-sub {
    font-size: 12px;
    color: #9ca3af;
    margin: 2px 0 0;
}
.badge-live {
    background: #EAF3DE;
    color: #3B6D11;
    font-size: 11px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 99px;
    border: 0.5px solid #97C459;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.03em;
}
.dot-live {
    width: 6px;
    height: 6px;
    background: #3B6D11;
    border-radius: 50%;
}

/* ── Metric strip ── */
.metric-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 1.75rem;
}
.mcard {
    background: white;
    border: 0.5px solid #e5e7eb;
    border-radius: 13px;
    padding: 1rem 1.2rem 1rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.mcard-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    border-radius: 3px 0 0 3px;
}
.mcard-top {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.mcard-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #9ca3af;
}
.mcard-icon {
    color: #9ca3af;
    display: flex;
    align-items: center;
}
.mcard-value {
    font-size: 23px;
    font-weight: 600;
    color: #0f111a;
    line-height: 1;
    letter-spacing: -0.5px;
}
.mcard-sub {
    font-size: 11px;
    color: #b0b5be;
    margin-top: 4px;
}

/* ── Panels ── */
.panel {
    background: white;
    border: 0.5px solid #e5e7eb;
    border-radius: 13px;
    padding: 1.2rem;
    height: 100%;
}
.panel-hdr {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.panel-icon-wrap {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.panel-title {
    font-size: 13px;
    font-weight: 600;
    color: #0f111a;
}

/* ── Policy rows ── */
.prow {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 9px 10px;
    border-radius: 9px;
    cursor: default;
    transition: background 0.15s;
}
.prow:hover { background: #f8f9fb; }
.prow-icon {
    width: 26px;
    height: 26px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}
.prow-label {
    font-size: 13px;
    font-weight: 500;
    color: #0f111a;
}
.prow-desc {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 2px;
}

/* ── Info grid ── */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin-top: 14px;
}
.info-cell {
    background: #f8f9fb;
    border-radius: 9px;
    padding: 9px 11px;
}
.info-key {
    font-size: 10px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.info-val {
    font-size: 12px;
    font-weight: 600;
    color: #0f111a;
    margin-top: 2px;
}

/* ── Result card ── */
.result-card {
    border: 0.5px solid #e5e7eb;
    border-radius: 13px;
    overflow: hidden;
    margin-top: 1rem;
}
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 1.4rem;
}
.result-icon-box {
    width: 42px;
    height: 42px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.result-status-tag {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.result-headline {
    font-size: 14px;
    font-weight: 600;
    color: #0f111a;
    margin-top: 2px;
}
.result-pill {
    font-size: 12px;
    font-weight: 600;
    padding: 5px 16px;
    border-radius: 99px;
    border: 0.5px solid transparent;
    display: flex;
    align-items: center;
    gap: 6px;
}
.result-body { padding: 1rem 1.4rem 1.4rem; }
.result-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.rm-cell {
    background: #f8f9fb;
    border-radius: 9px;
    padding: 10px 12px;
}
.rm-key { font-size: 11px; color: #9ca3af; }
.rm-val { font-size: 15px; font-weight: 600; color: #0f111a; margin-top: 3px; }
.conf-label-row {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 7px;
}
.conf-label-row span:last-child {
    font-weight: 600;
    color: #0f111a;
}
.prog-bg {
    background: #f0f0f0;
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
}
.prog-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.4s ease;
}

/* ── Error / warning ── */
.err-box {
    background: #fff1f1;
    border: 0.5px solid #fca5a5;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #991b1b;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.warn-box {
    background: #fffbeb;
    border: 0.5px solid #fcd34d;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #92400e;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-left">
        <div class="shield-wrap">{ICON_SHIELD}</div>
        <div>
            <p class="app-title">Content moderation</p>
            <p class="app-sub">DistilBERT · ONNX Runtime · Jigsaw 20K</p>
        </div>
    </div>
    <div class="badge-live">
        <div class="dot-live"></div>
        Live
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric strip ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-strip">
    <div class="mcard">
        <div class="mcard-bar" style="background:#534AB7"></div>
        <div class="mcard-top">
            <div class="mcard-icon" style="color:#534AB7">{ICON_CPU}</div>
            <div class="mcard-label">Model</div>
        </div>
        <div class="mcard-value">DistilBERT</div>
        <div class="mcard-sub">Fine-tuned binary classifier</div>
    </div>
    <div class="mcard">
        <div class="mcard-bar" style="background:#1D9E75"></div>
        <div class="mcard-top">
            <div class="mcard-icon" style="color:#1D9E75">{ICON_TARGET}</div>
            <div class="mcard-label">Accuracy</div>
        </div>
        <div class="mcard-value">96.1%</div>
        <div class="mcard-sub">Validation set · Jigsaw</div>
    </div>
    <div class="mcard">
        <div class="mcard-bar" style="background:#BA7517"></div>
        <div class="mcard-top">
            <div class="mcard-icon" style="color:#BA7517">{ICON_ZAP}</div>
            <div class="mcard-label">ONNX latency</div>
        </div>
        <div class="mcard-value">12.18 ms</div>
        <div class="mcard-sub">Avg. per inference</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown(f"""
    <div class="panel-hdr">
        <div class="panel-icon-wrap" style="background:#EEEDFE;color:#534AB7">{ICON_PEN}</div>
        <span class="panel-title">Input content</span>
    </div>
    """, unsafe_allow_html=True)

    user_text = st.text_area(
        label="content",
        placeholder="Type or paste user-generated content here…",
        height=168,
        label_visibility="collapsed",
        max_chars=2000
    )

    char_count = len(user_text) if user_text else 0
    st.caption(f"{char_count:,} / 2,000 characters · Review threshold < 60% confidence")

    analyze = st.button("Analyze content", use_container_width=True, type="primary")

with right:
    st.markdown(f"""
    <div class="panel">
        <div class="panel-hdr">
            <div class="panel-icon-wrap" style="background:#EAF3DE;color:#3B6D11">{ICON_CLIPBOARD}</div>
            <span class="panel-title">Moderation policy</span>
        </div>
        <div class="prow">
            <div class="prow-icon" style="background:#EAF3DE;color:#3B6D11">{ICON_CHECK}</div>
            <div>
                <div class="prow-label">Safe — allow</div>
                <div class="prow-desc">Passes all checks, publish immediately</div>
            </div>
        </div>
        <div class="prow">
            <div class="prow-icon" style="background:#FCEBEB;color:#A32D2D">{ICON_BAN}</div>
            <div>
                <div class="prow-label">Toxic — block</div>
                <div class="prow-desc">Policy violation, reject and log</div>
            </div>
        </div>
        <div class="prow">
            <div class="prow-icon" style="background:#FAEEDA;color:#854F0B">{ICON_ALERT}</div>
            <div>
                <div class="prow-label">Needs review</div>
                <div class="prow-desc">Confidence &lt; 60%, route to human</div>
            </div>
        </div>
        <div style="border-top:0.5px solid #e5e7eb;margin:12px 0"></div>
        <div class="info-grid">
            <div class="info-cell">
                <div class="info-key">Architecture</div>
                <div class="info-val">DistilBERT</div>
            </div>
            <div class="info-cell">
                <div class="info-key">Runtime</div>
                <div class="info-val">ONNX Runtime</div>
            </div>
            <div class="info-cell">
                <div class="info-key">Training data</div>
                <div class="info-val">Jigsaw 20K</div>
            </div>
            <div class="info-cell">
                <div class="info-key">Endpoint</div>
                <div class="info-val">POST /moderate</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Result ────────────────────────────────────────────────────────────────────
if analyze:
    if not user_text or not user_text.strip():
        st.markdown(
            f"<div class='warn-box'>{ICON_ALERT} Please enter some text before analyzing.</div>",
            unsafe_allow_html=True
        )
    else:
        with st.spinner("Analyzing content…"):
            try:
                response = requests.post(API_URL, json={"text": user_text}, timeout=30)

                if response.status_code == 200:
                    result     = response.json()
                    prediction = result["prediction"]
                    confidence = float(result["confidence"])

                    # ── Determine visual state ──
                    if confidence < 60:
                        headline   = "Needs human review"
                        status_tag = "Review"
                        action     = "Route to human"
                        header_bg  = "#fffbeb"
                        icon_bg    = "#FAEEDA"
                        icon_color = "#854F0B"
                        result_icon = ICON_ALERT
                        tag_color  = "#BA7517"
                        pill_bg    = "#FAEEDA"
                        pill_color = "#633806"
                        pill_bd    = "#EF9F27"
                        bar_color  = "#EF9F27"
                        pill_icon  = ICON_ALERT

                    elif prediction == "toxic":
                        headline   = "Toxic content detected — block this post"
                        status_tag = "Toxic"
                        action     = "Block"
                        header_bg  = "#fff1f1"
                        icon_bg    = "#FCEBEB"
                        icon_color = "#A32D2D"
                        result_icon = ICON_BAN
                        tag_color  = "#dc2626"
                        pill_bg    = "#FCEBEB"
                        pill_color = "#791F1F"
                        pill_bd    = "#F09595"
                        bar_color  = "#E24B4A"
                        pill_icon  = ICON_BAN

                    else:
                        headline   = "Content is safe to publish"
                        status_tag = "Safe"
                        action     = "Allow"
                        header_bg  = "#f0fdf4"
                        icon_bg    = "#EAF3DE"
                        icon_color = "#3B6D11"
                        result_icon = ICON_CHECK
                        tag_color  = "#16a34a"
                        pill_bg    = "#EAF3DE"
                        pill_color = "#27500A"
                        pill_bd    = "#97C459"
                        bar_color  = "#639922"
                        pill_icon  = ICON_CHECK

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header" style="background:{header_bg}">
                            <div style="display:flex;align-items:center;gap:12px">
                                <div class="result-icon-box" style="background:{icon_bg};color:{icon_color}">
                                    {result_icon}
                                </div>
                                <div>
                                    <div class="result-status-tag" style="color:{tag_color}">{status_tag}</div>
                                    <div class="result-headline">{headline}</div>
                                </div>
                            </div>
                            <div class="result-pill"
                                style="background:{pill_bg};color:{pill_color};border-color:{pill_bd}">
                                <span style="color:{icon_color}">{pill_icon}</span>
                                {action}
                            </div>
                        </div>
                        <div class="result-body">
                            <div class="result-meta-grid">
                                <div class="rm-cell">
                                    <div class="rm-key">Prediction</div>
                                    <div class="rm-val">{status_tag}</div>
                                </div>
                                <div class="rm-cell">
                                    <div class="rm-key">Confidence</div>
                                    <div class="rm-val">{confidence:.1f}%</div>
                                </div>
                                <div class="rm-cell">
                                    <div class="rm-key">Action</div>
                                    <div class="rm-val">{action}</div>
                                </div>
                            </div>
                            <div class="conf-label-row">
                                <span>Model confidence</span>
                                <span>{confidence:.2f}%</span>
                            </div>
                            <div class="prog-bg">
                                <div class="prog-fill"
                                    style="width:{min(confidence, 100):.1f}%;background:{bar_color}">
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown(
                        f"<div class='err-box'>{ICON_BAN} API returned an error. Check your FastAPI server.</div>",
                        unsafe_allow_html=True
                    )

            except requests.exceptions.ConnectionError:
                st.markdown(
                    f"<div class='err-box'>{ICON_BAN} Cannot reach the API. "
                    "Start it with: <code>uvicorn app.api:app --reload</code></div>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.markdown(
                    f"<div class='err-box'>{ICON_BAN} Unexpected error: {e}</div>",
                    unsafe_allow_html=True
                )