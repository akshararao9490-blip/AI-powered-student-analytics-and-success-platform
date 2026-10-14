"""
Smart Campus Analytics & Student Success Platform
State Management Service — Centralized data loader and session state cache.
"""

import os
import streamlit as st
import pandas as pd
from typing import Tuple, Dict, Any

from services.data_loader import (
    load_raw_csv,
    process_and_augment_dataset,
    get_default_dataset_path
)
from services.intervention_tracker import seed_demo_interventions_if_empty


def get_current_dataset() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Retrieves or initializes the active dataset in Streamlit session state.
    """
    if "dataset" not in st.session_state or st.session_state["dataset"] is None:
        csv_path = get_default_dataset_path()
        df_raw = load_raw_csv(csv_path)
        augmented_df, validation_report = process_and_augment_dataset(df_raw)
        st.session_state["dataset"] = augmented_df
        st.session_state["validation_report"] = validation_report
        st.session_state["is_custom_data"] = False

        # Seed initial demo interventions
        seed_demo_interventions_if_empty(augmented_df.to_dict(orient="records"))

    return st.session_state["dataset"], st.session_state.get("validation_report", {})


def set_custom_dataset(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Updates session state with newly uploaded dataset."""
    augmented_df, validation_report = process_and_augment_dataset(df_raw)
    st.session_state["dataset"] = augmented_df
    st.session_state["validation_report"] = validation_report
    st.session_state["is_custom_data"] = True
    return augmented_df, validation_report


def reset_to_sample_dataset() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Resets session state to the bundled synthetic demo dataset."""
    csv_path = get_default_dataset_path()
    df_raw = load_raw_csv(csv_path)
    augmented_df, validation_report = process_and_augment_dataset(df_raw)
    st.session_state["dataset"] = augmented_df
    st.session_state["validation_report"] = validation_report
    st.session_state["is_custom_data"] = False
    return augmented_df, validation_report
