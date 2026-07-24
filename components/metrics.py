import streamlit as st
from components.icons import get_icon_html

def render_metric_card(title: str, value: str, subtext: str = "", icon_name: str = "activity", accent_color: str = "#10b981"):
    icon_html = get_icon_html(icon_name, accent_color)
    html = f"""
    <div class="metric-card">
        <div class="metric-title">{icon_html} <span>{title}</span></div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub" style="color: {accent_color};">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
