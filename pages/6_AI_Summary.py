import streamlit as st
from database.db import DatabaseManager
from services.report_service import ReportService
from components.header import render_header
from components.icons import get_icon_html

def render_page():
    db = DatabaseManager()
    service = ReportService(db)

    render_header(
        title="AI Trend Summary & Digest",
        subtitle="OpenRouter LLM-synthesized daily intelligence digest covering breakthroughs, emerging tools, and model updates"
    )

    c_btn, c_info = st.columns([3, 7])
    with c_btn:
        if st.button("Generate Fresh AI Digest", type="primary"):
            with st.spinner("Generating LLM trend analysis via OpenRouter..."):
                digest = service.generate_daily_digest()
                st.success("New AI Trend Digest generated!")
                st.rerun()

    digest = service.get_latest_digest()
    if not digest or not digest.get("biggest_news"):
        digest = service.generate_daily_digest()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)


    # Render Digest Sections in sleek dark cards
    cpu_icon = get_icon_html("cpu", "#10b981")
    zap_icon = get_icon_html("zap", "#06b6d4")
    shield_icon = get_icon_html("shield", "#8b5cf6")

    # Section 1: Today's Biggest AI News
    st.markdown(f"""
    <div class="trend-card">
        <div class="trend-title" style="color: #10b981;">{zap_icon} Today's Biggest AI News</div>
        <div style="margin-top: 0.75rem; font-size: 0.9375rem; color: #e4e4e7; line-height: 1.6;">
            {digest.get('biggest_news', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Top Discussions
        discussions_html = "".join([f"<li style='margin-bottom: 6px;'>{d}</li>" for d in digest.get('top_discussions', [])])
        st.markdown(f"""
        <div class="trend-card">
            <div class="trend-title" style="color: #06b6d4;">Top Discussions & Debates</div>
            <ul style="margin-top: 0.75rem; padding-left: 1.2rem; font-size: 0.875rem; color: #a1a1aa; line-height: 1.5;">
                {discussions_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Emerging Tools
        tools_html = "".join([f"<li style='margin-bottom: 6px;'>{t}</li>" for t in digest.get('emerging_tools', [])])
        st.markdown(f"""
        <div class="trend-card">
            <div class="trend-title" style="color: #8b5cf6;">Emerging Tools & Frameworks</div>
            <ul style="margin-top: 0.75rem; padding-left: 1.2rem; font-size: 0.875rem; color: #a1a1aa; line-height: 1.5;">
                {tools_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Trending Companies & Models
        companies_str = ", ".join(digest.get('trending_companies', []))
        models_str = ", ".join(digest.get('most_discussed_models', []))

        st.markdown(f"""
        <div class="trend-card">
            <div class="trend-title" style="color: #f59e0b;">Trending Entities & Models</div>
            <div style="margin-top: 0.75rem; font-size: 0.875rem; color: #a1a1aa; line-height: 1.6;">
                <div style="margin-bottom: 8px;"><strong style="color: #fafafa;">Companies:</strong> {companies_str}</div>
                <div><strong style="color: #fafafa;">Most Discussed Models:</strong> {models_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Key Releases
        releases_html = "".join([f"<li style='margin-bottom: 6px;'>{r}</li>" for r in digest.get('important_releases', [])])
        st.markdown(f"""
        <div class="trend-card">
            <div class="trend-title" style="color: #10b981;">Important Model & Software Releases</div>
            <ul style="margin-top: 0.75rem; padding-left: 1.2rem; font-size: 0.875rem; color: #a1a1aa; line-height: 1.5;">
                {releases_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Hallucination Minimization Badge
    st.markdown(f"""
    <div style="margin-top: 1rem; padding: 0.75rem; background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; font-size: 0.75rem; color: #71717a; display: flex; align-items: center; justify-content: space-between;">
        <span>{shield_icon} VERIFIED AGATHA DATA: {digest.get('hallucination_warning', 'Grounded strictly in crawl data.')}</span>
        <span>Report Created: {digest.get('created_at', 'Today')}</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__" or "app" in __name__:
    render_page()
