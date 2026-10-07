import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui import render_navbar, render_footer, page_header, badge

st.set_page_config(page_title="Recommendations - FarmCare AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

render_navbar(active_page="Recommendations")
page_header("📋 Your Full Farm Report")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
HISTORY_FILE = os.path.join(DATA_DIR, 'check_history.csv')

rep = st.session_state.get("latest_report")
if not rep and os.path.exists(HISTORY_FILE):
    df = pd.read_csv(HISTORY_FILE)
    if not df.empty:
        l = df.iloc[-1]
        rep = {
            "crop": l["crop"], "prediction": l["prediction"], "confidence": l["confidence"],
            "rain": l["rain"], "soil": l["soil"], "duration": l["duration"],
            "timestamp": l["timestamp"],
            "status": "Urgent Attention" if l["confidence"] < 60 else ("Attention Recommended" if l["prediction"] != "Healthy" else "Healthy"),
            "actions": ["Based on history, action plan unavailable."],
            "monitor_signs": "N/A", "expert_help": "N/A"
        }

if rep:
    col1, col2 = st.columns([1, 2])
    with col1:
        if "image_bytes" in rep:
            st.image(rep["image_bytes"], caption="Analyzed Leaf", use_column_width=True)
        else:
            st.info("No image available from history.")
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"Crop: {rep['crop']}")
        st.markdown(f"**Possible Indication:** {rep['prediction']}")
        st.markdown(badge(rep["status"], rep["status"]), unsafe_allow_html=True)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rep['confidence'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#2E7D32"}}
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("### Context Answers")
    st.markdown(f"**Rain:** {rep['rain']} | **Soil:** {rep['soil']} | **Duration:** {rep['duration']}")
    
    st.markdown("### Top 3 Actions")
    for i, action in enumerate(rep.get("actions", [])[:3]):
        st.markdown(f'<div class="card" style="padding:15px; margin-bottom:10px;"><strong>{i+1}.</strong> {action}</div>', unsafe_allow_html=True)

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.markdown("### Past Checks")
        c1, c2 = st.columns([1, 1.5])
        with c1:
            counts = df['prediction'].value_counts().reset_index()
            counts.columns = ['Prediction', 'Count']
            fig2 = px.pie(counts, values='Count', names='Prediction', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            st.dataframe(df.tail(5), use_container_width=True)
else:
    st.info("No report available.")

st.markdown("<br>", unsafe_allow_html=True)
_, bcol, _ = st.columns(3)
with bcol:
    if st.button("Check another crop →", use_container_width=True):
        st.switch_page("pages/2_AI_Crop_Check.py")

render_footer()
