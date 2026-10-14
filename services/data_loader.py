"""
Smart Campus Analytics & Student Success Platform
Data Loader Service — Ingests, merges, cleans, and augments student datasets.
"""

import os
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np

from services.scoring import compute_student_success_score
from services.risk_rules import evaluate_student_risks
from services.segmentation import assign_student_segments
from services.recommendations import generate_recommendations
from services.data_validation import validate_student_dataset

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SAMPLE_CSV_PATH = os.path.join(DATA_DIR, "sample_students.csv")


def get_default_dataset_path() -> str:
    """Returns absolute path to sample dataset."""
    return SAMPLE_CSV_PATH


def load_raw_csv(filepath_or_buffer) -> pd.DataFrame:
    """Loads CSV file with normalized column headers."""
    df = pd.read_csv(filepath_or_buffer)
    # Strip whitespace from string columns and column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def merge_category_dataframes(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """Merges multiple category dataframes on student_id using outer join."""
    if not dfs:
        return pd.DataFrame()
    merged = dfs[0]
    for nxt in dfs[1:]:
        if "student_id" in merged.columns and "student_id" in nxt.columns:
            merged = pd.merge(merged, nxt, on="student_id", how="outer", suffixes=("", "_duplicate"))
        else:
            raise ValueError("All data sources must contain 'student_id' column to join.")
    return merged


def process_and_augment_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Validates and enriches the student dataframe with Student Success Scores,
    academic risk, placement readiness, segmentation, and recommendations.
    """
    validation_report = validate_student_dataset(df)
    if not validation_report["is_valid"]:
        return df, validation_report

    # Remove duplicate student_id keeping first
    clean_df = df.drop_duplicates(subset=["student_id"]).copy()

    records = clean_df.to_dict(orient="records")
    augmented_rows = []

    for row in records:
        success_info = compute_student_success_score(row)
        risk_info = evaluate_student_risks(row, success_info)
        segment_info = assign_student_segments(row, success_info, risk_info)
        recs = generate_recommendations(row, success_info, risk_info, segment_info)

        row_copy = dict(row)
        row_copy["success_score"] = success_info["score"]
        row_copy["score_band"] = success_info["band"]
        row_copy["band_color"] = success_info["band_color"]
        row_copy["data_coverage_pct"] = success_info["coverage_pct"]
        row_copy["is_sufficient"] = success_info["is_sufficient"]
        row_copy["score_explanation"] = success_info["explanation"]
        row_copy["positive_drivers"] = success_info["positive_drivers"]
        row_copy["risk_drivers"] = success_info["risk_drivers"]
        row_copy["subscores"] = success_info["subscores"]
        row_copy["normalized_weights"] = success_info["normalized_weights"]

        # Risk info
        row_copy["academic_risk_level"] = risk_info["academic_risk"]["level"]
        row_copy["academic_risk_color"] = risk_info["academic_risk"]["color"]
        row_copy["academic_risk_reasons"] = risk_info["academic_risk"]["reasons"]

        row_copy["placement_risk_level"] = risk_info["placement_risk"]["level"]
        row_copy["placement_risk_color"] = risk_info["placement_risk"]["color"]
        row_copy["placement_risk_reasons"] = risk_info["placement_risk"]["reasons"]

        # Segments & Recommendations
        row_copy["primary_segment"] = segment_info["primary_segment"]
        row_copy["all_segments"] = segment_info["all_segments"]
        row_copy["segment_details"] = segment_info["details"]
        row_copy["recommendations"] = recs

        # Formatted fields for display
        score_val = row_copy["success_score"]
        row_copy["display_score"] = f"{score_val:.1f}" if score_val is not None else "N/A"

        augmented_rows.append(row_copy)

    augmented_df = pd.DataFrame(augmented_rows)
    return augmented_df, validation_report
