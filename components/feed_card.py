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

    country = post.get("country", "International")
    translation_en = post.get("translation_en")

    country_badges = {
        "China": ('🇨🇳 China', "rgba(249, 115, 22, 0.15)", "#f97316", "rgba(249, 115, 22, 0.3)"),
        "Indonesia": ('🇮🇩 Indonesia', "rgba(239, 68, 68, 0.15)", "#ef4444", "rgba(239, 68, 68, 0.3)"),
        "International": ('🌐 Global', "rgba(59, 130, 246, 0.15)", "#3b82f6", "rgba(59, 130, 246, 0.3)")
    }
    c_label, c_bg, c_text, c_border = country_badges.get(country, ('🌐 Global', "rgba(59, 130, 246, 0.15)", "#3b82f6", "rgba(59, 130, 246, 0.3)"))

    likes = format_number(post.get("likes", 0))
    comments = format_number(post.get("comments", 0))
    shares = format_number(post.get("shares", 0))
    views = format_number(post.get("views", 0))

    ext_icon = get_icon_html("external", "#a1a1aa")

    translation_html = ""
    if translation_en and translation_en.strip():
        translation_html = f'<div style="margin-top: 0.6rem; padding: 0.5rem 0.75rem; background: #18181b; border-left: 3px solid #06b6d4; border-radius: 4px; font-size: 0.8rem; color: #d4d4d8;"><div style="font-size: 0.7rem; color: #06b6d4; font-weight: 700; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.05em;">🇬🇧 English Translation</div><div>{translation_en}</div></div>'

    html = (
        f'<div class="feed-card">'
        f'<div class="feed-header">'
        f'<div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">'
        f'<span class="platform-badge badge-{platform}">{platform.upper()}</span>'
        f'<span style="font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 12px; background: {c_bg}; color: {c_text}; border: 1px solid {c_border};">{c_label}</span>'
        f'<span class="feed-author">{author}</span>'
        f'<span style="color: #71717a; font-size: 0.75rem;">• {created_rel}</span>'
        f'</div>'
        f'<div style="font-size: 0.75rem; color: #10b981; font-weight: 600;">SCORE {trend_score}</div>'
        f'</div>'
        f'<div class="feed-text">{text}</div>'
        f'{translation_html}'
        f'<div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #27272a; margin-top: 0.6rem; padding-top: 0.5rem; font-size: 0.75rem; color: #a1a1aa;">'
        f'<div style="display: flex; gap: 1rem;">'
        f'<span>LIKES <strong>{likes}</strong></span>'
        f'<span>COMMENTS <strong>{comments}</strong></span>'
        f'<span>SHARES <strong>{shares}</strong></span>'
        f'<span>VIEWS <strong>{views}</strong></span>'
        f'</div>'
        f'<a href="{url}" target="_blank" style="color: #06b6d4; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;">Original Post {ext_icon}</a>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
