"""
Smart Campus Analytics & Student Success Platform
Charts Component — Plotly visualizations adhering to visual tokens and accessible palettes.
"""

from typing import Dict, Any, List, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Palette constants
COLOR_PRIMARY = "#3B5BDB"
COLOR_SUCCESS = "#16803C"
COLOR_WARNING = "#B54708"
COLOR_DANGER = "#B42318"
COLOR_MUTED = "#667085"
COLOR_BG_CARD = "#FFFFFF"

RISK_COLOR_MAP = {
    "High": COLOR_DANGER,
    "Medium": COLOR_WARNING,
    "Low": COLOR_SUCCESS,
    "Placement Ready": COLOR_SUCCESS,
    "Insufficient Data": COLOR_MUTED,
    "N/A (Year 1)": "#94A3B8",
    "N/A (Pending)": "#94A3B8",
}

BAND_COLOR_MAP = {
    "Strong Progress": COLOR_SUCCESS,
    "On Track / Monitor": COLOR_PRIMARY,
    "Needs Support": COLOR_WARNING,
    "Priority Support": COLOR_DANGER,
    "Insufficient Data": COLOR_MUTED,
}


def apply_common_layout(fig: go.Figure, title: str, height: int = 350) -> go.Figure:
    """Applies unified typography, borders, and margins to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "y": 0.95,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 15, "color": "#172033", "family": "Plus Jakarta Sans, sans-serif"},
        },
        paper_bgcolor=COLOR_BG_CARD,
        plot_bgcolor="#F8FAFC",
        height=height,
        margin={"l": 40, "r": 20, "t": 50, "b": 40},
        font={"family": "Plus Jakarta Sans, sans-serif", "color": "#172033"},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0", zeroline=False)
    return fig


def plot_score_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of Student Success Score with benchmark band bands."""
    valid_scores = df["success_score"].dropna()

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=valid_scores,
        nbinsx=20,
        marker_color=COLOR_PRIMARY,
        opacity=0.85,
        name="Students",
        hovertemplate="Score Range: %{x}<br>Count: %{y}<extra></extra>",
    ))

    # Add vertical reference lines for score bands
    fig.add_vline(x=50, line_dash="dash", line_color=COLOR_DANGER, annotation_text="Priority (50)", annotation_position="top left")
    fig.add_vline(x=65, line_dash="dash", line_color=COLOR_WARNING, annotation_text="Monitor (65)", annotation_position="top left")
    fig.add_vline(x=80, line_dash="dash", line_color=COLOR_SUCCESS, annotation_text="Strong (80)", annotation_position="top right")

    fig = apply_common_layout(fig, "Student Success Score Distribution (0–100)")
    fig.update_xaxes(title="Success Score", range=[0, 100])
    fig.update_yaxes(title="Number of Students")
    return fig


def plot_academic_risk_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart showing Academic Risk breakdown."""
    counts = df["academic_risk_level"].value_counts().reset_index()
    counts.columns = ["Risk Level", "Count"]

    colors = [RISK_COLOR_MAP.get(level, COLOR_MUTED) for level in counts["Risk Level"]]

    fig = go.Figure(data=[go.Pie(
        labels=counts["Risk Level"],
        values=counts["Count"],
        hole=0.55,
        marker={"colors": colors},
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Students: %{value} (%{percent})<extra></extra>",
    )])

    fig = apply_common_layout(fig, "Academic Support Need Breakdown")
    fig.update_layout(showlegend=False)
    return fig


def plot_placement_risk_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart showing Placement Readiness breakdown."""
    counts = df["placement_risk_level"].value_counts().reset_index()
    counts.columns = ["Readiness Level", "Count"]

    colors = [RISK_COLOR_MAP.get(level, COLOR_MUTED) for level in counts["Readiness Level"]]

    fig = go.Figure(data=[go.Pie(
        labels=counts["Readiness Level"],
        values=counts["Count"],
        hole=0.55,
        marker={"colors": colors},
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Students: %{value} (%{percent})<extra></extra>",
    )])

    fig = apply_common_layout(fig, "Placement Readiness Breakdown")
    fig.update_layout(showlegend=False)
    return fig


def plot_risk_by_department(df: pd.DataFrame) -> go.Figure:
    """Stacked bar chart showing Academic Risk by Department."""
    grouped = df.groupby(["department", "academic_risk_level"]).size().reset_index(name="Count")

    fig = px.bar(
        grouped,
        x="department",
        y="Count",
        color="academic_risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        category_orders={"academic_risk_level": ["High", "Medium", "Low", "Insufficient Data"]},
        barmode="stack",
    )

    fig = apply_common_layout(fig, "Academic Risk Distribution by Department", height=380)
    fig.update_xaxes(title="", tickangle=-15)
    fig.update_yaxes(title="Number of Students")
    return fig


def plot_student_radar_subscores(subscores: Dict[str, Optional[float]]) -> go.Figure:
    """Radar chart displaying the 7 indicator subscores for an individual student."""
    categories = [
        "Academic", "Attendance", "LMS Activity", "Placement",
        "Skills", "Engagement", "Feedback"
    ]
    keys = ["academic", "attendance", "lms", "placement", "skills", "engagement", "feedback"]

    values = []
    for k in keys:
        v = subscores.get(k)
        values.append(v if v is not None else 0.0)

    # Close radar loop
    r_vals = values + [values[0]]
    theta_cats = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_vals,
        theta=theta_cats,
        fill="toself",
        fillcolor="rgba(59, 91, 219, 0.25)",
        line={"color": COLOR_PRIMARY, "width": 2.5},
        marker={"size": 6, "color": COLOR_PRIMARY},
        hovertemplate="<b>%{theta}</b>: %{r:.1f}/100<extra></extra>",
    ))

    fig.update_layout(
        polar={
            "radialaxis": {"visible": True, "range": [0, 100], "tickfont": {"size": 10}},
            "bgcolor": "#F8FAFC",
        },
        paper_bgcolor=COLOR_BG_CARD,
        margin={"l": 30, "r": 30, "t": 35, "b": 30},
        height=320,
        showlegend=False,
        title={"text": "<b>Indicator Breakdown (0–100)</b>", "font": {"size": 14, "color": "#172033"}},
    )
    return fig


def plot_segments_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of student segments count."""
    counts = df["primary_segment"].value_counts().reset_index()
    counts.columns = ["Segment", "Count"]

    fig = px.bar(
        counts,
        y="Segment",
        x="Count",
        orientation="h",
        color="Segment",
        color_discrete_sequence=px.colors.qualitative.Prism,
    )

    fig = apply_common_layout(fig, "Student Segment Distribution", height=360)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="Number of Students")
    fig.update_yaxes(title="")
    return fig
