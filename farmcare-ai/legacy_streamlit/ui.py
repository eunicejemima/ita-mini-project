import streamlit as st
import os

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_navbar(active_page="Home"):
    load_css()
    # Navbar columns
    col_logo, col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1.2, 1.5, 1])
    with col_logo:
        st.markdown("<h3 style='margin:0; padding-top:5px;'>🌿 FarmCare AI</h3>", unsafe_allow_html=True)
    with col1:
        st.page_link("app.py", label="Home", icon="🏠" if active_page=="Home" else None)
    with col2:
        st.page_link("pages/1_My_Crop.py", label="My Crop", icon="🌱" if active_page=="My Crop" else None)
    with col3:
        st.page_link("pages/2_AI_Crop_Check.py", label="AI Crop Check", icon="🔍" if active_page=="AI Crop Check" else None)
    with col4:
        st.page_link("pages/3_Recommendations.py", label="Recommendations", icon="📋" if active_page=="Recommendations" else None)
    with col5:
        st.page_link("pages/4_Crop_Guide.py", label="Crop Guide", icon="📚" if active_page=="Crop Guide" else None)
    st.markdown("---")

def render_footer():
    st.markdown("""
        <div style="text-align: center; color: #757575; font-size: 0.85em; padding: 30px 0; margin-top: 50px; border-top: 1px solid #E0E0E0;">
            FarmCare AI gives possible indications for guidance only. Consult a local agricultural expert for confirmation.<br>
            <strong>FarmCare AI - ITA Project</strong>
        </div>
    """, unsafe_allow_html=True)

def page_header(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.markdown(f"**{subtitle}**")

def card(content, css_class="card"):
    st.markdown(f'<div class="{css_class}">{content}</div>', unsafe_allow_html=True)

def badge(text, status="Healthy"):
    status_map = {
        "Healthy": "badge-healthy",
        "Attention Recommended": "badge-attention",
        "Urgent Attention": "badge-urgent"
    }
    css_class = status_map.get(status, "badge-healthy")
    return f'<span class="badge {css_class}">{text}</span>'
