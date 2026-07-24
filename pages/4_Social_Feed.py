import streamlit as st
from database.db import DatabaseManager
from components.header import render_header
from components.feed_card import render_feed_card

def render_page():
    db = DatabaseManager()
    render_header(
        title="Social Feed",
        subtitle="Live multi-platform stream of AI discussions with explainable virality scoring"
    )

    # Filter & Sort controls
    c_plat, c_sort, c_search = st.columns([3, 3, 4])
    with c_plat:
        selected_platform = st.selectbox(
            "Platform Filter:",
            ["all", "x", "threads", "tiktok", "instagram", "facebook"],
            format_func=lambda x: "All Platforms" if x == "all" else x.upper()
        )
    with c_sort:
        sort_by = st.selectbox(
            "Sort Posts By:",
            ["trend_score", "virality_score", "engagement_score", "created_at"],
            format_func=lambda x: x.replace("_", " ").title()
        )
    with c_search:
        search_query = st.text_input("Search post content or author...", "", placeholder="e.g. deepseek, sonnet, karpathy")

    posts = db.get_posts(
        platform=selected_platform,
        limit=100,
        search_query=search_query.strip() if search_query.strip() else None,
        sort_by=sort_by
    )

    st.markdown(f"<div class='section-title'>Showing {len(posts)} Collected Posts</div>", unsafe_allow_html=True)

    if not posts:
        st.info("No posts match your selected filter criteria.")
        return

    # Render in 2 column grid
    col1, col2 = st.columns(2)
    for idx, post in enumerate(posts):
        with (col1 if idx % 2 == 0 else col2):
            render_feed_card(post)

if __name__ == "__main__" or "app" in __name__:
    render_page()
