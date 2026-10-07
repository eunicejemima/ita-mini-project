import streamlit as st
import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui import render_navbar, render_footer, page_header

st.set_page_config(page_title="Crop Guide - FarmCare AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

render_navbar(active_page="Crop Guide")
page_header("📚 Crop Guide", "Learn about common diseases, growth stages, and monitoring tips.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, 'engine', 'knowledge_base.json')

knowledge_base = {}
if os.path.exists(KNOWLEDGE_BASE_PATH):
    with open(KNOWLEDGE_BASE_PATH, 'r') as f:
        knowledge_base = json.load(f)

tabs = st.tabs(["Tomato", "Potato", "Maize"])

for i, crop in enumerate(["Tomato", "Potato", "Maize"]):
    with tabs[i]:
        crop_data = knowledge_base.get(crop, {})
        st.markdown(f'<div class="card" style="text-align:center;"><h3>{crop}</h3><p>🌱 Seedling → 🌿 Vegetative → 🌼 Flowering → 🍅 Maturation</p></div>', unsafe_allow_html=True)
        
        for disease, details in crop_data.items():
            st.markdown(f'<div class="card"><h4>{disease}</h4><p><strong>Description:</strong> {details.get("description", "")}</p><p><strong>Stages:</strong> {details.get("growth_stages", "")}</p><p><strong>Monitor:</strong> {details.get("monitor_signs", "")}</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
_, bcol, _ = st.columns(3)
with bcol:
    if st.button("Check My Crop →", use_container_width=True):
        st.switch_page("pages/2_AI_Crop_Check.py")

render_footer()
