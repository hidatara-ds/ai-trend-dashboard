import streamlit as st
import pandas as pd
from database.db import DatabaseManager
from components.header import render_header
from components.trend_card import render_trend_card
from components.feed_card import render_feed_card
from utils.charts import create_treemap, create_bar_chart

def render_page():
    db = DatabaseManager()
    render_header(
        title="Trending AI Topics",
        subtitle="Clustered AI topics sorted by virality, mentions volume, and community sentiment"
    )

    topics = db.get_topics(limit=30)
    if not topics:
        st.info("No topics available yet. Please trigger a crawl cycle in Settings or Home.")
        return

    # Visual Treemap of Topics
    st.markdown("<div class='section-title'>Topic Volume & Score Treemap</div>", unsafe_allow_html=True)
    fig_tree = create_treemap(topics, title="AI Topic Mentions Magnitude")
    st.plotly_chart(fig_tree, use_container_width=True)

    # Search & Filter bar
    st.markdown("<div class='section-title'>All Detected AI Topics</div>", unsafe_allow_html=True)
    search_term = st.text_input("Filter Topics by keyword...", "", placeholder="e.g. reasoning, cursor, sonnet, agents")

    filtered_topics = [
        t for t in topics
        if not search_term or search_term.lower() in t["name"].lower() or search_term.lower() in t["summary"].lower()
    ]

    col1, col2 = st.columns(2)

    for idx, topic in enumerate(filtered_topics):
        with (col1 if idx % 2 == 0 else col2):
            render_trend_card(topic)
            with st.expander(f"Inspect Topic Details: {topic['name']}"):
                st.markdown(f"**Executive Summary:** {topic['summary']}")
                st.markdown(f"**Growth:** +{topic['growth_pct']}% | **Sentiment:** {topic['sentiment_score']} | **Confidence:** {int(topic['confidence_score']*100)}%")

                entities = topic.get("key_entities", {})
                if entities:
                    st.markdown("##### Extracted Entities:")
                    for cat, items in entities.items():
                        st.markdown(f"- **{cat.capitalize()}:** {', '.join(items)}")

                # Matching sample posts from database
                kw = topic['name'].split()[0].lower()
                matching_posts = db.get_posts(search_query=kw, limit=3)
                if matching_posts:
                    st.markdown("##### Key Posts:")
                    for mp in matching_posts:
                        render_feed_card(mp)

if __name__ == "__main__" or "app" in __name__:
    render_page()
