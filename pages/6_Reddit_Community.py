import streamlit as st
from database.db import DatabaseManager
from crawler.socialcrawl import SocialCrawlAdapter
from components.header import render_header
from components.icons import get_icon_html
from utils.formatters import format_number, format_relative_time

def render_page():
    db = DatabaseManager()
    render_header(
        title="Reddit AI Community Discussions",
        subtitle="Live discussions, open-source model benchmarks, and developer threads from top AI subreddits"
    )

    st.markdown("<div class='section-title'>Subreddit Filter & Hot Threads</div>", unsafe_allow_html=True)
    
    subreddits = ["All Subreddits", "r/LocalLLaMA", "r/MachineLearning", "r/OpenAI", "r/ChatGPT", "r/singularity"]
    selected_sub = st.selectbox("Select Subreddit:", subreddits, index=0)

    # Fetch Reddit posts from DB or live adapter
    posts = db.get_posts(platform="reddit", limit=50)
    if not posts:
        # Trigger quick Reddit crawl cycle
        adapter = SocialCrawlAdapter()
        reddit_posts = adapter.fetch_reddit_posts(limit=25)
        if reddit_posts:
            db.save_posts(db.score_posts(reddit_posts) if hasattr(db, 'score_posts') else reddit_posts)
            posts = db.get_posts(platform="reddit", limit=50)

    filtered_posts = posts
    if selected_sub != "All Subreddits":
        sub_name = selected_sub.replace("r/", "").lower()
        filtered_posts = [p for p in filtered_posts if sub_name in p.get("text", "").lower() or sub_name in p.get("author", "").lower()]

    if not filtered_posts:
        st.info(f"No active threads found for {selected_sub}. Click below to refresh Reddit feed!")

    ext_icon = get_icon_html("external", "#ff4500")

    # Display Reddit Thread Cards
    for post in filtered_posts[:15]:
        author = post.get("author", "u/reddit_user")
        text = post.get("text", "")
        url = post.get("url", "#")
        likes = format_number(post.get("likes", 0))
        comments = format_number(post.get("comments", 0))
        rel_time = format_relative_time(post.get("created_at", ""))
        score = post.get("trend_score", 78.5)

        html = f"""
        <div style="background: #18181b; border: 1px solid #27272a; border-left: 4px solid #ff4500; border-radius: 8px; padding: 1rem; margin-bottom: 0.85rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: rgba(255,69,0,0.15); color: #ff4500; border: 1px solid rgba(255,69,0,0.3); font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 4px;">REDDIT AI</span>
                    <span style="font-size: 0.8rem; color: #a1a1aa; font-weight: 600;">{author}</span>
                    <span style="font-size: 0.75rem; color: #71717a;">• {rel_time}</span>
                </div>
                <div style="font-size: 0.75rem; color: #10b981; font-weight: 700; background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 4px;">SCORE {score}</div>
            </div>
            <div style="font-size: 0.95rem; color: #fafafa; font-weight: 600; line-height: 1.4; margin-bottom: 0.75rem;">
                {text}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #27272a; padding-top: 0.5rem; font-size: 0.75rem; color: #a1a1aa;">
                <div style="display: flex; gap: 1.2rem;">
                    <span>⬆️ Upvotes <strong style="color: #fafafa;">{likes}</strong></span>
                    <span>💬 Comments <strong style="color: #fafafa;">{comments}</strong></span>
                </div>
                <a href="{url}" target="_blank" style="color: #ff4500; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                    Open Thread {ext_icon}
                </a>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

if __name__ == "__main__" or "app" in __name__:
    render_page()
