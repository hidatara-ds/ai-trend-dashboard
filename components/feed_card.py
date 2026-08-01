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
        translation_html = f'<div style="margin-top: 0.6rem; padding: 0.5rem 0.75rem; background: #18181b; border-left: 3px solid #06b6d4; border-radius: 6px; font-size: 0.8rem; color: #d4d4d8;"><div style="font-size: 0.7rem; color: #06b6d4; font-weight: 700; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.05em;">🇬🇧 English Translation</div><div>{translation_en}</div></div>'

    entities = post.get("entities", {})
    entity_pills = ""
    if isinstance(entities, dict):
        all_ents = [item for sublist in entities.values() if isinstance(sublist, list) for item in sublist][:3]
        if all_ents:
            entity_pills = '<div style="display: flex; gap: 4px; margin-top: 6px; flex-wrap: wrap;">' + "".join([f'<span style="font-size: 0.65rem; background: #27272a; color: #a1a1aa; padding: 1px 6px; border-radius: 4px;">#{e}</span>' for e in all_ents]) + '</div>'

    html = f'<div class="feed-card" style="transition: transform 0.15s ease, box-shadow 0.15s ease;"><div class="feed-header"><div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;"><span class="platform-badge badge-{platform}">{platform.upper()}</span><span style="font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 12px; background: {c_bg}; color: {c_text}; border: 1px solid {c_border};">{c_label}</span><span class="feed-author">{author}</span><span style="color: #71717a; font-size: 0.75rem;">• {created_rel}</span></div><div style="font-size: 0.75rem; color: #10b981; font-weight: 700; background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 6px;">SCORE {trend_score}</div></div><div class="feed-text">{text}</div>{translation_html}{entity_pills}<div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #27272a; margin-top: 0.6rem; padding-top: 0.5rem; font-size: 0.75rem; color: #a1a1aa;"><div style="display: flex; gap: 1rem;"><span>LIKES <strong>{likes}</strong></span><span>COMMENTS <strong>{comments}</strong></span><span>SHARES <strong>{shares}</strong></span><span>VIEWS <strong>{views}</strong></span></div><a href="{url}" target="_blank" style="color: #06b6d4; text-decoration: none; display: inline-flex; align-items: center; gap: 4px; font-weight: 600;">Original Post {ext_icon}</a></div></div>'
    st.markdown(html, unsafe_allow_html=True)

