"""
Unit tests for data validation service.
"""

import pandas as pd
from services.data_validation import validate_student_dataset


def test_empty_dataframe():
    df = pd.DataFrame()
    res = validate_student_dataset(df)
    assert res["is_valid"] is False
    assert "empty" in res["errors"][0].lower()


def test_missing_student_id():
    df = pd.DataFrame({"cgpa": [8.0, 7.5]})
    res = validate_student_dataset(df)
    assert res["is_valid"] is False
    assert any("student_id" in err for err in res["errors"])


def test_valid_dataframe():
    df = pd.DataFrame({
        "student_id": ["STU-01", "STU-02"],
        "cgpa": [8.2, 7.1],
        "attendance_pct": [90.0, 85.0],
    })
    res = validate_student_dataset(df)
    assert res["is_valid"] is True
    assert res["total_rows"] == 2
    assert res["unique_students"] == 2


def test_duplicate_student_id():
    df = pd.DataFrame({
        "student_id": ["STU-01", "STU-01"],
        "cgpa": [8.2, 7.1],
    })
    res = validate_student_dataset(df)
    assert res["is_valid"] is True
    assert any("duplicate" in w.lower() for w in res["warnings"])
