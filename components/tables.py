"""
Smart Campus Analytics & Student Success Platform
Tables Component — Styled student listings and profile displays.
"""

from typing import Dict, Any, Optional
import streamlit as st
import pandas as pd


def render_student_summary_table(df: pd.DataFrame, max_rows: int = 50) -> Optional[str]:
    """
    Renders styled student table with search, key metrics, and returns selected student_id.
    """
    if df.empty:
        st.info("No student records match the selected filters.")
        return None

    # Search bar
    search_query = st.text_input(
        "🔎 Search Student by ID or Name:",
        placeholder="Type student ID (e.g. STU-2026-004) or Name...",
        key="table_search_input"
    ).strip().lower()

    display_df = df.copy()
    if search_query:
        mask = (
            display_df["student_id"].str.lower().str.contains(search_query, na=False) |
            display_df["student_name"].str.lower().str.contains(search_query, na=False)
        )
        display_df = display_df[mask]

    st.write(f"Showing **{min(len(display_df), max_rows)}** of **{len(display_df)}** matching students:")

    # Select columns to display
    cols_to_show = [
        "student_id",
        "student_name",
        "department",
        "academic_year",
        "cgpa",
        "attendance_pct",
        "backlog_count",
        "success_score",
        "academic_risk_level",
        "placement_risk_level",
        "primary_segment",
    ]

    available_cols = [c for c in cols_to_show if c in display_df.columns]
    table_subset = display_df[available_cols].head(max_rows).copy()

    # Rename for cleaner table headers
    renames = {
        "student_id": "Student ID",
        "student_name": "Name",
        "department": "Department",
        "academic_year": "Year",
        "cgpa": "CGPA",
        "attendance_pct": "Att %",
        "backlog_count": "Backlogs",
        "success_score": "Score (0-100)",
        "academic_risk_level": "Academic Risk",
        "placement_risk_level": "Placement Status",
        "primary_segment": "Segment",
    }
    table_subset.rename(columns=renames, inplace=True)

    # Streamlit dataframe with interactive styling
    st.dataframe(
        table_subset,
        use_container_width=True,
        hide_index=True,
    )

    # Student selector for deep dive
    student_options = ["-- Select a student to inspect full profile --"] + [
        f"{r['student_id']} - {r['student_name']} ({r['department']})"
        for _, r in display_df.head(max_rows).iterrows()
    ]

    selected_choice = st.selectbox(
        "Select student profile for explainable breakdown:",
        options=student_options,
        index=0,
        key="student_picker_select"
    )

    if selected_choice != student_options[0]:
        selected_id = selected_choice.split(" - ")[0].strip()
        return selected_id

    return None
