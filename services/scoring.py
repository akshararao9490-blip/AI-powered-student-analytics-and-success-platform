"""
Smart Campus Analytics & Student Success Platform
Scoring Service — Computes transparent, explainable Student Success Scores.
"""

from typing import Dict, Any, Optional, Tuple, List
import math

DEFAULT_WEIGHTS = {
    "academic": 0.30,
    "attendance": 0.20,
    "lms": 0.10,
    "placement": 0.20,
    "skills": 0.10,
    "engagement": 0.05,
    "feedback": 0.05,
}

SCORE_BANDS = [
    (80.0, 100.0, "Strong Progress", "#16803C", "badge-success"),
    (65.0, 79.999, "On Track / Monitor", "#3B5BDB", "badge-info"),
    (50.0, 64.999, "Needs Support", "#B54708", "badge-warning"),
    (0.0, 49.999, "Priority Support", "#B42318", "badge-danger"),
]


def clamp(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamps a floating point number between min_val and max_val."""
    return max(min_val, min(max_val, float(val)))


def is_valid_num(val: Any) -> bool:
    """Checks if a value is a valid non-null, non-NaN number."""
    if val is None:
        return False
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ("", "nan", "none", "null", "n/a", "na"):
            return False
        try:
            float(v)
            return True
        except ValueError:
            return False
    if isinstance(val, (int, float)):
        return not (math.isnan(val) or math.isinf(val))
    return False


def to_float(val: Any, default: Optional[float] = None) -> Optional[float]:
    """Safely converts value to float."""
    if not is_valid_num(val):
        return default
    return float(val)


def calculate_academic_subscore(row: Dict[str, Any]) -> Optional[float]:
    """
    Academic subscore combining CGPA (0-10 -> 0-100), internal marks,
    optional subject performance, and backlog penalties.
    """
    cgpa = to_float(row.get("cgpa"))
    internal = to_float(row.get("internal_marks_pct"))
    subject = to_float(row.get("subject_performance_pct"))
    backlog = to_float(row.get("backlog_count"), 0.0)

    # Need at least cgpa or internal marks
    if cgpa is None and internal is None:
        return None

    components = []
    weights = []

    if cgpa is not None:
        components.append(clamp(cgpa * 10.0))
        weights.append(0.6 if internal is not None else 1.0)
    if internal is not None:
        components.append(clamp(internal))
        weights.append(0.4 if cgpa is not None else 1.0)
    if subject is not None and cgpa is not None and internal is not None:
        # If all 3 present, blend 50/30/20
        components = [clamp(cgpa * 10.0), clamp(internal), clamp(subject)]
        weights = [0.5, 0.3, 0.2]

    total_w = sum(weights)
    if total_w == 0:
        return None

    base_score = sum(c * w for c, w in zip(components, weights)) / total_w
    # Backlog penalty: 10 points per backlog
    penalty = max(0.0, backlog) * 10.0
    return clamp(base_score - penalty)


def calculate_attendance_subscore(row: Dict[str, Any]) -> Optional[float]:
    """Attendance percentage (0-100)."""
    att = to_float(row.get("attendance_pct"))
    if att is None:
        return None
    return clamp(att)


def calculate_lms_subscore(row: Dict[str, Any]) -> Optional[float]:
    """LMS activity combining assignment completion and weekly logins."""
    assign = to_float(row.get("assignment_completion_pct"))
    logins = to_float(row.get("lms_logins_per_week"))

    if assign is None and logins is None:
        return None

    if assign is not None and logins is not None:
        # Cap logins at 15 logins/week = 100%
        login_score = clamp((logins / 15.0) * 100.0)
        return clamp(0.70 * clamp(assign) + 0.30 * login_score)
    elif assign is not None:
        return clamp(assign)
    else:
        return clamp((logins / 15.0) * 100.0)


def calculate_placement_subscore(row: Dict[str, Any]) -> Optional[float]:
    """
    Placement readiness subscore. Returns None if placement is not applicable
    (e.g., early years or assessments not taken).
    """
    apt = to_float(row.get("aptitude_score_pct"))
    coding = to_float(row.get("coding_score_pct"))
    mock = to_float(row.get("mock_interview_pct"))
    resume = row.get("resume_ready")

    # If all placement metrics are missing, cohort is not yet in placement phase
    if apt is None and coding is None and mock is None and resume is None:
        return None

    components = []
    weights = []

    if apt is not None:
        components.append(clamp(apt))
        weights.append(0.30)
    if coding is not None:
        components.append(clamp(coding))
        weights.append(0.35)
    if mock is not None:
        components.append(clamp(mock))
        weights.append(0.25)
    if resume is not None and str(resume).strip().lower() not in ("", "nan", "none", "n/a"):
        is_ready = str(resume).strip().lower() in ("yes", "true", "1", "ready")
        components.append(100.0 if is_ready else 30.0)
        weights.append(0.10)

    if not weights or sum(weights) == 0:
        return None

    return clamp(sum(c * w for c, w in zip(components, weights)) / sum(weights))


def calculate_skills_subscore(row: Dict[str, Any]) -> Optional[float]:
    """Skills subscore averaging available rubrics."""
    tech = to_float(row.get("technical_skill_pct"))
    comm = to_float(row.get("communication_skill_pct"))
    prob = to_float(row.get("problem_solving_pct"))

    available = [s for s in (tech, comm, prob) if s is not None]
    if not available:
        return None
    return clamp(sum(available) / len(available))


def calculate_engagement_subscore(row: Dict[str, Any]) -> Optional[float]:
    """Engagement subscore based on participation, clubs, certifications."""
    events = to_float(row.get("events_participated"))
    clubs = to_float(row.get("clubs_or_hackathons"))
    certs = to_float(row.get("certifications_count"))

    if events is None and clubs is None and certs is None:
        return None

    e_val = events or 0.0
    c_val = clubs or 0.0
    cert_val = certs or 0.0

    raw = (e_val * 15.0) + (c_val * 20.0) + (cert_val * 25.0)
    return clamp(raw)


def calculate_feedback_subscore(row: Dict[str, Any]) -> Optional[float]:
    """Feedback subscore normalizing 1-5 scale to 0-100."""
    stu = to_float(row.get("student_feedback_score"))
    fac = to_float(row.get("faculty_feedback_score"))

    if stu is None and fac is None:
        return None

    scores = []
    for f in (stu, fac):
        if f is not None:
            # 1 to 5 scale normalized: (rating - 1) / 4 * 100
            norm = clamp(((f - 1.0) / 4.0) * 100.0)
            scores.append(norm)

    return clamp(sum(scores) / len(scores)) if scores else None


def compute_student_success_score(
    student_record: Dict[str, Any],
    custom_weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Computes transparent Student Success Score with dynamic weight re-normalization,
    explainability drivers, and data coverage indicators.
    """
    weights = custom_weights or DEFAULT_WEIGHTS

    subscores: Dict[str, Optional[float]] = {
        "academic": calculate_academic_subscore(student_record),
        "attendance": calculate_attendance_subscore(student_record),
        "lms": calculate_lms_subscore(student_record),
        "placement": calculate_placement_subscore(student_record),
        "skills": calculate_skills_subscore(student_record),
        "engagement": calculate_engagement_subscore(student_record),
        "feedback": calculate_feedback_subscore(student_record),
    }

    # Determine applicable categories and weights
    applicable_subscores: Dict[str, float] = {}
    total_applicable_weight = 0.0

    for cat, score in subscores.items():
        if score is not None:
            applicable_subscores[cat] = score
            total_applicable_weight += weights.get(cat, 0.0)

    # Coverage percentage
    total_possible_categories = len(subscores)
    present_categories = len(applicable_subscores)
    coverage_pct = round((present_categories / total_possible_categories) * 100.0, 1)

    # Insufficient data check: need at least 40% total applicable weight or attendance+academics
    if total_applicable_weight < 0.35 or (subscores["academic"] is None and subscores["attendance"] is None):
        return {
            "score": None,
            "band": "Insufficient Data",
            "band_color": "#667085",
            "band_class": "badge-neutral",
            "coverage_pct": coverage_pct,
            "subscores": subscores,
            "normalized_weights": {},
            "positive_drivers": [],
            "risk_drivers": ["Critical academic and attendance indicators missing"],
            "explanation": "Insufficient data available to compute a reliable success score.",
            "is_sufficient": False,
        }

    # Weight re-normalization
    normalized_weights: Dict[str, float] = {}
    weighted_sum = 0.0

    for cat, score in applicable_subscores.items():
        w = weights.get(cat, 0.0)
        norm_w = w / total_applicable_weight
        normalized_weights[cat] = round(norm_w, 4)
        weighted_sum += score * norm_w

    final_score = round(clamp(weighted_sum), 1)

    # Determine Band
    band_label = "Priority Support"
    band_color = "#B42318"
    band_class = "badge-danger"

    for min_val, max_val, label, color, css_class in SCORE_BANDS:
        if min_val <= final_score <= max_val:
            band_label = label
            band_color = color
            band_class = css_class
            break

    # Explainability: Positive Drivers & Risk Drivers
    positive_drivers: List[str] = []
    risk_drivers: List[str] = []

    cat_friendly_names = {
        "academic": "Academic Performance",
        "attendance": "Classroom Attendance",
        "lms": "LMS Coursework & Activity",
        "placement": "Placement Readiness",
        "skills": "Technical & Soft Skills",
        "engagement": "Campus Co-curricular Engagement",
        "feedback": "Mentor & Pulse Feedback",
    }

    for cat, score in applicable_subscores.items():
        name = cat_friendly_names.get(cat, cat.title())
        if score >= 75.0:
            positive_drivers.append(f"{name} is strong ({score:.1f}/100)")
        elif score < 55.0:
            risk_drivers.append(f"{name} is low ({score:.1f}/100)")

    # Backlog driver
    backlogs = to_float(student_record.get("backlog_count"), 0.0)
    if backlogs > 0:
        risk_drivers.append(f"Active backlogs: {int(backlogs)}")

    # Construct narrative explanation
    explanation_parts = []
    if positive_drivers:
        explanation_parts.append("Key strengths: " + "; ".join(positive_drivers[:2]) + ".")
    if risk_drivers:
        explanation_parts.append("Areas requiring attention: " + "; ".join(risk_drivers[:2]) + ".")
    if not risk_drivers and not positive_drivers:
        explanation_parts.append("Indicators show moderate, consistent performance across categories.")

    explanation = " ".join(explanation_parts)

    return {
        "score": final_score,
        "band": band_label,
        "band_color": band_color,
        "band_class": band_class,
        "coverage_pct": coverage_pct,
        "subscores": subscores,
        "normalized_weights": normalized_weights,
        "positive_drivers": positive_drivers,
        "risk_drivers": risk_drivers,
        "explanation": explanation,
        "is_sufficient": True,
    }
