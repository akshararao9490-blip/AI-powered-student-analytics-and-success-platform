"""
Unit tests for scoring service.
"""

import pytest
from services.scoring import (
    clamp,
    calculate_academic_subscore,
    calculate_attendance_subscore,
    calculate_lms_subscore,
    calculate_placement_subscore,
    calculate_skills_subscore,
    calculate_engagement_subscore,
    calculate_feedback_subscore,
    compute_student_success_score,
)


def test_clamp():
    assert clamp(-10) == 0.0
    assert clamp(150) == 100.0
    assert clamp(55.5) == 55.5


def test_academic_subscore_standard():
    record = {
        "cgpa": 8.0,
        "internal_marks_pct": 80.0,
        "backlog_count": 0,
        "subject_performance_pct": 80.0,
    }
    score = calculate_academic_subscore(record)
    assert score is not None
    assert 79.0 <= score <= 81.0


def test_academic_subscore_with_backlog_penalty():
    record = {
        "cgpa": 8.0,
        "internal_marks_pct": 80.0,
        "backlog_count": 2,
    }
    # Base is 80, minus 20 penalty = 60
    score = calculate_academic_subscore(record)
    assert score is not None
    assert 59.0 <= score <= 61.0


def test_attendance_subscore():
    assert calculate_attendance_subscore({"attendance_pct": 92.5}) == 92.5
    assert calculate_attendance_subscore({"attendance_pct": None}) is None


def test_placement_subscore_none_for_missing():
    record = {
        "aptitude_score_pct": None,
        "coding_score_pct": None,
        "mock_interview_pct": None,
        "resume_ready": None,
    }
    assert calculate_placement_subscore(record) is None


def test_compute_student_success_score_renormalization():
    # Student with placement missing (e.g. Year 1)
    record = {
        "cgpa": 8.0,
        "internal_marks_pct": 80.0,
        "attendance_pct": 90.0,
        "lms_logins_per_week": 10.0,
        "assignment_completion_pct": 85.0,
        "technical_skill_pct": 75.0,
        "communication_skill_pct": 75.0,
        "problem_solving_pct": 75.0,
        "events_participated": 2,
        "clubs_or_hackathons": 1,
        "certifications_count": 1,
        "student_feedback_score": 4.0,
        "faculty_feedback_score": 4.0,
        # Placement is missing:
        "aptitude_score_pct": None,
        "coding_score_pct": None,
        "mock_interview_pct": None,
        "resume_ready": None,
    }
    result = compute_student_success_score(record)
    assert result["is_sufficient"] is True
    assert result["score"] is not None
    assert 0.0 <= result["score"] <= 100.0
    # Normalized weights must sum to 1.0
    assert abs(sum(result["normalized_weights"].values()) - 1.0) < 0.01
    assert "placement" not in result["normalized_weights"]


def test_insufficient_data():
    record = {
        "student_id": "EMPTY-001",
        "cgpa": None,
        "attendance_pct": None,
    }
    result = compute_student_success_score(record)
    assert result["is_sufficient"] is False
    assert result["score"] is None
    assert result["band"] == "Insufficient Data"
