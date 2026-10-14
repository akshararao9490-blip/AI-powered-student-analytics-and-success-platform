"""
Smart Campus Analytics & Student Success Platform
Page 4 — Student Segmentation & Targeted Cohort Interventions.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.charts import plot_segments_bar
from services.state import get_current_dataset, set_custom_dataset
from services.segmentation import SEGMENT_DEFINITIONS

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Student Cohort Segmentation",
    subtitle="Rule-based behavioral clustering to deliver targeted, differentiated campus interventions",
    icon="🎯"
)

# Segment Distribution Chart & Summary
col_bar, col_card = st.columns([1.3, 1])

with col_bar:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.plotly_chart(plot_segments_bar(df_filtered), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_card:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Why Segmentation Matters</div>', unsafe_allow_html=True)
    st.markdown(
        """
        One-size-fits-all academic interventions fail because students have divergent needs:
        - **High CGPA but Low Placement:** Needs algorithmic bootcamps, not remedial theory.
        - **Attendance Shortage:** Needs proctor counseling & personal support, not extra tests.
        - **Academic Recovery:** Needs subject faculty tutoring and backlog clearing roadmaps.
        - **Well-Rounded:** Needs research grants, leadership roles, and honors mentorship.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Segment Deep-Dive Section
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 Segment Drill-Down & Roster</div>', unsafe_allow_html=True)

all_seg_names = list(SEGMENT_DEFINITIONS.keys())
selected_seg = st.selectbox(
    "Choose Segment to Inspect:",
    options=all_seg_names,
    index=0
)

seg_meta = SEGMENT_DEFINITIONS.get(selected_seg, {})
seg_students = df_filtered[df_filtered["primary_segment"] == selected_seg]

st.markdown(
    f"""
    <div style="background-color: #F8FAFC; border-left: 4px solid {seg_meta.get('color', '#3B5BDB')}; padding: 16px; border-radius: 0 10px 10px 0; margin-bottom: 20px;">
        <h4 style="margin: 0 0 6px 0; color: #172033;">{seg_meta.get('icon', '📌')} {selected_seg} ({len(seg_students)} students)</h4>
        <p style="color: #475467; font-size: 14px; margin: 0 0 10px 0;">{seg_meta.get('description', '')}</p>
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 6px; font-size: 13px;">
            <b>Institutional Action Strategy:</b> {seg_meta.get('recommended_action', '')}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not seg_students.empty:
    # Summary metrics for this segment
    sm1, sm2, sm3, sm4 = st.columns(4)
    sm1.metric("Students in Segment", f"{len(seg_students)}")
    sm2.metric("Average CGPA", f"{pd.to_numeric(seg_students['cgpa'], errors='coerce').mean():.2f}")
    sm3.metric("Average Attendance", f"{pd.to_numeric(seg_students['attendance_pct'], errors='coerce').mean():.1f}%")
    sm4.metric("Avg Success Score", f"{seg_students['success_score'].dropna().mean():.1f}/100")

    st.markdown("##### 📋 Student Roster in this Segment")
    roster_display = seg_students[[
        "student_id", "student_name", "department", "academic_year",
        "cgpa", "attendance_pct", "backlog_count", "success_score",
        "academic_risk_level", "placement_risk_level"
    ]].copy()

    roster_display.columns = [
        "Student ID", "Name", "Department", "Year",
        "CGPA", "Attendance %", "Backlogs", "Score",
        "Academic Risk", "Placement Status"
    ]
    st.dataframe(roster_display, use_container_width=True, hide_index=True)
else:
    st.info(f"No students in the current filtered cohort belong to '{selected_seg}'.")

st.markdown('</div>', unsafe_allow_html=True)
