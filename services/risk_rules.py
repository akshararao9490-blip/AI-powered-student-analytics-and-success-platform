"""
Smart Campus Analytics & Student Success Platform
Risk Rules Service — Evaluates transparent Academic Risk and Placement Readiness.
"""

from typing import Dict, Any, List, Optional
from services.scoring import to_float


def evaluate_academic_risk(student_record: Dict[str, Any], success_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates academic risk based on attendance, academic subscore, backlogs, and success score.
    Returns risk level (High, Medium, Low, Insufficient data), specific trigger reasons, and badge metadata.
    """
    if not success_info.get("is_sufficient", True):
        return {
            "level": "Insufficient Data",
            "color": "#667085",
            "badge_class": "badge-neutral",
            "reasons": ["Insufficient academic data to evaluate risk."],
            "signal_count": 0,
            "critical_signal": False,
        }

    reasons: List[str] = []
    critical = False

    # 1. Attendance check
    att = to_float(student_record.get("attendance_pct"))
    if att is not None:
        if att < 65.0:
            reasons.append(f"Severe attendance shortage ({att:.1f}% < 65%)")
            critical = True
        elif att < 75.0:
            reasons.append(f"Low attendance ({att:.1f}% < 75% statutory minimum)")

    # 2. Backlogs check
    backlogs = to_float(student_record.get("backlog_count"), 0.0)
    if backlogs >= 2:
        reasons.append(f"Multiple active backlogs ({int(backlogs)} subjects)")
        critical = True
    elif backlogs == 1:
        reasons.append("1 active backlog pending clearance")

    # 3. Academic performance subscore
    acad_sub = success_info.get("subscores", {}).get("academic")
    if acad_sub is not None:
        if acad_sub < 40.0:
            reasons.append(f"Critical academic performance deficit ({acad_sub:.1f}/100)")
            critical = True
        elif acad_sub < 50.0:
            reasons.append(f"Academic subscore below benchmark ({acad_sub:.1f}/100)")

    # 4. Overall Success Score check
    score = success_info.get("score")
    if score is not None:
        if score < 45.0:
            reasons.append(f"Overall success score in priority intervention zone ({score:.1f}/100)")
            critical = True
        elif score < 55.0:
            reasons.append(f"Overall success score below target ({score:.1f}/100)")

    # Determine risk level
    signal_count = len(reasons)
    if critical or signal_count >= 2:
        level = "High"
        color = "#B42318"
        badge_class = "badge-danger"
    elif signal_count == 1:
        level = "Medium"
        color = "#B54708"
        badge_class = "badge-warning"
    else:
        level = "Low"
        color = "#16803C"
        badge_class = "badge-success"
        reasons = ["Good academic standing; meets attendance and grade benchmarks."]

    return {
        "level": level,
        "color": color,
        "badge_class": badge_class,
        "reasons": reasons,
        "signal_count": signal_count,
        "critical_signal": critical,
    }


def evaluate_placement_risk(student_record: Dict[str, Any], success_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates placement readiness and risk. Returns N/A for early years or when assessments are not applicable.
    """
    year = to_float(student_record.get("academic_year"))
    # If explicitly year 1, placement is not applicable
    if year == 1:
        return {
            "level": "N/A (Year 1)",
            "color": "#667085",
            "badge_class": "badge-neutral",
            "reasons": ["Placement assessments commence in pre-final and final years."],
            "is_applicable": False,
            "signal_count": 0,
        }

    apt = to_float(student_record.get("aptitude_score_pct"))
    coding = to_float(student_record.get("coding_score_pct"))
    mock = to_float(student_record.get("mock_interview_pct"))
    resume = student_record.get("resume_ready")

    # If all placement data is missing, mark N/A
    if apt is None and coding is None and mock is None and resume is None:
        return {
            "level": "N/A (Pending)",
            "color": "#667085",
            "badge_class": "badge-neutral",
            "reasons": ["Placement evaluation metrics have not yet been recorded for this student."],
            "is_applicable": False,
            "signal_count": 0,
        }

    reasons: List[str] = []
    strengths: List[str] = []
    critical = False

    # Coding check
    if coding is not None:
        if coding < 40.0:
            reasons.append(f"Low coding proficiency score ({coding:.1f}% < 40%)")
            critical = True
        elif coding < 50.0:
            reasons.append(f"Coding score below placement cut-off ({coding:.1f}%)")
        elif coding >= 75.0:
            strengths.append(f"Strong coding proficiency ({coding:.1f}%)")

    # Mock Interview check
    if mock is not None:
        if mock < 45.0:
            reasons.append(f"Mock interview performance below benchmark ({mock:.1f}%)")
            critical = True
        elif mock < 55.0:
            reasons.append(f"Interview communication needs practice ({mock:.1f}%)")
        elif mock >= 75.0:
            strengths.append(f"Good mock interview score ({mock:.1f}%)")

    # Aptitude check
    if apt is not None:
        if apt < 45.0:
            reasons.append(f"Quantitative aptitude score low ({apt:.1f}%)")
        elif apt >= 75.0:
            strengths.append(f"Solid aptitude assessment ({apt:.1f}%)")

    # Resume check
    if resume is not None and str(resume).strip().lower() not in ("", "nan", "none", "n/a"):
        is_ready = str(resume).strip().lower() in ("yes", "true", "1", "ready")
        if not is_ready:
            reasons.append("Resume not verified / requires revision")
        else:
            strengths.append("Verified resume on file")

    signal_count = len(reasons)
    if critical or signal_count >= 2:
        level = "High"
        color = "#B42318"
        badge_class = "badge-danger"
    elif signal_count == 1:
        level = "Medium"
        color = "#B54708"
        badge_class = "badge-warning"
    else:
        level = "Placement Ready"
        color = "#16803C"
        badge_class = "badge-success"
        if not strengths:
            strengths = ["Placement readiness metrics meet institutional requirements."]
        reasons = strengths

    return {
        "level": level,
        "color": color,
        "badge_class": badge_class,
        "reasons": reasons,
        "is_applicable": True,
        "signal_count": signal_count,
        "strengths": strengths,
    }


def evaluate_student_risks(student_record: Dict[str, Any], success_info: Dict[str, Any]) -> Dict[str, Any]:
    """Combines academic and placement risk assessments."""
    acad_risk = evaluate_academic_risk(student_record, success_info)
    place_risk = evaluate_placement_risk(student_record, success_info)

    return {
        "academic_risk": acad_risk,
        "placement_risk": place_risk,
    }
