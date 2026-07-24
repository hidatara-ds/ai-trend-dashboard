import json
import streamlit as st
from database.db import DatabaseManager
from components.header import render_header
from config.settings import DEFAULT_PLATFORM_WEIGHTS
from services.pipeline import CrawlPipeline

def render_page():
    db = DatabaseManager()
    render_header(
        title="Settings & Configuration",
        subtitle="Manage OpenRouter LLM credentials, crawler keywords, scoring weights, and database maintenance"
    )

    tab_api, tab_keywords, tab_weights, tab_db = st.tabs([
        "API & LLM Config", "Tracked Keywords", "Platform Weights", "Database Maintenance"
    ])

    with tab_api:
        st.markdown("### OpenRouter API Credentials")
        current_api_key = db.get_setting("openrouter_api_key", "")
        current_model = db.get_setting("openrouter_model", "anthropic/claude-3.5-sonnet")

        api_key_input = st.text_input("OpenRouter API Key:", value=current_api_key, type="password", help="Required for AI Summary digest generation.")
        model_select = st.selectbox(
            "Default LLM Backend Model:",
            ["anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-001", "deepseek/deepseek-chat", "openai/gpt-4o-mini"],
            index=0 if current_model not in ["anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-001", "deepseek/deepseek-chat", "openai/gpt-4o-mini"] else ["anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-001", "deepseek/deepseek-chat", "openai/gpt-4o-mini"].index(current_model)
        )

        if st.button("Save API Settings", type="primary"):
            db.set_setting("openrouter_api_key", api_key_input.strip())
            db.set_setting("openrouter_model", model_select)
            st.success("API configuration updated successfully!")

    with tab_keywords:
        st.markdown("### Tracked Keywords")
        keywords = db.get_keywords_list()

        st.write("Current active keywords:", ", ".join(keywords))

        new_kw = st.text_input("Add new keyword to crawler:", "", placeholder="e.g. DeepSeek-V3, Qwen-Coder")
        if st.button("Add Keyword"):
            if new_kw.strip():
                db.add_keyword(new_kw.strip())
                st.success(f"Added keyword '{new_kw.strip()}'!")
                st.rerun()

        kw_to_remove = st.selectbox("Remove keyword:", keywords)
        if st.button("Remove Selected Keyword"):
            db.remove_keyword(kw_to_remove)
            st.success(f"Removed keyword '{kw_to_remove}'!")
            st.rerun()

    with tab_weights:
        st.markdown("### Platform Scoring Weights")
        st.caption("Adjust the multiplier contribution for each social platform in the trend scoring formula.")

        saved_weights_str = db.get_setting("platform_weights", json.dumps(DEFAULT_PLATFORM_WEIGHTS))
        try:
            current_weights = json.loads(saved_weights_str)
        except Exception:
            current_weights = DEFAULT_PLATFORM_WEIGHTS.copy()

        new_weights = {}
        for plat, weight in current_weights.items():
            new_weights[plat] = st.slider(f"{plat.upper()} Weight:", 0.1, 2.0, float(weight), 0.1)

        if st.button("Save Platform Weights"):
            db.set_setting("platform_weights", json.dumps(new_weights))
            st.success("Platform weights saved!")

    with tab_db:
        st.markdown("### Database Maintenance & Seeding")
        st.warning("Resetting database will clear cached posts and topics, then re-seed data.")

        col_seed, col_clear = st.columns(2)

        with col_seed:
            if st.button("Run Instant Seed Sync"):
                with st.spinner("Executing crawl sync cycle..."):
                    pipeline = CrawlPipeline(db)
                    res = pipeline.run_crawl_cycle(limit_per_platform=25)
                    st.success(f"Crawl completed! Saved {res['deduplicated_saved']} posts.")
                    st.rerun()

        with col_clear:
            if st.button("Reset Database Data", type="secondary"):
                db.reset_database_data()
                st.success("Database data cleared.")
                st.rerun()

if __name__ == "__main__" or "app" in __name__:
    render_page()
