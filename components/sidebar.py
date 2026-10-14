"""
Smart Campus Analytics & Student Success Platform
Sidebar Component — Global cohort filters, data source switcher, and user role toggle.
"""

from typing import Tuple, Dict, Any
import streamlit as st
import pandas as pd

from services.data_loader import (
    load_raw_csv,
    process_and_augment_dataset,
    get_default_dataset_path
)


def render_sidebar(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Renders global sidebar filters and controls.
    Returns: (filtered_dataframe, active_filters_dict)
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #E4E7EC; margin-bottom: 16px;">
                <h3 style="margin: 0; color: #172033; font-size: 18px; font-weight: 700;">Smart Campus</h3>
                <span style="font-size: 12px; color: #667085; font-weight: 500;">KPMG Hackathon Platform</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Role Selector
        st.selectbox(
            "Viewing As Role:",
            options=["Institutional Administrator", "Faculty / Mentor", "Placement Coordinator"],
            index=0,
            key="user_role",
            help="Tailors view emphasis and default prioritization."
        )

        st.markdown("---")
        st.markdown("#### 🔍 Global Cohort Filters")

        # Department Filter
        all_depts = sorted([d for d in df_raw["department"].dropna().unique() if str(d).strip()])
        selected_depts = st.multiselect(
            "Department / Branch",
            options=all_depts,
            default=[],
            placeholder="All Departments",
            key="filter_dept"
        )

        # Academic Year Filter
        all_years = sorted([int(y) for y in df_raw["academic_year"].dropna().unique() if str(y).isdigit()])
        selected_years = st.multiselect(
            "Academic Year",
            options=all_years,
            default=[],
            format_func=lambda y: f"Year {y}",
            placeholder="All Years",
            key="filter_year"
        )

        # Academic Risk Filter
        all_risks = ["High", "Medium", "Low", "Insufficient Data"]
        selected_risks = st.multiselect(
            "Academic Risk Level",
            options=all_risks,
            default=[],
            placeholder="All Risk Levels",
            key="filter_risk"
        )

        # Placement Readiness Filter
        all_placement_levels = ["Placement Ready", "High", "Medium", "N/A (Year 1)", "N/A (Pending)"]
        selected_placement = st.multiselect(
            "Placement Readiness",
            options=all_placement_levels,
            default=[],
            placeholder="All Placement Statuses",
            key="filter_placement"
        )

        # Student Segment Filter
        all_segments = sorted(list(df_raw["primary_segment"].dropna().unique()))
        selected_segments = st.multiselect(
            "Student Segment",
            options=all_segments,
            default=[],
            placeholder="All Segments",
            key="filter_segment"
        )

        # Filter reset button
        if st.button("Reset All Filters", use_container_width=True):
            st.session_state["filter_dept"] = []
            st.session_state["filter_year"] = []
            st.session_state["filter_risk"] = []
            st.session_state["filter_placement"] = []
            st.session_state["filter_segment"] = []
            st.rerun()

        st.markdown("---")
        st.markdown("#### 📁 Data Source")

        use_upload = st.checkbox("Upload Custom CSV", value=False, key="use_upload_csv")
        uploaded_df = None

        if use_upload:
            uploaded_file = st.file_uploader(
                "Upload Student CSV",
                type=["csv"],
                help="Accepts unified CSV matching data schema."
            )
            if uploaded_file is not None:
                try:
                    uploaded_df = load_raw_csv(uploaded_file)
                    st.success("Custom CSV uploaded!")
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")

        # Download Sample Template
        with open(get_default_dataset_path(), "rb") as f:
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=f,
                file_name="sample_students_template.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.caption("Big Busters • HacXLerate 2026")

    # Apply filters to df_raw
    filtered_df = df_raw.copy()

    if selected_depts:
        filtered_df = filtered_df[filtered_df["department"].isin(selected_depts)]
    if selected_years:
        filtered_df = filtered_df[filtered_df["academic_year"].isin(selected_years)]
    if selected_risks:
        filtered_df = filtered_df[filtered_df["academic_risk_level"].isin(selected_risks)]
    if selected_placement:
        filtered_df = filtered_df[filtered_df["placement_risk_level"].isin(selected_placement)]
    if selected_segments:
        filtered_df = filtered_df[filtered_df["primary_segment"].isin(selected_segments)]

    active_filters = {
        "departments": selected_depts,
        "years": selected_years,
        "academic_risks": selected_risks,
        "placement_levels": selected_placement,
        "segments": selected_segments,
        "uploaded_df": uploaded_df,
    }

    return filtered_df, active_filters
