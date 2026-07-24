import streamlit as st
from components.icons import get_icon_html

def render_header(title: str = "AI Social Trend Intelligence", subtitle: str = "Real-time AI discussion monitoring & multi-platform trend analytics"):
    zap_icon = get_icon_html("zap", "#10b981")
    html = f"""
    <div style="padding-bottom: 1rem; margin-bottom: 1.5rem; border-bottom: 1px solid #27272a; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                {zap_icon}
                <span style="font-size: 1.5rem; font-weight: 700; color: #fafafa; letter-spacing: -0.02em;">{title}</span>
            </div>
            <div style="font-size: 0.875rem; color: #a1a1aa; margin-top: 4px;">{subtitle}</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.75rem; color: #a1a1aa; display: flex; align-items: center; justify-content: flex-end; gap: 6px;">
                <span class="status-dot status-active"></span>
                <span style="color: #fafafa; font-weight: 600;">CRAWLER ONLINE</span>
            </div>
            <div style="font-size: 0.75rem; color: #71717a; margin-top: 2px;">Sync: 5 platforms connected</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
