"""
Smart Campus Analytics & Student Success Platform
Data Validation Service — Validates schema, data types, ranges, duplicates, and coverage.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


EXPECTED_RANGES = {
    "cgpa": (0.0, 10.0),
    "internal_marks_pct": (0.0, 100.0),
    "subject_performance_pct": (0.0, 100.0),
    "backlog_count": (0, 50),
    "attendance_pct": (0.0, 100.0),
    "lms_logins_per_week": (0.0, 100.0),
    "assignment_completion_pct": (0.0, 100.0),
    "events_participated": (0, 100),
    "clubs_or_hackathons": (0, 50),
    "certifications_count": (0, 50),
    "aptitude_score_pct": (0.0, 100.0),
    "coding_score_pct": (0.0, 100.0),
    "mock_interview_pct": (0.0, 100.0),
    "technical_skill_pct": (0.0, 100.0),
    "communication_skill_pct": (0.0, 100.0),
    "problem_solving_pct": (0.0, 100.0),
    "student_feedback_score": (1.0, 5.0),
    "faculty_feedback_score": (1.0, 5.0),
}


def validate_student_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates a student dataframe against schema integrity rules.
    Returns validation status, errors, warnings, and column statistics.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if df.empty:
        return {
            "is_valid": False,
            "errors": ["Dataset is empty. No student records found."],
            "warnings": [],
            "total_rows": 0,
            "column_stats": {},
        }

    # 1. Required Key Check
    if "student_id" not in df.columns:
        errors.append("Missing required primary key column: 'student_id'.")
        return {
            "is_valid": False,
            "errors": errors,
            "warnings": warnings,
            "total_rows": len(df),
            "column_stats": {},
        }

    total_rows = len(df)

    # 2. Check Duplicate student_id
    duplicate_count = df["student_id"].duplicated().sum()
    if duplicate_count > 0:
        duplicates = df[df["student_id"].duplicated()]["student_id"].unique()[:5].tolist()
        warnings.append(
            f"Found {duplicate_count} duplicate student_id records (e.g., {duplicates}). "
            f"Keeping first occurrence for analytics."
        )

    # 3. Check Range Violations for Numeric Columns
    for col, (min_val, max_val) in EXPECTED_RANGES.items():
        if col in df.columns:
            # Convert to numeric safely
            numeric_vals = pd.to_numeric(df[col], errors="coerce").dropna()
            out_of_bounds = numeric_vals[(numeric_vals < min_val) | (numeric_vals > max_val)]
            if len(out_of_bounds) > 0:
                warnings.append(
                    f"Column '{col}' contains {len(out_of_bounds)} values outside expected range "
                    f"[{min_val}, {max_val}]. These will be safely clamped during scoring."
                )

    # 4. Check Key Demographic Columns
    for optional_col in ["department", "academic_year", "semester"]:
        if optional_col not in df.columns:
            warnings.append(f"Optional cohort column '{optional_col}' is missing; cohort filters will be limited.")

    # 5. Missing Value Statistics
    column_stats: Dict[str, Dict[str, Any]] = {}
    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        missing_pct = round((missing_count / total_rows) * 100.0, 1)
        column_stats[col] = {
            "type": str(df[col].dtype),
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "coverage_pct": round(100.0 - missing_pct, 1),
        }

    # Critical columns check
    critical_cols = ["cgpa", "attendance_pct"]
    for c in critical_cols:
        if c in df.columns and column_stats[c]["missing_pct"] > 40.0:
            warnings.append(
                f"Column '{c}' has high missing rate ({column_stats[c]['missing_pct']}%), "
                "which may increase the proportion of 'Insufficient Data' students."
            )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "total_rows": total_rows,
        "unique_students": int(df["student_id"].nunique()),
        "column_stats": column_stats,
    }
