import streamlit as st
from database.db import DatabaseManager
from components.header import render_header
from components.icons import get_icon_html
from utils.formatters import format_relative_time

def render_page():
    db = DatabaseManager()
    render_header(
        title="AI News Reader",
        subtitle="Dedicated portal for exploring up-to-date live AI news, model breakthroughs, and tech articles with image previews"
    )

    posts = db.get_posts(limit=60)
    
    # Filter only posts with news/articles or text content
    news_posts = [p for p in posts if p.get("text")]

    st.markdown("<div class='section-title'>Live AI Headlines & Articles</div>", unsafe_allow_html=True)
    
    # Category / Nation Filters
    c1, c2 = st.columns([2, 1])
    with c1:
        search_query = st.text_input("🔍 Search AI News:", "", placeholder="Type topic, e.g., DeepSeek, Claude 3.7, OpenAI, Agent...")
    with c2:
        selected_country = st.selectbox("Filter Region:", ["All Regions", "International", "China", "Indonesia"])

    filtered_posts = news_posts
    if search_query.strip():
        sq = search_query.strip().lower()
        filtered_posts = [p for p in filtered_posts if sq in p.get("text", "").lower() or sq in p.get("author", "").lower()]

    if selected_country != "All Regions":
        filtered_posts = [p for p in filtered_posts if p.get("country") == selected_country]

    if not filtered_posts:
        st.info("No live news articles matching your filter. Try clearing the search or switching region filter!")
        return

    ext_icon = get_icon_html("external", "#06b6d4")

    # Render Grid of News Cards with Hero Images
    cols = st.columns(3)
    for idx, post in enumerate(filtered_posts[:24]):
        col = cols[idx % 3]
        text = post.get("text", "")
        author = post.get("author", "@news_source")
        platform = post.get("platform", "x").lower()
        url = post.get("url", "#")
        
        # TikTok / broken image fallback handling
        tiktok_fallback = "https://images.unsplash.com/photo-1611605698335-8b1569810432?w=800&auto=format&fit=crop&q=80"
        general_fallback = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop&q=80"
        
        default_media = tiktok_fallback if platform == "tiktok" else general_fallback
        media = post.get("media") if post.get("media") and not "tiktok.com" in str(post.get("media")) else default_media

        rel_time = format_relative_time(post.get("created_at", ""))
        country = post.get("country", "International")

        country_badge = "🌐 Global"
        if country == "China":
            country_badge = "🇨🇳 China"
        elif country == "Indonesia":
            country_badge = "🇮🇩 Indonesia"

        with col:
            html = f"""
            <div style="background-color: #18181b; border: 1px solid #27272a; border-radius: 10px; overflow: hidden; margin-bottom: 1.25rem; transition: transform 0.2s ease;">
                <div style="height: 160px; width: 100%; overflow: hidden; position: relative; background: #09090b;">
                    <img src="{media}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.onerror=null; this.src='{default_media}';" />
                    <div style="position: absolute; top: 10px; left: 10px; background: rgba(9,9,11,0.85); border: 1px solid #27272a; color: #38bdf8; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 12px; backdrop-filter: blur(4px);">
                        {country_badge}
                    </div>
                    <div style="position: absolute; top: 10px; right: 10px; background: rgba(9,9,11,0.85); border: 1px solid #27272a; color: #a1a1aa; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">
                        {platform}
                    </div>
                </div>

                <div style="padding: 1rem;">
                    <div style="font-size: 0.75rem; color: #a1a1aa; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #06b6d4; font-weight: 600;">{author}</span>
                        <span>{rel_time}</span>
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #fafafa; line-height: 1.4; margin-bottom: 0.75rem; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; min-height: 3.9em;">
                        {text}
                    </div>
                    <div style="border-top: 1px solid #27272a; padding-top: 0.6rem; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.7rem; color: #10b981; font-weight: 700;">VIRALITY SCORE {post.get('trend_score', 82.0)}</span>
                        <a href="{url}" target="_blank" style="color: #38bdf8; text-decoration: none; font-size: 0.8rem; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                            Read Article {ext_icon}
                        </a>
                    </div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__" or "app" in __name__:
    render_page()
