import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

PLOTLY_DARK_LAYOUT = dict(
    paper_bgcolor="#09090b",
    plot_bgcolor="#09090b",
    font=dict(color="#fafafa", family="Inter, system-ui, -apple-system, sans-serif"),
    xaxis=dict(
        gridcolor="#27272a",
        zerolinecolor="#27272a",
        tickfont=dict(color="#a1a1aa"),
        titlefont=dict(color="#a1a1aa")
    ),
    yaxis=dict(
        gridcolor="#27272a",
        zerolinecolor="#27272a",
        tickfont=dict(color="#a1a1aa"),
        titlefont=dict(color="#a1a1aa")
    ),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        font=dict(color="#a1a1aa"),
        bgcolor="rgba(0,0,0,0)"
    )
)

def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, group_col: str = None, title: str = "") -> go.Figure:
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        title=title,
        color_discrete_sequence=["#10b981", "#06b6d4", "#8b5cf6", "#f59e0b", "#f43f5e"]
    )
    fig.update_layout(**PLOTLY_DARK_LAYOUT)
    fig.update_traces(mode="lines+markers", line=dict(width=2.5), marker=dict(size=6))
    return fig

def create_area_chart(df: pd.DataFrame, x_col: str, y_col: str, group_col: str = None, title: str = "") -> go.Figure:
    fig = px.area(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        title=title,
        color_discrete_sequence=["#06b6d4", "#8b5cf6", "#10b981", "#f59e0b", "#f43f5e"]
    )
    fig.update_layout(**PLOTLY_DARK_LAYOUT)
    return fig

def create_heatmap(df: pd.DataFrame, x_col: str, y_col: str, z_col: str, title: str = "") -> go.Figure:
    pivot = df.pivot(index=y_col, columns=x_col, values=z_col).fillna(0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[[0, "#18181b"], [0.5, "#06b6d4"], [1.0, "#10b981"]],
        showscale=True
    ))
    fig.update_layout(title=title, **PLOTLY_DARK_LAYOUT)
    return fig

def create_treemap(topics: List[Dict[str, Any]], title: str = "Trending AI Topics Hierarchy") -> go.Figure:
    df = pd.DataFrame(topics)
    if df.empty:
        df = pd.DataFrame([{"name": "No Topics", "mentions_count": 1, "trend_score": 50}])

    fig = px.treemap(
        df,
        path=["name"],
        values="mentions_count",
        color="trend_score",
        title=title,
        color_continuous_scale=["#27272a", "#06b6d4", "#10b981"]
    )
    fig.update_layout(**PLOTLY_DARK_LAYOUT)
    fig.update_traces(marker=dict(cornerradius=6))
    return fig

def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "", orientation: str = "v") -> go.Figure:
    fig = px.bar(
        df,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        orientation=orientation,
        title=title,
        color_discrete_sequence=["#10b981"]
    )
    fig.update_layout(**PLOTLY_DARK_LAYOUT)
    fig.update_traces(marker_line_color="#10b981", marker_line_width=1, opacity=0.85)
    return fig

def create_timeline_chart(events: List[Dict[str, Any]], title: str = "AI Release Timeline") -> go.Figure:
    df = pd.DataFrame(events)
    fig = px.scatter(
        df,
        x="date",
        y="category",
        size="importance",
        color="category",
        hover_name="title",
        title=title,
        color_discrete_sequence=["#10b981", "#06b6d4", "#8b5cf6", "#f59e0b"]
    )
    fig.update_layout(**PLOTLY_DARK_LAYOUT)
    return fig
