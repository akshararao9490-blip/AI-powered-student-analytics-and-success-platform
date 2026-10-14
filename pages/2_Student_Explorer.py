"""
Smart Campus Analytics & Student Success Platform
Page 2 — Student Explorer & Comprehensive Individual Profiles.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.charts import plot_student_radar_subscores
from components.tables import render_student_summary_table
from services.state import get_current_dataset, set_custom_dataset
from services.intervention_tracker import add_intervention, get_interventions_for_student

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Student Explorer & Profile Center",
    subtitle="Search individual student records, understand scoring drivers & prescribe actionable interventions",
    icon="🔍"
)

st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">👥 Student Cohort Roster</div>', unsafe_allow_html=True)

selected_student_id = render_student_summary_table(df_filtered, max_rows=100)
st.markdown('</div>', unsafe_allow_html=True)

if selected_student_id:
    student = df_filtered[df_filtered["student_id"] == selected_student_id].iloc[0]

    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">🎓 Student Detail: {student["student_name"]} ({student["student_id"]})</div>', unsafe_allow_html=True)

    col_meta1, col_meta2 = st.columns([1.3, 1])

    with col_meta1:
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 18px; border-radius: 12px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 16px; font-weight: 700; color: #172033;">{student['department']} — Year {student['academic_year']} (Sem {student['semester']})</span>
                    <span class="badge" style="background-color: {student['band_color']}20; color: {student['band_color']}; font-size: 13px;">
                        Score: {student['display_score']}/100 ({student['score_band']})
                    </span>
                </div>
                <p style="color: #475467; font-size: 13px; line-height: 1.5; margin: 0 0 10px 0;">
                    <b>Explainable Score Assessment:</b> {student['score_explanation']}
                </p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <span class="badge" style="background-color: {student['academic_risk_color']}20; color: {student['academic_risk_color']};">
                        Academic Risk: {student['academic_risk_level']}
                    </span>
                    <span class="badge" style="background-color: {student['placement_risk_color']}20; color: {student['placement_risk_color']};">
                        Placement: {student['placement_risk_level']}
                    </span>
                    <span class="badge badge-info">
                        Segment: {student['primary_segment']}
                    </span>
                    <span class="badge badge-neutral">
                        Completeness: {student['data_coverage_pct']}%
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tabbed details: Indicators, Drivers, and Recommendations
        tab_ind, tab_rec, tab_hist = st.tabs(["📊 Multi-Domain Indicators", "🎯 Prescribed Interventions", "📝 Intervention History"])

        with tab_ind:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("CGPA", f"{student.get('cgpa') or 'N/A'}")
            m2.metric("Attendance", f"{student.get('attendance_pct') or 'N/A'}%")
            m3.metric("Backlogs", f"{int(student.get('backlog_count') or 0)}")
            m4.metric("Internal Marks", f"{student.get('internal_marks_pct') or 'N/A'}%")

            m5, m6, m7, m8 = st.columns(4)
            m5.metric("LMS Logins/Wk", f"{student.get('lms_logins_per_week') or 'N/A'}")
            m6.metric("LMS Submissions", f"{student.get('assignment_completion_pct') or 'N/A'}%")
            m7.metric("Coding Assessment", f"{student.get('coding_score_pct') or 'N/A'}%")
            m8.metric("Mock Interview", f"{student.get('mock_interview_pct') or 'N/A'}%")

            st.markdown("##### 🔍 Score Weight Contributions")
            weights = student["normalized_weights"]
            subscores = student["subscores"]
            weight_data = []
            for cat, w in weights.items():
                s = subscores.get(cat)
                weight_data.append({
                    "Category": cat.title(),
                    "Assigned Weight": f"{round(w * 100, 1)}%",
                    "Normalized Subscore (0-100)": f"{round(s, 1) if s is not None else 'N/A'}",
                    "Weighted Contribution": f"{round((s or 0) * w, 1)} pts"
                })
            st.dataframe(pd.DataFrame(weight_data), use_container_width=True, hide_index=True)

        with tab_rec:
            st.markdown("##### 💡 Recommended Targeted Actions")
            for rec in student["recommendations"]:
                st.markdown(
                    f"""
                    <div class="recommendation-box">
                        <div style="font-weight: 700; color: #172033; font-size: 14px;">
                            {rec['category']} • <span style="color: #B42318;">{rec['priority']} Priority</span>
                        </div>
                        <div style="color: #334155; font-size: 13px; margin: 4px 0;">{rec['action']}</div>
                        <div style="font-size: 12px; color: #667085;">
                            <b>Trigger:</b> {rec['trigger']} &nbsp;|&nbsp; <b>Owner:</b> {rec['owner']} &nbsp;|&nbsp; <b>Target:</b> {rec['target_timeline']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.form("add_intervention_form"):
                st.markdown("##### ➕ Log Custom Action / Follow-Up")
                c_cat, c_pri = st.columns(2)
                with c_cat:
                    form_cat = st.selectbox("Category", [
                        "Academic Remediation", "Attendance Counseling", "Placement Technical Training",
                        "Interview Coaching", "Quantitative Aptitude", "General Mentorship"
                    ])
                with c_pri:
                    form_pri = st.selectbox("Priority", ["High", "Medium", "Low"])

                form_action = st.text_area("Prescribed Action Plan", value=student["recommendations"][0]["action"] if student["recommendations"] else "")
                form_owner = st.text_input("Assigned Mentor / Owner", value=f"Dr. Faculty Advisor ({student['department']})")
                form_timeline = st.selectbox("Target Follow-Up", ["Immediate (3 days)", "Within 7 days", "Next 2 weeks", "End of Semester"])
                form_notes = st.text_input("Initial Notes", value="Initiated from Student Explorer profile review.")

                if st.form_submit_button("Save Intervention to Platform"):
                    add_intervention(
                        student_id=student["student_id"],
                        student_name=student["student_name"],
                        department=student["department"],
                        category=form_cat,
                        priority=form_pri,
                        action=form_action,
                        owner=form_owner,
                        target_timeline=form_timeline,
                        status="In Progress",
                        notes=form_notes,
                    )
                    st.success("Intervention record successfully persisted!")
                    st.rerun()

        with tab_hist:
            student_ints = get_interventions_for_student(student["student_id"])
            if student_ints:
                int_df = pd.DataFrame(student_ints)[["id", "category", "priority", "action", "owner", "status", "notes", "created_at"]]
                st.dataframe(int_df, use_container_width=True, hide_index=True)
            else:
                st.info("No intervention actions have been logged yet for this student.")

    with col_meta2:
        radar_fig = plot_student_radar_subscores(student["subscores"])
        st.plotly_chart(radar_fig, use_container_width=True)

        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 14px; border-radius: 10px; margin-top: 10px;">
                <h5 style="margin: 0 0 8px 0; color: #172033;">Cohort Segment Alignment</h5>
                <p style="font-size: 13px; color: #475467; margin: 0 0 6px 0;">
                    <b>Primary Tag:</b> {student['segment_details']['icon']} {student['primary_segment']}
                </p>
                <p style="font-size: 12px; color: #667085; margin: 0 0 8px 0;">
                    {student['segment_details']['description']}
                </p>
                <div style="background-color: #EEF2FF; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #3B5BDB;">
                    <b>Strategic Goal:</b> {student['segment_details']['recommended_action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
