"""
Smart Campus Analytics & Student Success Platform
Page 6 — Data & Methodology: Transparent Formulas, Thresholds & Validation Report.
"""

import streamlit as st
import pandas as pd

from components.layout import inject_custom_styles, render_page_header
from components.sidebar import render_sidebar
from services.state import get_current_dataset, set_custom_dataset
from services.scoring import DEFAULT_WEIGHTS, SCORE_BANDS

inject_custom_styles()

df_full, validation_report = get_current_dataset()
df_filtered, active_filters = render_sidebar(df_full)

if active_filters.get("uploaded_df") is not None:
    df_full, validation_report = set_custom_dataset(active_filters["uploaded_df"])
    df_filtered, active_filters = render_sidebar(df_full)

render_page_header(
    title="Data, Scoring Methodology & Validation",
    subtitle="Mathematical formulation, dynamic re-normalization, risk thresholds & data integrity checks",
    icon="📐"
)

# Tabbed Methodology Views
t_formula, t_valid, t_risk, t_ethics = st.tabs([
    "🧮 Student Success Score Formula",
    "🛡️ Data Validation & Integrity Report",
    "⚠️ Risk Signals & Thresholds",
    "🔒 Privacy, Ethics & Fairness",
])

with t_formula:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### 1. Student Success Score Formulation")
    st.markdown(
        """
        The **Student Success Score** is a transparent, explainable index ranging from **0.0 to 100.0**.
        Rather than using an opaque black box, it synthesizes indicators across seven verified domains:
        """
    )

    weight_table = [
        {"Category": "Academic Performance", "Base Weight": "30%", "Subscore Formula": "0.5×(CGPA×10) + 0.3×Internal% + 0.2×Subject% − (Backlogs×10 pts)"},
        {"Category": "Classroom Attendance", "Base Weight": "20%", "Subscore Formula": "Direct Attendance Percentage (0–100%)"},
        {"Category": "LMS Coursework & Activity", "Base Weight": "10%", "Subscore Formula": "0.7×Assignment Completion% + 0.3×(Logins/15×100 capped)"},
        {"Category": "Placement Readiness", "Base Weight": "20%", "Subscore Formula": "0.35×Coding% + 0.30×Aptitude% + 0.25×Mock% + 0.10×Resume"},
        {"Category": "Skills & Rubrics", "Base Weight": "10%", "Subscore Formula": "Mean of Technical, Problem Solving & Communication rubrics"},
        {"Category": "Campus Engagement", "Base Weight": "5%", "Subscore Formula": "Events (15 pts) + Clubs/Hackathons (20 pts) + Certifications (25 pts)"},
        {"Category": "Mentor & Pulse Feedback", "Base Weight": "5%", "Subscore Formula": "Normalized 1–5 scale: ((Rating − 1) / 4) × 100"},
    ]
    st.dataframe(pd.DataFrame(weight_table), use_container_width=True, hide_index=True)

    st.markdown("#### Dynamic Weight Re-normalization for Missing / Non-Applicable Data")
    st.markdown(
        r"""
        > **Core Principle:** Missing or non-applicable indicators (e.g. 1st-year students with no placement assessments) **are NEVER treated as zero**.

        For any student with a subset of applicable categories $\mathcal{A}$:
        $$\text{Normalized Weight } w_i' = \frac{w_i}{\sum_{j \in \mathcal{A}} w_j}$$
        $$\text{Success Score} = \sum_{i \in \mathcal{A}} (\text{Subscore}_i \times w_i')$$

        If total available weight is below 35% or critical indicators are unrecorded, the platform safely outputs **Insufficient Data** instead of a misleading numerical score.
        """
    )

    st.markdown("#### Score Interpretation Bands")
    bands_table = [
        {"Score Range": f"{low:.0f} – {high:.0f}", "Classification": label, "Intervention Priority": "Routine Monitoring" if low >= 65 else ("Targeted Support" if low >= 50 else "High Priority Immediate Remediation")}
        for low, high, label, col, cls in SCORE_BANDS
    ]
    st.dataframe(pd.DataFrame(bands_table), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with t_valid:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### 2. Dataset Health & Validation Summary")

    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.write(f"**Total Records Ingested:** {validation_report.get('total_rows', 0)}")
        st.write(f"**Unique Students:** {validation_report.get('unique_students', 0)}")
        st.write(f"**Schema Validation Status:** {'✅ Valid' if validation_report.get('is_valid') else '❌ Invalid'}")

    with v_col2:
        warnings = validation_report.get("warnings", [])
        if warnings:
            st.warning(f"**Validation Warnings ({len(warnings)}):**")
            for w in warnings:
                st.write(f"- {w}")
        else:
            st.success("All data passes integrity and range bounds checks!")

    st.markdown("#### Column-Level Data Completeness")
    col_stats = validation_report.get("column_stats", {})
    if col_stats:
        stats_rows = []
        for col_name, stats in col_stats.items():
            stats_rows.append({
                "Column Header": col_name,
                "Data Type": stats["type"],
                "Missing Values": stats["missing_count"],
                "Coverage (%)": f"{stats['coverage_pct']}%"
            })
        st.dataframe(pd.DataFrame(stats_rows), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

with t_risk:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### 3. Early-Warning Risk Rules & Thresholds")
    st.markdown(
        r"""
        The system separates **Academic Support Need** from **Placement Readiness**:

        #### Academic Support Rules
        - **Critical Attendance:** Attendance $< 65\%$ (Statutory threshold: $75\%$)
        - **Active Backlogs:** $\ge 2$ active backlogs is High Risk; $1$ backlog is Medium Risk
        - **Academic Deficit:** Composite academic subscore $< 40/100$ or CGPA $< 5.0$
        - **Composite Success Score:** Below $50/100$ flags priority review

        #### Placement Readiness Rules (Year 3 & 4)
        - **Coding Proficiency Cut-Off:** Programming score $< 40\%$ is High Risk; $< 50\%$ is Medium Risk
        - **Mock Interview Cut-Off:** Interview performance $< 45\%$ triggers communication review
        - **Aptitude Benchmark:** Aptitude score $< 45\%$ triggers practice module
        - **Resume Verification:** Resume marked unverified / absent
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

with t_ethics:
    st.markdown('<div class="analytics-card">', unsafe_allow_html=True)
    st.markdown("### 4. Responsible AI, Privacy & Ethical Governance")
    st.markdown(
        """
        - **Decision-Support, Not Determinism:** Scores and risk flags are transparent signals to guide faculty mentorship and supportive conversations, not automated penalties.
        - **No Irrelevant Personal Attributes:** Protected traits (gender, caste, religion, socioeconomic background) are explicitly excluded from data ingestion and scoring algorithms.
        - **Human-in-the-Loop:** Every recommendation must be validated and owned by a faculty proctor, mentor, or placement coordinator.
        - **Synthetic Demonstration Notice:** All data utilized in this demonstration is 100% synthetically generated and does not represent real students.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)
