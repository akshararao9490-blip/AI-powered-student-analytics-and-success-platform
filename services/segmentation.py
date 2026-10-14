"""
Smart Campus Analytics & Student Success Platform
Student Segmentation Service — Rule-based cohort segmentation.
"""

from typing import Dict, Any, List
from services.scoring import to_float


SEGMENT_DEFINITIONS = {
    "Strong Academics, Low Placement Readiness": {
        "description": "High academic achievement but struggling with coding, aptitude, or mock interviews.",
        "icon": "🎯",
        "recommended_action": "Targeted placement bootcamps, DSA mentoring, and mock interview coaching.",
        "color": "#3B5BDB",
    },
    "Attendance Support Needed": {
        "description": "Attendance below the mandatory statutory threshold (75%).",
        "icon": "⏱️",
        "recommended_action": "Proactive mentor check-in, review personal/transport barriers, attendance agreement.",
        "color": "#B54708",
    },
    "Academic Recovery": {
        "description": "Facing active backlogs or continuous internal assessment score below 50%.",
        "icon": "📚",
        "recommended_action": "Remedial subject-level tutoring, faculty office hours, structured revision schedule.",
        "color": "#B42318",
    },
    "Low LMS Engagement": {
        "description": "Low assignment completion or minimal digital learning activity on campus LMS.",
        "icon": "💻",
        "recommended_action": "LMS refresher, chunked coursework milestones, automated assignment reminders.",
        "color": "#D97706",
    },
    "Skills Development": {
        "description": "Technical rubric, problem-solving, or communication assessment below benchmark.",
        "icon": "🛠️",
        "recommended_action": "Hands-on laboratory workshops, peer programming groups, soft-skills workshops.",
        "color": "#7C3AED",
    },
    "Well-Rounded / On Track": {
        "description": "Consistently strong performance across academic, attendance, and placement domains.",
        "icon": "🌟",
        "recommended_action": "Honors tracks, research mentorship, hackathon sponsorships, leadership roles.",
        "color": "#16803C",
    },
    "Insufficient Data": {
        "description": "Key assessment indicators are missing or unrecorded.",
        "icon": "❓",
        "recommended_action": "Request updated department records and follow up with mentor.",
        "color": "#667085",
    },
}


def assign_student_segments(
    student_record: Dict[str, Any],
    success_info: Dict[str, Any],
    risk_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assigns rule-based student segment tags and determines primary segment.
    """
    if not success_info.get("is_sufficient", True):
        return {
            "primary_segment": "Insufficient Data",
            "all_segments": ["Insufficient Data"],
            "details": SEGMENT_DEFINITIONS["Insufficient Data"],
        }

    subscores = success_info.get("subscores", {})
    acad_sub = subscores.get("academic", 0.0) or 0.0
    place_sub = subscores.get("placement")
    att = to_float(student_record.get("attendance_pct"), 100.0)
    backlogs = to_float(student_record.get("backlog_count"), 0.0)
    lms_assign = to_float(student_record.get("assignment_completion_pct"), 100.0)
    logins = to_float(student_record.get("lms_logins_per_week"), 10.0)
    skills_sub = subscores.get("skills", 100.0) or 100.0
    coding = to_float(student_record.get("coding_score_pct"))
    overall_score = success_info.get("score", 0.0) or 0.0
    acad_risk_level = risk_info.get("academic_risk", {}).get("level", "Low")

    matched_segments: List[str] = []

    # 1. Academic Recovery
    if backlogs > 0 or acad_sub < 50.0:
        matched_segments.append("Academic Recovery")

    # 2. Attendance Support Needed
    if att < 75.0:
        matched_segments.append("Attendance Support Needed")

    # 3. Strong Academics, Low Placement Readiness
    if acad_sub >= 68.0 and place_sub is not None and place_sub < 55.0:
        matched_segments.append("Strong Academics, Low Placement Readiness")

    # 4. Low LMS Engagement
    if lms_assign < 60.0 or logins < 3.0:
        matched_segments.append("Low LMS Engagement")

    # 5. Skills Development
    if skills_sub < 55.0 or (coding is not None and coding < 45.0):
        matched_segments.append("Skills Development")

    # 6. Well-Rounded / On Track
    if (
        overall_score >= 70.0
        and acad_risk_level == "Low"
        and att >= 80.0
        and backlogs == 0
        and (place_sub is None or place_sub >= 65.0)
    ):
        matched_segments.append("Well-Rounded / On Track")

    if not matched_segments:
        # Fallback based on score
        if overall_score >= 60.0:
            matched_segments.append("Well-Rounded / On Track")
        else:
            matched_segments.append("Skills Development")

    # Primary segment prioritization
    # Priority: Academic Recovery > Attendance Support > Strong Acad, Low Place > Low LMS > Skills > Well-Rounded
    priority_order = [
        "Academic Recovery",
        "Attendance Support Needed",
        "Strong Academics, Low Placement Readiness",
        "Low LMS Engagement",
        "Skills Development",
        "Well-Rounded / On Track",
    ]

    primary_segment = "Well-Rounded / On Track"
    for p in priority_order:
        if p in matched_segments:
            primary_segment = p
            break

    return {
        "primary_segment": primary_segment,
        "all_segments": matched_segments,
        "details": SEGMENT_DEFINITIONS.get(primary_segment, SEGMENT_DEFINITIONS["Well-Rounded / On Track"]),
    }
