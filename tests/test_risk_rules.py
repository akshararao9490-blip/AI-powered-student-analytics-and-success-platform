"""
Unit tests for risk evaluation rules.
"""

from services.scoring import compute_student_success_score
from services.risk_rules import evaluate_academic_risk, evaluate_placement_risk


def test_academic_risk_high_attendance_deficit():
    record = {
        "attendance_pct": 58.0,
        "cgpa": 6.5,
        "internal_marks_pct": 65.0,
        "backlog_count": 0,
    }
    score_info = compute_student_success_score(record)
    risk = evaluate_academic_risk(record, score_info)
    assert risk["level"] == "High"
    assert any("attendance" in r.lower() for r in risk["reasons"])


def test_academic_risk_backlog_trigger():
    record = {
        "attendance_pct": 82.0,
        "cgpa": 5.5,
        "internal_marks_pct": 52.0,
        "backlog_count": 2,
    }
    score_info = compute_student_success_score(record)
    risk = evaluate_academic_risk(record, score_info)
    assert risk["level"] == "High"
    assert any("backlog" in r.lower() for r in risk["reasons"])


def test_placement_risk_na_year_1():
    record = {
        "academic_year": 1,
        "coding_score_pct": 35.0,
    }
    score_info = compute_student_success_score(record)
    risk = evaluate_placement_risk(record, score_info)
    assert "N/A" in risk["level"]
    assert risk["is_applicable"] is False


def test_placement_risk_low_coding():
    record = {
        "academic_year": 4,
        "coding_score_pct": 32.0,
        "mock_interview_pct": 40.0,
        "aptitude_score_pct": 55.0,
        "resume_ready": "Yes",
    }
    score_info = compute_student_success_score(record)
    risk = evaluate_placement_risk(record, score_info)
    assert risk["level"] == "High"
    assert any("coding" in r.lower() for r in risk["reasons"])
