"""
Unit tests for student segmentation service.
"""

from services.scoring import compute_student_success_score
from services.risk_rules import evaluate_student_risks
from services.segmentation import assign_student_segments


def test_segment_strong_academics_low_placement():
    record = {
        "student_id": "TEST-01",
        "cgpa": 9.2,
        "internal_marks_pct": 88.0,
        "attendance_pct": 90.0,
        "academic_year": 4,
        "coding_score_pct": 35.0,
        "mock_interview_pct": 42.0,
        "aptitude_score_pct": 45.0,
        "resume_ready": "No",
    }
    score_info = compute_student_success_score(record)
    risk_info = evaluate_student_risks(record, score_info)
    seg_info = assign_student_segments(record, score_info, risk_info)
    assert seg_info["primary_segment"] == "Strong Academics, Low Placement Readiness"


def test_segment_attendance_support():
    record = {
        "student_id": "TEST-02",
        "cgpa": 7.5,
        "internal_marks_pct": 75.0,
        "attendance_pct": 68.0,
        "academic_year": 2,
    }
    score_info = compute_student_success_score(record)
    risk_info = evaluate_student_risks(record, score_info)
    seg_info = assign_student_segments(record, score_info, risk_info)
    assert seg_info["primary_segment"] == "Attendance Support Needed"


def test_segment_academic_recovery():
    record = {
        "student_id": "TEST-03",
        "cgpa": 5.2,
        "internal_marks_pct": 44.0,
        "backlog_count": 2,
        "attendance_pct": 80.0,
    }
    score_info = compute_student_success_score(record)
    risk_info = evaluate_student_risks(record, score_info)
    seg_info = assign_student_segments(record, score_info, risk_info)
    assert seg_info["primary_segment"] == "Academic Recovery"
