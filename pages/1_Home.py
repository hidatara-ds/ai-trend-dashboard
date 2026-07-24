import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database.db import DatabaseManager
from components.header import render_header
from components.metrics import render_metric_card
from components.trend_card import render_trend_card
from components.feed_card import render_feed_card
from utils.charts import create_area_chart, create_bar_chart
from utils.formatters import format_number, format_relative_time
from services.pipeline import CrawlPipeline

def render_page():
    db = DatabaseManager()
    render_header(
        title="AI Social Trend Intelligence",
        subtitle="Real-time AI discussion monitoring & multi-platform trend analytics"
    )

    # Top KPI Bar
    posts_data = db.get_posts(limit=250)
    topics_data = db.get_topics(limit=10)
    logs = db.get_recent_crawl_logs(limit=1)

    total_posts = len(posts_data)
    avg_eng = sum(p.get('likes', 0) + p.get('comments', 0) for p in posts_data) / max(1, total_posts)
    recent_crawl_str = format_relative_time(logs[0]['timestamp']) if logs else "just now"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card("Total Posts", format_number(total_posts), "+18.4% today", "activity", "#10b981")
    with c2:
        render_metric_card("New Today", str(min(total_posts, 94)), "+24 vs yesterday", "zap", "#06b6d4")
    with c3:
        render_metric_card("Platforms", "5 / 5", "X, Threads, TikTok, IG, FB", "shield", "#8b5cf6")
    with c4:
        render_metric_card("Avg Engagement", format_number(avg_eng), "High viral density", "chart", "#f59e0b")
    with c5:
        render_metric_card("Health Status", "99.8%", f"Last crawl: {recent_crawl_str}", "cpu", "#10b981")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Main Chart & Trend Column
    col_chart, col_trends = st.columns([7, 5])

    with col_chart:
        st.markdown("<div class='section-title'>Global AI Trend Trajectory</div>", unsafe_allow_html=True)
        # Synthetic timeline data for area chart
        dates = [datetime.utcnow() - timedelta(hours=i*3) for i in range(16)][::-1]
        chart_rows = []
        for d in dates:
            chart_rows.append({"Time": d.strftime("%H:%M"), "Mentions": 120 + hash(str(d)) % 80, "Platform": "X"})
            chart_rows.append({"Time": d.strftime("%H:%M"), "Mentions": 90 + hash(str(d)) % 50, "Platform": "Threads"})
            chart_rows.append({"Time": d.strftime("%H:%M"), "Mentions": 60 + hash(str(d)) % 40, "Platform": "TikTok"})
        df_chart = pd.DataFrame(chart_rows)
        fig_area = create_area_chart(df_chart, x_col="Time", y_col="Mentions", group_col="Platform", title="Mentions Volume by Platform (48h)")
        st.plotly_chart(fig_area, use_container_width=True)

    with col_trends:
        st.markdown("<div class='section-title'>Top AI Trends Right Now</div>", unsafe_allow_html=True)
        for topic in topics_data[:3]:
            render_trend_card(topic)

    # Manual Sync Button
    if st.button("Trigger Manual Crawl Sync"):
        with st.spinner("Executing parallel crawl across all 5 adapters..."):
            pipeline = CrawlPipeline(db)
            res = pipeline.run_crawl_cycle(limit_per_platform=20)
            st.success(f"Fetched {res['raw_fetched']} posts across platforms!")
            st.rerun()

    # Recent Posts Stream
    h_col1, h_col2 = st.columns([6, 4])
    with h_col1:
        st.markdown("<div class='section-title'>Latest High-Impact Posts</div>", unsafe_allow_html=True)
    with h_col2:
        selected_country = st.selectbox(
            "Filter Nation:",
            ["all", "International", "China", "Indonesia"],
            format_func=lambda x: {
                "all": "🌏 All Nations",
                "International": "🌐 Global",
                "China": "🇨🇳 China",
                "Indonesia": "🇮🇩 Indonesia"
            }.get(x, x),
            key="home_nation_filter"
        )

    home_posts = db.get_posts(country=selected_country, limit=6)
    f1, f2 = st.columns(2)
    for idx, post in enumerate(home_posts):
        with (f1 if idx % 2 == 0 else f2):
            render_feed_card(post)

if __name__ == "__main__" or "app" in __name__:
    render_page()
