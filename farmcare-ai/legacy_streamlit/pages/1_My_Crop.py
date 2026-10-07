import streamlit as st
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui import render_navbar, render_footer, page_header

st.set_page_config(page_title="My Crop - FarmCare AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

render_navbar(active_page="My Crop")
page_header("🌱 My Crop", "Save your current crop details for personalized tracking.")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
MY_CROP_FILE = os.path.join(DATA_DIR, 'my_crop.json')

existing_data = {"crop": "Tomato", "age": 30, "recent_rain": "Today", "soil": "Normal"}
if os.path.exists(MY_CROP_FILE):
    with open(MY_CROP_FILE, 'r') as f:
        try:
            existing_data = json.load(f)
        except:
            pass

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("my_crop_form"):
        crop = st.selectbox("Select Crop", ["Tomato", "Potato", "Maize"], index=["Tomato", "Potato", "Maize"].index(existing_data.get("crop", "Tomato")))
        age = st.number_input("Crop Age (in days)", min_value=1, max_value=365, value=existing_data.get("age", 30))
        recent_rain = st.selectbox("Recent Rain", ["Today", "1–3 days ago", "4–7 days ago", "More than 7 days ago"], index=["Today", "1–3 days ago", "4–7 days ago", "More than 7 days ago"].index(existing_data.get("recent_rain", "Today")))
        soil = st.selectbox("Soil Condition", ["Wet", "Normal", "Dry"], index=["Wet", "Normal", "Dry"].index(existing_data.get("soil", "Normal")))
        
        submitted = st.form_submit_button("Save Crop Details", use_container_width=True)
        if submitted:
            new_data = {
                "crop": crop,
                "age": age,
                "recent_rain": recent_rain,
                "soil": soil
            }
            with open(MY_CROP_FILE, 'w') as f:
                json.dump(new_data, f)
            st.success("Crop details saved successfully!")
            existing_data = new_data
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="card" style="background-color: #E8F5E9; border-left: 5px solid #2E7D32;">
        <h3>Your saved crop</h3>
        <p><strong>Crop:</strong> {}</p>
        <p><strong>Age:</strong> {} days</p>
        <p><strong>Recent Rain:</strong> {}</p>
        <p><strong>Soil Condition:</strong> {}</p>
    </div>""".format(existing_data.get("crop"), existing_data.get("age"), existing_data.get("recent_rain"), existing_data.get("soil")), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Check my crop with AI →", use_container_width=True):
        st.switch_page("pages/2_AI_Crop_Check.py")

render_footer()
