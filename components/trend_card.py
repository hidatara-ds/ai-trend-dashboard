import streamlit as st
from typing import Dict, Any
from utils.formatters import format_number
from config.theme import PLATFORM_COLORS

def render_trend_card(topic: Dict[str, Any], key_prefix: str = ""):
    platforms_html = "".join([
        f'<span class="platform-badge badge-{p}" style="margin-right: 4px;">{p.upper()}</span>'
        for p in topic.get("platforms_involved", [])
    ])

    sent_score = topic.get("sentiment_score", 0.0)
    sent_color = "#10b981" if sent_score > 0.2 else "#f59e0b" if sent_score > -0.2 else "#f43f5e"
    sent_label = "Positive" if sent_score > 0.2 else "Neutral" if sent_score > -0.2 else "Negative"

    html = f"""
    <div class="trend-card">
        <div class="trend-header">
            <div>
                <div class="trend-title">{topic['name']}</div>
                <div style="margin-top: 4px;">{platforms_html}</div>
            </div>
            <div class="trend-score-badge">SCORE {topic['trend_score']}</div>
        </div>
        <div style="font-size: 0.875rem; color: #a1a1aa; margin-bottom: 0.75rem; line-height: 1.4;">
            {topic.get('summary', '')}
        </div>
        <div style="display: flex; gap: 1rem; font-size: 0.75rem; color: #71717a; border-top: 1px solid #27272a; padding-top: 0.5rem;">
            <div>GROWTH <strong style="color: #fafafa;">+{topic.get('growth_pct', 0)}%</strong></div>
            <div>MENTIONS <strong style="color: #fafafa;">{format_number(topic.get('mentions_count', 0))}</strong></div>
            <div>SENTIMENT <strong style="color: {sent_color};">{sent_label}</strong></div>
            <div>CONFIDENCE <strong style="color: #fafafa;">{int(topic.get('confidence_score', 0.9)*100)}%</strong></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
