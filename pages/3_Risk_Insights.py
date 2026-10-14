"""
Smart Campus Analytics & Student Success Platform
Page 3 — Risk Insights & Explainable Early-Warning Analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.metric_cards import render_metric_card
from components.charts import (
    plot_academic_risk_donut,
    plot_placement_risk_donut,
    apply_common_layout,
    RISK_COLOR_MAP,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
)
from services.state import get_current_dataset, set_custom_dataset

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Risk Insights & Early-Warning Signals",
    subtitle="Deconstruct academic support needs & placement readiness gaps with explainable triggers",
    icon="⚠️"
)

# Risk KPIs
total_students = len(df_filtered)
high_acad = len(df_filtered[df_filtered["academic_risk_level"] == "High"])
med_acad = len(df_filtered[df_filtered["academic_risk_level"] == "Medium"])
att_short = len(df_filtered[pd.to_numeric(df_filtered["attendance_pct"], errors="coerce") < 75.0])
backlog_any = len(df_filtered[pd.to_numeric(df_filtered["backlog_count"], errors="coerce") > 0])
placement_at_risk = len(df_filtered[df_filtered["placement_risk_level"].isin(["High", "Medium"])])

rc1, rc2, rc3, rc4 = st.columns(4)
with rc1:
    render_metric_card("High Academic Risk", f"{high_acad}", f"{round(high_acad/total_students*100, 1) if total_students else 0}% of cohort", color_accent=COLOR_DANGER, border_accent=COLOR_DANGER)
with rc2:
    render_metric_card("Attendance Shortage", f"{att_short}", "<75% statutory bar", color_accent=COLOR_WARNING, border_accent=COLOR_WARNING)
with rc3:
    render_metric_card("Students with Backlogs", f"{backlog_any}", "Requiring remedial exam prep", border_accent=COLOR_DANGER)
with rc4:
    render_metric_card("Placement Gaps", f"{placement_at_risk}", "Coding or interview deficits", border_accent=COLOR_WARNING)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Scatter Visualizations: Academic standing & Placement proficiency
sc_col1, sc_col2 = st.columns(2)

with sc_col1:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    # Attendance vs CGPA Scatter Plot
    df_clean_plot = df_filtered.dropna(subset=["cgpa", "attendance_pct"]).copy()
    df_clean_plot["cgpa"] = pd.to_numeric(df_clean_plot["cgpa"], errors="coerce")
    df_clean_plot["attendance_pct"] = pd.to_numeric(df_clean_plot["attendance_pct"], errors="coerce")

    fig_acad_scatter = px.scatter(
        df_clean_plot,
        x="attendance_pct",
        y="cgpa",
        color="academic_risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        hover_data=["student_id", "student_name", "department", "backlog_count"],
        labels={"attendance_pct": "Attendance Percentage (%)", "cgpa": "CGPA (0–10)"},
        category_orders={"academic_risk_level": ["High", "Medium", "Low", "Insufficient Data"]},
    )
    fig_acad_scatter.add_vline(x=75, line_dash="dash", line_color=COLOR_WARNING, annotation_text="75% Min Attendance")
    fig_acad_scatter.add_hline(y=6.0, line_dash="dash", line_color="#94A3B8", annotation_text="6.0 CGPA")
    fig_acad_scatter = apply_common_layout(fig_acad_scatter, "Attendance vs. Academic Standing (CGPA)")
    st.plotly_chart(fig_acad_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with sc_col2:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    # Coding vs CGPA Scatter Plot for Placement
    df_placement_plot = df_filtered.dropna(subset=["cgpa", "coding_score_pct"]).copy()
    df_placement_plot["coding_score_pct"] = pd.to_numeric(df_placement_plot["coding_score_pct"], errors="coerce")
    df_placement_plot["cgpa"] = pd.to_numeric(df_placement_plot["cgpa"], errors="coerce")

    fig_place_scatter = px.scatter(
        df_placement_plot,
        x="coding_score_pct",
        y="cgpa",
        color="placement_risk_level",
        color_discrete_map=RISK_COLOR_MAP,
        hover_data=["student_id", "student_name", "department"],
        labels={"coding_score_pct": "Coding Assessment Score (%)", "cgpa": "CGPA (0–10)"},
    )
    fig_place_scatter.add_vline(x=50, line_dash="dash", line_color=COLOR_WARNING, annotation_text="50% Cut-Off")
    fig_place_scatter = apply_common_layout(fig_place_scatter, "Coding Proficiency vs. CGPA (Placement Cohort)")
    st.plotly_chart(fig_place_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Risk Driver Analysis
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Explainable Risk Trigger Breakdown</div>', unsafe_allow_html=True)

t1, t2 = st.tabs(["🚨 Academic Risk Signals", "💼 Placement Readiness Signals"])

with t1:
    high_academic_students = df_filtered[df_filtered["academic_risk_level"] == "High"]
    if not high_academic_students.empty:
        st.write(f"Identified **{len(high_academic_students)}** students crossing high academic risk thresholds:")
        acad_table_data = []
        for _, s in high_academic_students.iterrows():
            acad_table_data.append({
                "Student ID": s["student_id"],
                "Name": s["student_name"],
                "Department": s["department"],
                "Attendance": f"{s['attendance_pct']}%",
                "CGPA": s["cgpa"],
                "Backlogs": int(s["backlog_count"] or 0),
                "Key Triggers": "; ".join(s["academic_risk_reasons"]),
                "Primary Recommendation": s["recommendations"][0]["action"] if s["recommendations"] else "Mentor review"
            })
        st.dataframe(pd.DataFrame(acad_table_data), use_container_width=True, hide_index=True)
    else:
        st.success("No students currently exhibit high academic risk conditions in this cohort.")

with t2:
    placement_risk_students = df_filtered[df_filtered["placement_risk_level"].isin(["High", "Medium"])]
    if not placement_risk_students.empty:
        st.write(f"Identified **{len(placement_risk_students)}** students with placement readiness deficits:")
        place_table_data = []
        for _, s in placement_risk_students.iterrows():
            place_table_data.append({
                "Student ID": s["student_id"],
                "Name": s["student_name"],
                "Department": s["department"],
                "Coding Score": f"{s['coding_score_pct']}%" if s['coding_score_pct'] else "N/A",
                "Mock Interview": f"{s['mock_interview_pct']}%" if s['mock_interview_pct'] else "N/A",
                "Aptitude Score": f"{s['aptitude_score_pct']}%" if s['aptitude_score_pct'] else "N/A",
                "Resume": s.get("resume_ready", "N/A"),
                "Identified Gaps": "; ".join(s["placement_risk_reasons"]),
                "Action": s["recommendations"][0]["action"] if s["recommendations"] else "Placement coaching"
            })
        st.dataframe(pd.DataFrame(place_table_data), use_container_width=True, hide_index=True)
    else:
        st.success("All assessed students meet or exceed placement readiness standards.")

st.markdown('</div>', unsafe_allow_html=True)
