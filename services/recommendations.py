"""
Smart Campus Analytics & Student Success Platform
Recommendations Service — Generates constructive, actionable, explainable intervention plans.
"""

from typing import Dict, Any, List
from services.scoring import to_float


def generate_recommendations(
    student_record: Dict[str, Any],
    success_info: Dict[str, Any],
    risk_info: Dict[str, Any],
    segment_info: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Generates tailored, prioritized, and constructive intervention actions
    directly linked to observed indicators.
    """
    actions: List[Dict[str, str]] = []

    att = to_float(student_record.get("attendance_pct"))
    backlogs = to_float(student_record.get("backlog_count"), 0.0)
    internal = to_float(student_record.get("internal_marks_pct"))
    lms_assign = to_float(student_record.get("assignment_completion_pct"))
    logins = to_float(student_record.get("lms_logins_per_week"))
    coding = to_float(student_record.get("coding_score_pct"))
    apt = to_float(student_record.get("aptitude_score_pct"))
    mock = to_float(student_record.get("mock_interview_pct"))
    resume = student_record.get("resume_ready")
    primary_seg = segment_info.get("primary_segment", "")

    # 1. Backlogs / Critical Academics
    if backlogs > 0:
        actions.append({
            "category": "Academic Remediation",
            "priority": "High",
            "trigger": f"{int(backlogs)} active backlog(s) recorded",
            "action": "Enroll in department remedial tutoring sessions and schedule weekly doubt-clearing with course faculty.",
            "owner": "Course Faculty / Academic Mentor",
            "target_timeline": "Within 7 days",
        })

    # 2. Attendance Shortage
    if att is not None and att < 75.0:
        urgency = "High" if att < 65.0 else "Medium"
        actions.append({
            "category": "Attendance Counseling",
            "priority": urgency,
            "trigger": f"Attendance is {att:.1f}% (below 75% requirement)",
            "action": "Conduct 1-on-1 mentor check-in to identify commute or personal challenges; establish a personalized attendance recovery commitment.",
            "owner": "Class Mentor / Proctor",
            "target_timeline": "Immediate (3 days)",
        })

    # 3. Internal Marks Deficit
    if internal is not None and internal < 50.0 and backlogs == 0:
        actions.append({
            "category": "Continuous Assessment Support",
            "priority": "Medium",
            "trigger": f"Internal assessment marks at {internal:.1f}%",
            "action": "Assign study-buddy peer partner and provide structured revision problem sets for upcoming internal assessments.",
            "owner": "Subject Faculty",
            "target_timeline": "Next 2 weeks",
        })

    # 4. Placement: Coding Proficiency
    if coding is not None and coding < 50.0:
        actions.append({
            "category": "Placement Technical Training",
            "priority": "High" if coding < 40.0 else "Medium",
            "trigger": f"Coding assessment score is {coding:.1f}%",
            "action": "Recommend daily 45-min curated DSA practice modules on college coding portal and hands-on laboratory problem-solving clinics.",
            "owner": "Placement Training Team",
            "target_timeline": "Ongoing (Bi-weekly review)",
        })

    # 5. Placement: Mock Interview & Soft Skills
    if mock is not None and mock < 50.0:
        actions.append({
            "category": "Interview Coaching",
            "priority": "Medium",
            "trigger": f"Mock interview score at {mock:.1f}%",
            "action": "Schedule specialized 1-on-1 communication review and video-recorded mock interview rehearsal with constructive feedback.",
            "owner": "Career Services / Soft Skills Trainer",
            "target_timeline": "Within 10 days",
        })

    # 6. Placement: Aptitude Score
    if apt is not None and apt < 50.0:
        actions.append({
            "category": "Quantitative Aptitude",
            "priority": "Medium",
            "trigger": f"Aptitude test score at {apt:.1f}%",
            "action": "Provide guided module-based practice quizzes focusing on quantitative reasoning and speed-math shortcuts.",
            "owner": "Aptitude Trainer",
            "target_timeline": "Next 2 weeks",
        })

    # 7. Resume Readiness
    if resume is not None and str(resume).strip().lower() in ("no", "false", "0"):
        actions.append({
            "category": "Career Profile Preparation",
            "priority": "Medium",
            "trigger": "Resume status is incomplete / unverified",
            "action": "Schedule resume verification review session to format projects, certifications, and technical profile.",
            "owner": "Placement Officer",
            "target_timeline": "Within 5 days",
        })

    # 8. LMS Engagement
    if (lms_assign is not None and lms_assign < 60.0) or (logins is not None and logins < 3.0):
        actions.append({
            "category": "Digital Coursework Engagement",
            "priority": "Low",
            "trigger": f"Assignment completion at {lms_assign or 0:.0f}%, logins {logins or 0:.1f}/week",
            "action": "Send automated coursework deadlines digest and provide orientation on accessing digital lecture materials.",
            "owner": "LMS Coordinator / Mentor",
            "target_timeline": "Within 1 week",
        })

    # 9. Strong Academics, Low Placement Cohort
    if primary_seg == "Strong Academics, Low Placement Readiness":
        actions.insert(0, {
            "category": "Comprehensive Placement Acceleration",
            "priority": "High",
            "trigger": "High academic capability with placement assessment gap",
            "action": "Fast-track into intensive coding bootcamps and algorithmic problem-solving batches to leverage strong conceptual foundation.",
            "owner": "Head of Placement & Corporate Relations",
            "target_timeline": "Immediate enrollment",
        })

    # 10. Default / Well-Rounded Recognition
    if not actions:
        actions.append({
            "category": "Enrichment & Mentorship",
            "priority": "Low",
            "trigger": "Consistently meeting or exceeding all benchmarks",
            "action": "Recommend for peer-mentorship roles, hackathon leadership, undergraduate research opportunities, or corporate competitive tracks.",
            "owner": "Department HOD / Academic Advisor",
            "target_timeline": "End of semester",
        })

    return actions
