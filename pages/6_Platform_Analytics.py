import streamlit as st
import pandas as pd
from database.db import DatabaseManager
from components.header import render_header
from components.metrics import render_metric_card
from utils.charts import create_heatmap, create_bar_chart
from utils.formatters import format_number
from config.theme import PLATFORM_COLORS

def render_page():
    db = DatabaseManager()
    render_header(
        title="Platform Analytics",
        subtitle="Comparative performance, engagement density, and activity heatmaps across connected sources"
    )

    metrics = db.get_platform_metrics()

    # Platform metric cards grid
    cols = st.columns(5)
    for idx, pm in enumerate(metrics):
        with cols[idx]:
            plat_color = PLATFORM_COLORS.get(pm.platform, {}).get("text", "#10b981")
            render_metric_card(
                title=pm.platform.upper(),
                value=str(pm.posts_count),
                subtext=f"Avg Eng: {format_number(pm.avg_engagement)}",
                icon_name="shield",
                accent_color=plat_color
            )
            st.markdown(f"""
            <div style="background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; padding: 0.75rem; margin-top: 0.5rem; font-size: 0.75rem; color: #a1a1aa;">
                <div>TOP TOPIC: <strong style="color: #fafafa;">{pm.top_topic}</strong></div>
                <div>GROWTH: <strong style="color: #10b981;">+{pm.growth_pct}%</strong></div>
                <div>STATUS: <strong style="color: #fafafa;">{pm.status.upper()}</strong></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # Activity Heatmap
    st.markdown("<div class='section-title'>Platform Hourly Activity Heatmap (UTC)</div>", unsafe_allow_html=True)

    # Generate hourly matrix for heatmap
    hours = [f"{h:02d}:00" for h in range(24)]
    heatmap_rows = []
    platforms = ["x", "threads", "tiktok", "instagram", "facebook"]

    for p in platforms:
        for h_idx, h in enumerate(hours):
            val = (hash(p + h) % 85) + (30 if p in ["x", "threads"] else 10)
            heatmap_rows.append({"Platform": p.upper(), "Hour": h, "Activity": val})

    df_heat = pd.DataFrame(heatmap_rows)
    fig_heat = create_heatmap(df_heat, x_col="Hour", y_col="Platform", z_col="Activity", title="Platform Activity Concentration Matrix")
    st.plotly_chart(fig_heat, use_container_width=True)

    # Comparative Engagement Bar Chart
    st.markdown("<div class='section-title'>Engagement Density Comparison</div>", unsafe_allow_html=True)
    df_comp = pd.DataFrame([
        {"Platform": pm.platform.upper(), "Avg Engagement": pm.avg_engagement}
        for pm in metrics
    ])
    fig_bar = create_bar_chart(df_comp, x_col="Platform", y_col="Avg Engagement", title="Average Interactions per Post")
    st.plotly_chart(fig_bar, use_container_width=True)

if __name__ == "__main__" or "app" in __name__:
    render_page()
