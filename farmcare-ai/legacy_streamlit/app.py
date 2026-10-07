import streamlit as st
from ui import render_navbar, render_footer

st.set_page_config(page_title="FarmCare AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

render_navbar(active_page="Home")

st.markdown("""
<div class="hero-banner">
    <h1 style="font-size: 3rem; margin-bottom: 10px;">Smart decisions. Healthier crops.</h1>
    <p style="font-size: 1.2rem;">Your Context-Aware AI Farm Action Planner.</p>
</div>
""", unsafe_allow_html=True)

col_center = st.columns([1, 1, 1])
with col_center[1]:
    if st.button("📷 Check My Crop", use_container_width=True):
        st.switch_page("pages/2_AI_Crop_Check.py")

st.markdown("<h3 style='text-align: center; margin-top: 40px;'>How it works</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="card" style="text-align:center;">
        <h1 style="font-size:3rem; margin:0;">1️⃣</h1>
        <h3>Upload</h3>
        <p>Take a picture of a leaf.</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="card" style="text-align:center;">
        <h1 style="font-size:3rem; margin:0;">2️⃣</h1>
        <h3>AI Analysis</h3>
        <p>Our model analyzes it.</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="card" style="text-align:center;">
        <h1 style="font-size:3rem; margin:0;">3️⃣</h1>
        <h3>Action Plan</h3>
        <p>Get tailored recommendations.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; margin-top: 40px;'>Why FarmCare AI?</h3>", unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
    st.markdown("""<div class="card">
        <h4>🧠 AI Detection</h4>
        <p>Powered by deep learning for reliable insights.</p>
        <h4>📝 Simple Inputs</h4>
        <p>Just answer 3 quick context questions.</p>
    </div>""", unsafe_allow_html=True)
with col5:
    st.markdown("""<div class="card">
        <h4>✅ Action Plan</h4>
        <p>Clear, actionable next steps for your farm.</p>
        <h4>📊 Health History</h4>
        <p>Track your crop's progress over time.</p>
    </div>""", unsafe_allow_html=True)

render_footer()
