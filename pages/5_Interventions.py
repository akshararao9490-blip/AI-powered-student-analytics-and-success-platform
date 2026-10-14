"""
Smart Campus Analytics & Student Success Platform
Page 5 — Intervention Action Center & Follow-Up Tracking.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from components.metric_cards import render_metric_card
from services.state import get_current_dataset, set_custom_dataset
from services.intervention_tracker import (
    get_all_interventions,
    add_intervention,
    update_intervention,
)

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Intervention Action Center & Tracking",
    subtitle="Log, assign, update, and track closing-the-loop student support interventions",
    icon="📋"
)

# Fetch persisted interventions from SQLite
all_ints = get_all_interventions()
ints_df = pd.DataFrame(all_ints) if all_ints else pd.DataFrame()

# Intervention KPIs
total_ints = len(ints_df)
in_progress_count = len(ints_df[ints_df["status"] == "In Progress"]) if not ints_df.empty else 0
completed_count = len(ints_df[ints_df["status"] == "Completed"]) if not ints_df.empty else 0
planned_count = len(ints_df[ints_df["status"] == "Planned"]) if not ints_df.empty else 0

ic1, ic2, ic3, ic4 = st.columns(4)
with ic1:
    render_metric_card("Tracked Interventions", f"{total_ints}", "Persisted in SQLite database")
with ic2:
    render_metric_card("In Progress", f"{in_progress_count}", "Active support engagements", color_accent="#B54708", border_accent="#B54708")
with ic3:
    render_metric_card("Completed Actions", f"{completed_count}", "Successfully resolved", color_accent="#16803C", border_accent="#16803C")
with ic4:
    render_metric_card("Planned / Pending", f"{planned_count}", "Scheduled next steps", color_accent="#3B5BDB", border_accent="#3B5BDB")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Main Interventions Workflow
col_roster, col_actions = st.columns([1.5, 1])

with col_roster:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📂 Active Intervention Log</div>', unsafe_allow_html=True)

    if not ints_df.empty:
        # Filter by status
        status_filter = st.radio(
            "Filter Status:",
            options=["All", "In Progress", "Planned", "Completed", "Cancelled"],
            horizontal=True
        )

        filtered_ints = ints_df if status_filter == "All" else ints_df[ints_df["status"] == status_filter]

        st.write(f"Showing **{len(filtered_ints)}** interventions:")
        display_cols = ["id", "student_id", "student_name", "department", "category", "priority", "status", "owner", "target_timeline", "notes", "updated_at"]
        st.dataframe(filtered_ints[display_cols], use_container_width=True, hide_index=True)
    else:
        st.info("No intervention records tracked yet. Use the form on the right to log an intervention.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_actions:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✏️ Update Existing Intervention</div>', unsafe_allow_html=True)

    if not ints_df.empty:
        int_options = [f"#{row['id']} — {row['student_id']} ({row['category']} - {row['status']})" for _, row in ints_df.iterrows()]
        selected_int_label = st.selectbox("Select Record to Update:", int_options)
        selected_id = int(selected_int_label.split(" — ")[0].replace("#", ""))

        target_row = ints_df[ints_df["id"] == selected_id].iloc[0]

        with st.form(f"update_form_{selected_id}"):
            st.write(f"**Student:** {target_row['student_name']} ({target_row['student_id']})")
            st.write(f"**Action:** {target_row['action']}")

            new_status = st.selectbox("Update Status:", ["Planned", "In Progress", "Completed", "Cancelled"], index=["Planned", "In Progress", "Completed", "Cancelled"].index(target_row["status"]))
            new_notes = st.text_area("Progress / Closing Notes:", value=target_row.get("notes") or "")
            new_owner = st.text_input("Assigned Owner:", value=target_row.get("owner") or "")

            if st.form_submit_button("Save Updates"):
                update_intervention(selected_id, status=new_status, notes=new_notes, owner=new_owner)
                st.success("Intervention record updated successfully!")
                st.rerun()
    else:
        st.info("Create a record first to enable updates.")

    st.markdown('</div>', unsafe_allow_html=True)

# Add New Intervention Panel
st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">➕ Log New Student Intervention</div>', unsafe_allow_html=True)

with st.form("new_intervention_page_form"):
    c1, c2, c3 = st.columns(3)

    student_choices = [f"{r['student_id']} - {r['student_name']} ({r['department']})" for _, r in df_filtered.iterrows()]

    with c1:
        chosen_student = st.selectbox("Target Student:", options=student_choices if student_choices else ["None"])
    with c2:
        new_cat = st.selectbox("Category:", [
            "Academic Remediation", "Attendance Counseling", "Placement Technical Training",
            "Interview Coaching", "Quantitative Aptitude", "General Mentorship", "Career Profile Preparation"
        ])
    with c3:
        new_pri = st.selectbox("Priority:", ["High", "Medium", "Low"])

    c4, c5 = st.columns(2)
    with c4:
        new_owner = st.text_input("Responsible Faculty / Mentor:", value="Class Proctor / Academic Mentor")
    with c5:
        new_timeline = st.selectbox("Target Timeline:", ["Immediate (3 days)", "Within 7 days", "Next 2 weeks", "End of Semester"])

    new_action = st.text_area("Action Description:", placeholder="Specify constructive remediation steps...")
    new_notes = st.text_input("Initial Context / Notes:", placeholder="Reason for intervention...")

    if st.form_submit_button("Create and Assign Intervention"):
        if chosen_student != "None" and new_action.strip():
            stu_id = chosen_student.split(" - ")[0].strip()
            matched_rec = df_filtered[df_filtered["student_id"] == stu_id].iloc[0]
            add_intervention(
                student_id=stu_id,
                student_name=matched_rec["student_name"],
                department=matched_rec["department"],
                category=new_cat,
                priority=new_pri,
                action=new_action,
                owner=new_owner,
                target_timeline=new_timeline,
                status="Planned",
                notes=new_notes,
            )
            st.success(f"Intervention created for {matched_rec['student_name']} ({stu_id})!")
            st.rerun()
        else:
            st.error("Please provide both a student selection and an action description.")

st.markdown('</div>', unsafe_allow_html=True)
