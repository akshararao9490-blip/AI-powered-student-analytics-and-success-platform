"""
Smart Campus Analytics & Student Success Platform
Metric Cards Component — Consistent KPI card renderings.
"""

from typing import Optional
import streamlit as st


def render_metric_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    color_accent: Optional[str] = None,
    border_accent: Optional[str] = None
) -> None:
    """Renders a single styled KPI card."""
    accent_style = f"border-left: 4px solid {border_accent};" if border_accent else ""
    value_style = f"color: {color_accent};" if color_accent else ""

    subtitle_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="kpi-card" style="{accent_style}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value" style="{value_style}">{value}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
