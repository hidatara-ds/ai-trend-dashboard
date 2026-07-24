import os
import streamlit as st
from pathlib import Path

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="AI Social Trend Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS stylesheet
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Initialize Database & Initial Seed Sync
from database.db import DatabaseManager
from services.pipeline import CrawlPipeline

@st.cache_resource
def init_application():
    db = DatabaseManager()
    posts = db.get_posts(limit=10)
    if not posts:
        # Perform initial crawl cycle to seed data
        pipeline = CrawlPipeline(db)
        pipeline.run_crawl_cycle(limit_per_platform=25)
    return db

db = init_application()

# Main entry redirect / page loading notification
st.sidebar.markdown("""
<div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #27272a; margin-bottom: 1rem;">
    <div style="font-weight: 700; font-size: 1rem; color: #fafafa;">AI TREND PULSE</div>
    <div style="font-size: 0.75rem; color: #a1a1aa;">Social Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# Switch to Home page content if run directly
import pages.Home_1 as Home_1
Home_1.render_page()
