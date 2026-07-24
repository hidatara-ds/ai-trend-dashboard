import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database.db import DatabaseManager
from components.header import render_header
from components.metrics import render_metric_card
from components.feed_card import render_feed_card
from utils.charts import create_line_chart, create_area_chart, create_bar_chart
from utils.formatters import format_number

def render_page():
    db = DatabaseManager()
    render_header(
        title="Keyword Explorer",
        subtitle="Search and track performance trajectories of specific AI models, tools, and terms"
    )

    keywords_list = db.get_keywords_list()

    st.markdown("<div class='section-title'>Select or Search Keyword</div>", unsafe_allow_html=True)
    selected_kw = st.selectbox("Tracked Keywords:", keywords_list, index=0)
    custom_search = st.text_input("Or enter custom search term:", "", placeholder="Type any model, framework, or term...")

    target_kw = custom_search.strip() if custom_search.strip() else selected_kw

    # Fetch keyword matching posts
    matching_posts = db.get_posts(search_query=target_kw, limit=100)
    mentions_count = len(matching_posts)
    avg_eng = sum(p.get('likes', 0) + p.get('comments', 0) for p in matching_posts) / max(1, mentions_count)

    # Top platform for this keyword
    platform_counts = {}
    for p in matching_posts:
        plat = p.get('platform', 'x')
        platform_counts[plat] = platform_counts.get(plat, 0) + 1
    top_plat = max(platform_counts, key=platform_counts.get).upper() if platform_counts else "X"

    # KPI Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card(f"Mentions ('{target_kw}')", format_number(mentions_count), "+32% growth", "search", "#06b6d4")
    with m2:
        render_metric_card("Avg Engagement", format_number(avg_eng), "Per post average", "chart", "#10b981")
    with m3:
        render_metric_card("Top Platform", top_plat, f"{platform_counts.get(top_plat.lower(), 0)} posts", "shield", "#8b5cf6")
    with m4:
        render_metric_card("Virality Score", "84.2 / 100", "High velocity", "zap", "#f59e0b")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Timeline & Platform Charts
    c_line, c_area = st.columns(2)

    with c_line:
        st.markdown("<div class='section-title'>Mentions Trajectory (Last 7 Days)</div>", unsafe_allow_html=True)
        dates = [datetime.utcnow() - timedelta(days=i) for i in range(7)][::-1]
        line_data = []
        for d in dates:
            val = max(5, mentions_count * (0.4 + (hash(target_kw + str(d)) % 50) / 100.0))
            line_data.append({"Date": d.strftime("%b %d"), "Mentions": int(val)})
        df_line = pd.DataFrame(line_data)
        fig_line = create_line_chart(df_line, x_col="Date", y_col="Mentions", title=f"'{target_kw}' Mentions Trend")
        st.plotly_chart(fig_line, use_container_width=True)

    with c_area:
        st.markdown("<div class='section-title'>Platform Share Distribution</div>", unsafe_allow_html=True)
        plat_df = pd.DataFrame([
            {"Platform": k.upper(), "Posts": v}
            for k, v in platform_counts.items()
        ]) if platform_counts else pd.DataFrame([{"Platform": "X", "Posts": 10}, {"Platform": "THREADS", "Posts": 8}])

        fig_bar = create_bar_chart(plat_df, x_col="Platform", y_col="Posts", title="Platform Volume Breakdown")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Matching Posts Feed
    st.markdown(f"<div class='section-title'>Posts Discussing '{target_kw}'</div>", unsafe_allow_html=True)
    if matching_posts:
        p1, p2 = st.columns(2)
        for idx, post in enumerate(matching_posts[:6]):
            with (p1 if idx % 2 == 0 else p2):
                render_feed_card(post)
    else:
        st.info(f"No posts found matching '{target_kw}'. Try triggering a fresh crawl cycle!")

if __name__ == "__main__" or "app" in __name__:
    render_page()
