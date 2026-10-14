# Data Dictionary & Synthetic Dataset Documentation

> **Notice:** All data in this directory is **100% synthetic demonstration data** created for the HacXLerate 2026 hackathon. It does not represent real students, faculty, or institutions. No personally identifiable information (PII) or sensitive personal data is collected or stored.

---

## 1. Unified Student Record Schema

The platform integrates data across seven key categories into a unified student record indexed by `student_id`.

| Field Name | Category | Type | Range / Format | Description |
|---|---|---|---|---|
| `student_id` | Identity | String | e.g. `STU2026-001` | Unique student identifier (Primary Key) |
| `student_name` | Identity | String | Synthetic name | Anonymized demo name for presentation |
| `department` | Cohort | String | CSE, IT, ECE, MECH, CIVIL, AI&DS | Academic branch/department |
| `academic_year` | Cohort | Integer | 1 to 4 | Current year of study |
| `semester` | Cohort | Integer | 1 to 8 | Current semester |
| `cgpa` | Academic | Float | 0.0 – 10.0 | Cumulative Grade Point Average |
| `internal_marks_pct` | Academic | Float | 0.0 – 100.0 | Mid-term / continuous assessment percentage |
| `backlog_count` | Academic | Integer | $\ge 0$ | Number of currently active backlogs |
| `subject_performance_pct`| Academic | Float | 0.0 – 100.0 | Average recent semester exam subject score |
| `attendance_pct` | Attendance | Float | 0.0 – 100.0 | Overall semester attendance percentage |
| `lms_logins_per_week` | LMS | Float | $\ge 0.0$ | Average weekly active logins on the LMS |
| `assignment_completion_pct`| LMS | Float | 0.0 – 100.0 | Percentage of assigned LMS coursework submitted |
| `events_participated` | Engagement | Integer | $\ge 0$ | Technical workshops & symposiums attended |
| `clubs_or_hackathons` | Engagement | Integer | $\ge 0$ | Co-curricular clubs & hackathons participated |
| `certifications_count` | Engagement | Integer | $\ge 0$ | Validated industry / MOOC certifications |
| `aptitude_score_pct` | Placement | Float / NA | 0.0 – 100.0 | General & quantitative aptitude assessment |
| `coding_score_pct` | Placement | Float / NA | 0.0 – 100.0 | Programming & DSA test score |
| `mock_interview_pct` | Placement | Float / NA | 0.0 – 100.0 | Technical + HR mock interview assessment |
| `resume_ready` | Placement | Boolean / NA | Yes / No | Whether resume is reviewed and verified |
| `technical_skill_pct` | Skills | Float | 0.0 – 100.0 | Core domain technical rubric score |
| `communication_skill_pct`| Skills | Float | 0.0 – 100.0 | Soft skills & communication rubric score |
| `problem_solving_pct` | Skills | Float | 0.0 – 100.0 | Analytical & problem-solving rubric score |
| `student_feedback_score` | Feedback | Float | 1.0 – 5.0 | Student self-reported pulse rating |
| `faculty_feedback_score` | Feedback | Float | 1.0 – 5.0 | Mentor / faculty observations rating |

---

## 2. Handling Missing and Non-Applicable Data
- **Placement assessments:** Typically not conducted for 1st and early 2nd-year students. In these cohorts, placement indicators are marked `N/A` (or empty) and dynamically excluded from the weighted Student Success Score without penalty.
- **Data Coverage Metric:** Calculated as the proportion of indicator categories present for that student. If critical categories are absent (< 40% coverage), the platform displays an "Insufficient Data" warning rather than a fabricated score.
