"""
Smart Campus Analytics & Student Success Platform
Main Application Entry Point — HacXLerate 2026 (KPMG in India) — Team BIG BUSTERS.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Configure Streamlit page layout
st.set_page_config(
    page_title="Smart Campus Analytics | BIG BUSTERS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.metric_cards import render_metric_card
from components.charts import (
    plot_score_distribution,
    plot_academic_risk_donut,
    plot_placement_risk_donut,
    plot_risk_by_department,
    plot_student_radar_subscores,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SUCCESS,
    COLOR_PRIMARY,
)
from components.tables import render_student_summary_table
from services.state import get_current_dataset, set_custom_dataset, reset_to_sample_dataset
from services.intervention_tracker import add_intervention

# Apply Design Tokens CSS
inject_custom_styles()

# Load Data
df_full, validation_report = get_current_dataset()

# Sidebar & Global Filters
df_filtered, active_filters = render_sidebar(df_full)

# If custom file uploaded via sidebar
if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

# Page Header
render_page_header(
    title="Smart Campus Analytics & Student Success Platform",
    subtitle="Unified multi-domain student intelligence, transparent risk scoring & proactive intervention tracking",
    icon="🏛️"
)

# User Role Alert Banner
role = st.session_state.get("user_role", "Institutional Administrator")
st.markdown(
    f"""
    <div style="background-color: #EEF2FF; border-left: 4px solid #3B5BDB; padding: 10px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 13px; color: #1E293B;">
        👤 <b>Active Role:</b> {role} &nbsp;|&nbsp; 
        📊 Cohort Scope: <b>{len(df_filtered)}</b> of <b>{len(df_full)}</b> students selected &nbsp;|&nbsp;
        🎯 <i>Focus: Proactive early-warning decision support</i>
    </div>
    """,
    unsafe_allow_html=True,
)

# Top KPI Cards
total_students = len(df_filtered)
avg_score = df_filtered["success_score"].dropna().mean() if total_students > 0 else 0.0

high_risk_students = len(df_filtered[df_filtered["academic_risk_level"] == "High"])
medium_risk_students = len(df_filtered[df_filtered["academic_risk_level"] == "Medium"])
need_support_total = high_risk_students + medium_risk_students

placement_ready = len(df_filtered[df_filtered["placement_risk_level"] == "Placement Ready"])
low_att_count = len(df_filtered[pd.to_numeric(df_filtered["attendance_pct"], errors="coerce") < 75.0])

kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

with kpi_c1:
    render_metric_card(
        title="Total Cohort",
        value=f"{total_students:,}",
        subtitle=f"Across {df_filtered['department'].nunique()} departments",
        border_accent=COLOR_PRIMARY
    )

with kpi_c2:
    render_metric_card(
        title="Avg Success Score",
        value=f"{avg_score:.1f}/100" if not np.isnan(avg_score) else "N/A",
        subtitle="Transparent 7-domain composite",
        border_accent=COLOR_SUCCESS if avg_score >= 70 else COLOR_WARNING
    )

with kpi_c3:
    render_metric_card(
        title="Academic Support Required",
        value=f"{need_support_total} ({round(need_support_total/total_students*100, 1) if total_students else 0}%)",
        subtitle=f"{high_risk_students} High • {medium_risk_students} Medium",
        color_accent=COLOR_DANGER if high_risk_students > 0 else COLOR_WARNING,
        border_accent=COLOR_DANGER
    )

with kpi_c4:
    render_metric_card(
        title="Placement Ready",
        value=f"{placement_ready}",
        subtitle=f"Attendance Shortage (<75%): {low_att_count}",
        border_accent=COLOR_SUCCESS
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Overview Analytics Charts
row1_col1, row1_col2 = st.columns([1.2, 1])

with row1_col1:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_score_distribution(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_academic_risk_donut(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns([1, 1.2])

with row2_col1:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_placement_risk_donut(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_risk_by_department(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Priority Insights & Action Panel
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚡ High-Priority Support Actions</div>', unsafe_allow_html=True)

urgent_cohort = df_filtered[
    (df_filtered["academic_risk_level"] == "High") |
    (df_filtered["primary_segment"] == "Strong Academics, Low Placement Readiness")
].head(3)

if not urgent_cohort.empty:
    for _, student in urgent_cohort.iterrows():
        recs = student["recommendations"]
        top_rec = recs[0] if recs else None
        st.markdown(
            f"""
            <div class="recommendation-box" style="border-left-color: {student['academic_risk_color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #172033; font-size: 15px;">
                        {student['student_id']} — {student['student_name']} ({student['department']})
                    </span>
                    <span class="badge" style="background-color: {student['academic_risk_color']}20; color: {student['academic_risk_color']};">
                        {student['academic_risk_level']} Academic Risk
                    </span>
                </div>
                <div style="color: #475467; font-size: 13px; margin-bottom: 6px;">
                    <b>Risk Triggers:</b> {"; ".join(student["academic_risk_reasons"][:2])}
                </div>
                <div style="background-color: #FFFFFF; padding: 8px 12px; border-radius: 6px; border: 1px solid #E4E7EC; font-size: 13px;">
                    💡 <b>Recommended Action:</b> {top_rec['action'] if top_rec else 'Conduct mentor assessment.'} 
                    <span style="color: #667085; font-size: 12px; margin-left: 8px;">(Owner: {top_rec['owner'] if top_rec else 'Mentor'})</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("No students in the filtered cohort currently require critical priority action.")

st.markdown('</div>', unsafe_allow_html=True)

# Student Explorer Preview
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Student Explorer & Profile Drill-down</div>', unsafe_allow_html=True)

selected_student_id = render_student_summary_table(df_filtered, max_rows=25)

# Profile Modal / Detailed Drill-down
if selected_student_id:
    student_record = df_filtered[df_filtered["student_id"] == selected_student_id].iloc[0]
    st.markdown("---")
    st.markdown(f"### 🔍 Detailed Profile: {student_record['student_name']} ({student_record['student_id']})")

    pcol1, pcol2 = st.columns([1.2, 1])

    with pcol1:
        st.markdown(
            f"""
            <div style="background: #F8FAFC; padding: 18px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 16px;">
                <h4 style="margin: 0 0 10px 0; color: #0F172A;">Composite Success Score: <span style="color: {student_record['band_color']}; font-size: 24px;">{student_record['display_score']}/100</span> ({student_record['score_band']})</h4>
                <p style="color: #334155; font-size: 14px; margin: 0 0 10px 0;">{student_record['score_explanation']}</p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <span class="badge" style="background-color: {student_record['academic_risk_color']}20; color: {student_record['academic_risk_color']};">
                        Academic Risk: {student_record['academic_risk_level']}
                    </span>
                    <span class="badge" style="background-color: {student_record['placement_risk_color']}20; color: {student_record['placement_risk_color']};">
                        Placement: {student_record['placement_risk_level']}
                    </span>
                    <span class="badge badge-info">
                        Segment: {student_record['primary_segment']}
                    </span>
                    <span class="badge badge-neutral">
                        Data Coverage: {student_record['data_coverage_pct']}%
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### 📌 Key Indicator Observations")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("CGPA", f"{student_record.get('cgpa') or 'N/A'}")
        sc2.metric("Attendance", f"{student_record.get('attendance_pct') or 'N/A'}%")
        sc3.metric("Backlogs", f"{student_record.get('backlog_count') or 0}")
        sc4.metric("Coding Score", f"{student_record.get('coding_score_pct') or 'N/A'}%")

        st.markdown("##### 🎯 Recommended Next Steps")
        for rec in student_record["recommendations"][:2]:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border-left: 3px solid #3B5BDB; padding: 10px 14px; margin-bottom: 8px; border-radius: 0 6px 6px 0; border: 1px solid #E2E8F0; border-left-width: 4px;">
                    <div style="font-weight: 600; color: #172033; font-size: 13px;">{rec['category']} ({rec['priority']} Priority)</div>
                    <div style="font-size: 13px; color: #475467;">{rec['action']}</div>
                    <div style="font-size: 11px; color: #667085; margin-top: 4px;">Responsible: {rec['owner']} • Target: {rec['target_timeline']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Quick Add Intervention Form
        with st.expander("➕ Log Follow-Up Intervention for this Student"):
            with st.form(f"quick_intervention_{selected_student_id}"):
                int_cat = st.selectbox("Intervention Category", [
                    "Academic Remediation", "Attendance Counseling", "Placement Technical Training",
                    "Interview Coaching", "Quantitative Aptitude", "General Mentorship"
                ])
                int_action = st.text_area("Prescribed Action Plan", value=student_record["recommendations"][0]["action"] if student_record["recommendations"] else "")
                int_owner = st.text_input("Assigned Owner", value=f"Prof. Proctor ({student_record['department']})")
                int_timeline = st.selectbox("Target Timeline", ["Immediate (3 days)", "Within 7 days", "Next 2 weeks", "End of Semester"])
                submitted = st.form_submit_button("Record Intervention")
                if submitted:
                    add_intervention(
                        student_id=student_record["student_id"],
                        student_name=student_record["student_name"],
                        department=student_record["department"],
                        category=int_cat,
                        priority="High" if student_record["academic_risk_level"] == "High" else "Medium",
                        action=int_action,
                        owner=int_owner,
                        target_timeline=int_timeline,
                        status="In Progress",
                        notes="Logged via Student Explorer"
                    )
                    st.success(f"Intervention recorded for {student_record['student_name']}!")

    with pcol2:
        radar_fig = plot_student_radar_subscores(student_record["subscores"])
        st.plotly_chart(radar_fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
