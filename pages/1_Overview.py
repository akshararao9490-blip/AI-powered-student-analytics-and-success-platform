"""
Smart Campus Analytics & Student Success Platform
Page 1 — Institutional Overview Dashboard.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.metric_cards import render_metric_card
from components.charts import (
    plot_score_distribution,
    plot_academic_risk_donut,
    plot_placement_risk_donut,
    plot_risk_by_department,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
    COLOR_PRIMARY,
)
from services.state import get_current_dataset, set_custom_dataset

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Institutional Overview Dashboard",
    subtitle="Macro performance metrics, department risk distributions & campus-wide indicators",
    icon="📊"
)

# Top KPIs
total_students = len(df_filtered)
avg_score = df_filtered["success_score"].dropna().mean() if total_students > 0 else 0.0
high_risk_count = len(df_filtered[df_filtered["academic_risk_level"] == "High"])
medium_risk_count = len(df_filtered[df_filtered["academic_risk_level"] == "Medium"])
placement_ready_count = len(df_filtered[df_filtered["placement_risk_level"] == "Placement Ready"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("Enrolled Students", f"{total_students:,}", f"Across {df_filtered['department'].nunique()} Branches", border_accent=COLOR_PRIMARY)
with c2:
    render_metric_card("Average Success Score", f"{avg_score:.1f}/100", "Campus-wide composite", border_accent=COLOR_SUCCESS if avg_score >= 70 else COLOR_WARNING)
with c3:
    render_metric_card("Academic Support Required", f"{high_risk_count + medium_risk_count}", f"{high_risk_count} High • {medium_risk_count} Med", color_accent=COLOR_DANGER, border_accent=COLOR_DANGER)
with c4:
    render_metric_card("Placement Ready Students", f"{placement_ready_count}", "Senior batches assessed", border_accent=COLOR_SUCCESS)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Charts Section
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_score_distribution(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_risk_by_department(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_academic_risk_donut(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_placement_risk_donut(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Department Breakdown Table
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏢 Department-Wise Cohort Summary</div>', unsafe_allow_html=True)

dept_summary = df_filtered.groupby("department").agg(
    Total_Students=("student_id", "count"),
    Avg_Success_Score=("success_score", lambda s: round(s.dropna().mean(), 1)),
    High_Academic_Risk=("academic_risk_level", lambda s: (s == "High").sum()),
    Placement_Ready=("placement_risk_level", lambda s: (s == "Placement Ready").sum()),
    Avg_Attendance=("attendance_pct", lambda s: round(pd.to_numeric(s, errors="coerce").mean(), 1)),
    Total_Backlogs=("backlog_count", lambda s: int(pd.to_numeric(s, errors="coerce").fillna(0).sum())),
).reset_index()

st.dataframe(dept_summary, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
