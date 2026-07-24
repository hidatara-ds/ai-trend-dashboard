import streamlit as st
from typing import Dict, Any
from utils.formatters import format_number, format_relative_time
from components.icons import get_icon_html

def render_feed_card(post: Dict[str, Any]):
    platform = post.get("platform", "x").lower()
    author = post.get("author", "@unknown")
    text = post.get("text", "")
    created_rel = format_relative_time(post.get("created_at", ""))
    url = post.get("url", "#")
    trend_score = post.get("trend_score", 0.0)

    likes = format_number(post.get("likes", 0))
    comments = format_number(post.get("comments", 0))
    shares = format_number(post.get("shares", 0))
    views = format_number(post.get("views", 0))

    ext_icon = get_icon_html("external", "#a1a1aa")

    html = f"""
    <div class="feed-card">
        <div class="feed-header">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="platform-badge badge-{platform}">{platform.upper()}</span>
                <span class="feed-author">{author}</span>
                <span style="color: #71717a; font-size: 0.75rem;">• {created_rel}</span>
            </div>
            <div style="font-size: 0.75rem; color: #10b981; font-weight: 600;">
                TREND SCORE {trend_score}
            </div>
        </div>
        <div class="feed-text">{text}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #27272a; padding-top: 0.5rem; font-size: 0.75rem; color: #a1a1aa;">
            <div style="display: flex; gap: 1rem;">
                <span>LIKES <strong>{likes}</strong></span>
                <span>COMMENTS <strong>{comments}</strong></span>
                <span>SHARES <strong>{shares}</strong></span>
                <span>VIEWS <strong>{views}</strong></span>
            </div>
            <a href="{url}" target="_blank" style="color: #06b6d4; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">
                Original Post {ext_icon}
            </a>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
