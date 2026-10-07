import streamlit as st
import os
import pandas as pd
from datetime import datetime
import json
import sys
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.predict import predict_image
from engine.context_engine import generate_action_plan
from ui import render_navbar, render_footer, badge

st.set_page_config(page_title="AI Crop Check - FarmCare AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

render_navbar(active_page="AI Crop Check")

st.markdown("<span style='background-color:#E3F2FD; color:#1565C0; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:0.8rem;'>DEMO MODE Active</span>", unsafe_allow_html=True)
st.title("🔍 AI Crop Check")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
MY_CROP_FILE = os.path.join(DATA_DIR, 'my_crop.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'check_history.csv')

saved_crop = "Tomato"
saved_rain = "Today"
saved_soil = "Normal"
if os.path.exists(MY_CROP_FILE):
    with open(MY_CROP_FILE, 'r') as f:
        try:
            d = json.load(f)
            saved_crop = d.get("crop", "Tomato")
            saved_rain = d.get("recent_rain", "Today")
            saved_soil = d.get("soil", "Normal")
        except: pass

st.markdown("""
<div class="step-indicator">
    <span class="step-active">① Select Crop</span> → <span>② Upload</span> → <span>③ Questions</span> → <span>④ Results</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
crop_options = ["Tomato", "Potato", "Maize", "Rice (Coming Soon)"]
crop_choice = st.radio("Step 1: Choose a crop", crop_options, index=crop_options.index(saved_crop) if saved_crop in crop_options else 0, horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### Step 2: Upload Image")
col_up, col_prev = st.columns([1, 1])
with col_up:
    uploaded_file = st.file_uploader("Upload Leaf Image (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
with col_prev:
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview", width=200)
    else:
        st.info("Upload an image to see preview.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### Step 3: Context Questions")
q1, q2, q3 = st.columns(3)
with q1:
    st.markdown("**🌧️ Has it rained recently?**")
    rain_opts = ["Today", "1–3 days ago", "4–7 days ago", "More than 7 days ago"]
    rain = st.radio("Rain", rain_opts, index=rain_opts.index(saved_rain) if saved_rain in rain_opts else 0, label_visibility="collapsed")
with q2:
    st.markdown("**💧 How does the soil look?**")
    soil_opts = ["Wet", "Normal", "Dry"]
    soil = st.radio("Soil", soil_opts, index=soil_opts.index(saved_soil) if saved_soil in soil_opts else 1, label_visibility="collapsed")
with q3:
    st.markdown("**📅 How long have you noticed the problem?**")
    duration = st.radio("Duration", ["Today", "A few days", "More than a week"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

def save_to_history(crop, prediction, confidence, rain, soil, duration):
    file_exists = os.path.exists(HISTORY_FILE)
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "crop": crop,
        "prediction": prediction,
        "confidence": confidence,
        "rain": rain,
        "soil": soil,
        "duration": duration
    }
    df = pd.DataFrame([data])
    df.to_csv(HISTORY_FILE, mode='a', header=not file_exists, index=False)

if st.button("Analyze My Crop", use_container_width=True):
    if "Rice" in crop_choice:
        st.warning("Rice analysis is coming soon! Please select another crop.")
    elif uploaded_file is None:
        st.error("Please upload a leaf image to proceed.")
    else:
        with st.spinner("Analyzing image and generating action plan..."):
            img_bytes = uploaded_file.read()
            prediction, confidence = predict_image(img_bytes, crop_choice)
            plan = generate_action_plan(crop_choice, prediction, confidence, rain, soil, duration)
            save_to_history(crop_choice, prediction, confidence, rain, soil, duration)
            
            st.session_state["latest_report"] = {
                "crop": crop_choice,
                "prediction": prediction,
                "confidence": confidence,
                "status": plan["status_level"],
                "actions": plan["actions"],
                "monitor_signs": plan["monitor_signs"],
                "expert_help": plan["expert_help"],
                "rain": rain,
                "soil": soil,
                "duration": duration,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "image_bytes": img_bytes
            }
            
            st.success("Analysis complete!")
            
if "latest_report" in st.session_state:
    st.markdown("### Step 4: Results")
    rep = st.session_state["latest_report"]
    
    if rep["confidence"] < 60:
        st.warning("⚠️ Unclear result. The AI is not confident. Please upload a clearer, well-lit photo of a single leaf.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    rcol1, rcol2 = st.columns([1, 1])
    with rcol1:
        st.subheader(f"Crop: {rep['crop']}")
        st.markdown(f"**Possible Indication:** {rep['prediction']}")
        st.markdown(f"**Confidence:** {rep['confidence']}%")
        st.markdown(badge(rep["status"], rep["status"]), unsafe_allow_html=True)
    with rcol2:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rep['confidence'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "AI Confidence"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#2E7D32"}}
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    acol1, acol2 = st.columns([1.5, 1])
    with acol1:
        st.markdown("### What should you do next?")
        for i, action in enumerate(rep["actions"]):
            st.markdown(f'<div class="card" style="padding:15px; margin-bottom:10px;"><strong>0{i+1}.</strong> {action}</div>', unsafe_allow_html=True)
    with acol2:
        st.markdown("### Monitor these signs")
        st.markdown(f'<div class="card" style="padding:15px;"><ul><li>{rep["monitor_signs"]}</li></ul></div>', unsafe_allow_html=True)
        st.markdown("### Need expert help?")
        st.markdown(f'<div class="card" style="padding:15px; border:2px solid #F9A825;">🧑‍🌾 {rep["expert_help"]}</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("View Full Farm Report →", use_container_width=True):
            st.switch_page("pages/3_Recommendations.py")
    with b2:
        if st.button("Check Another Leaf", use_container_width=True):
            del st.session_state["latest_report"]
            st.rerun()

render_footer()
