# `context.md` — Smart Campus Analytics & Student Success Platform

> **Project:** Smart Campus Analytics: Predict, Optimize & Improve Student Success  
> **Hackathon:** HacXLerate 2026 — Round 1  
> **Challenge owner:** KPMG in India  
> **Team:** BIG BUSTERS  
> **Purpose of this file:** This is the persistent source of truth for AI-assisted development in Antigravity. Read it before making changes. Keep the product, architecture, visual design, naming, and workflows consistent across sessions.

---

## 1. Instructions to the AI Developer

At the beginning of every session, read this entire `context.md` and inspect the existing repository before doing anything. Continue from the current implementation; do not restart or regenerate the project from scratch unless explicitly requested.

### Non-negotiable rules
1. **Preserve existing work.** Do not delete, overwrite, or redesign working features without a clear need and explicit approval.
2. **Keep the UI consistent.** New features must use the existing layout, navigation, colors, typography, spacing, cards, tables, chart styles, and interaction patterns. Do not introduce a second design system.
3. **Do not interrupt the user for routine decisions.** Use the defaults in this file, make sensible implementation choices, and continue. Ask a question only when a required decision cannot safely be inferred or when an action is destructive.
4. **Implement end-to-end.** A feature is not complete until its UI, data handling, validation, empty/error states, and navigation work together.
5. **Run and test the app.** After changes, run the available checks and fix errors. Do not claim something was tested if it was not.
6. **Keep changes focused.** Avoid unrelated refactors, unnecessary dependencies, duplicated components, and placeholder buttons that do nothing.
7. **Maintain this file.** When a major architecture, dependency, route, schema, scoring rule, or design-system decision changes, update this file to match the implementation.
8. **Persist progress.** Keep implementation notes in `PROJECT_STATUS.md` (create it if missing), including completed features, current state, commands, known bugs, and next tasks. Update it after each substantial work session.
9. **Never fabricate results.** Clearly label generated/demo data as synthetic. Do not claim a prediction model is accurate without evaluation evidence.
10. **Privacy and fairness.** Use synthetic or anonymized student records for demos. Risk scores are decision-support signals, not final judgments about a student. Avoid using protected or irrelevant personal attributes.

### Session-resume protocol
When a new session begins:
1. Read `context.md` and `PROJECT_STATUS.md` if present.
2. Inspect the repository tree, dependencies, and existing application entry point.
3. Identify what is already implemented and what remains.
4. Run the app or relevant tests if practical.
5. Continue from the highest-priority unfinished item in the status file.
6. Do not ask the user to repeat information already documented here.
7. Before finishing, update `PROJECT_STATUS.md` and report the exact run command, completed work, test status, and remaining issues.

---

## 2. Product Vision

Build a polished, interactive **Smart Campus Analytics & Student Success Platform** that combines academic, attendance, learning-platform, engagement, placement, skills, and feedback information into a unified student view. It should help faculty and administrators understand student progress, identify students who may benefit from support, and take targeted, explainable action.

This must be more than a static dashboard. It should provide:
- A unified view of student indicators from multiple data categories.
- A transparent Student Success Score.
- Explainable academic-risk and placement-readiness flags.
- Interactive analytics and meaningful trends.
- Student segmentation that supports targeted interventions.
- A student-level profile showing why a score or flag was assigned.
- Practical intervention recommendations and follow-up tracking.

### Primary users
- **Administrator:** sees overall institutional patterns, filters cohorts, reviews risk distribution, and identifies priorities.
- **Faculty / Mentor:** reviews assigned or filtered students, understands risk drivers, and records follow-up actions.
- **Placement coordinator:** reviews placement readiness, aptitude/coding/mock interview performance, skills gaps, and recommended preparation.

The prototype may use role selection or role-specific views; do not build complex authentication unless it is already present or specifically requested.

### Core product principle
**Every insight should answer three questions:**
1. What is happening?
2. Why might it be happening?
3. What practical action can the college take?

---

## 3. Hackathon Requirements and Evaluation Priorities

The challenge requires:
1. **Data integration:** academic, attendance, LMS, engagement, placement, skills, and feedback indicators in one unified student view.
2. **Student Success Score:** documented formula using relevant indicators.
3. **At-risk identification:** potential academic-performance and placement-outcome risks.
4. **Interactive dashboard:** scores, flags, trends, and student insights.
5. **Bonus — segmentation:** meaningful student groups.
6. **Bonus — explainability:** show the indicators contributing to each score and flag.

Evaluation weighting:
- Data integration and analysis — 30%
- Success score and risk identification — 25%
- Dashboard and visualization — 25%
- Problem understanding — 10%
- Presentation and demo — 10%

Therefore, prioritize working data integration, understandable scoring, risk explanations, useful filters, and a smooth demo over decorative features.

---

## 4. Recommended Technology Defaults

**First inspect the existing project. Keep its current working stack if one exists.** Do not migrate frameworks just for preference.

If the repository is empty or no stack has been chosen, use this simple hackathon-friendly default:
- **Language:** Python
- **UI:** Streamlit
- **Data manipulation:** pandas, NumPy
- **Charts:** Plotly
- **Modeling (optional):** scikit-learn, only when a meaningful labeled dataset and evaluation approach exist
- **Data storage:** CSV files for the simplest demo; SQLite for editable intervention records if needed
- **Testing:** pytest for scoring and data-processing functions
- **Deployment:** use the platform already configured in the repository; document environment variables and deployment steps.

Keep dependencies minimal. Pin compatible versions in the existing dependency file. Never expose secrets or credentials in source control.

### Suggested structure (adapt to the existing repository rather than forcing this structure)
```text
project-root/
├── app.py
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Student_Explorer.py
│   ├── 3_Risk_Insights.py
│   ├── 4_Segments.py
│   └── 5_Interventions.py
├── components/
│   ├── layout.py
│   ├── sidebar.py
│   ├── metric_cards.py
│   ├── charts.py
│   └── tables.py
├── services/
│   ├── data_loader.py
│   ├── data_validation.py
│   ├── scoring.py
│   ├── risk_rules.py
│   ├── segmentation.py
│   └── recommendations.py
├── data/
│   ├── sample_students.csv
│   └── README.md
├── tests/
│   ├── test_scoring.py
│   ├── test_data_validation.py
│   └── test_risk_rules.py
├── assets/
├── requirements.txt
├── context.md
├── PROJECT_STATUS.md
└── README.md
```
This is a suggested structure, not a reason to reorganize a functioning project.

---

## 5. User Experience and Navigation

Use a stable sidebar or top navigation, consistent across every page. Recommended sections:
1. **Overview** — institutional KPIs, score distribution, risk breakdown, trends, and priority insights.
2. **Student Explorer** — searchable/filterable table and individual student profiles.
3. **Risk Insights** — academic risk and placement readiness with explainable drivers.
4. **Student Segments** — groups of students with common needs.
5. **Interventions** — recommended support actions, assigned owner, status, and follow-up date.
6. **Data & Methodology** — data coverage, missing-data warnings, score formula, thresholds, and demo-data notice.

If the current project uses different route names, preserve them and map these capabilities to the existing navigation.

### Global filters
Where relevant, provide consistent filters:
- Department / branch
- Academic year / cohort
- Semester
- Risk category
- Student segment

Filters should update related KPIs, charts, and tables together. Include a clear reset option. Avoid filters that silently fail or affect only part of the page.

### Overview dashboard content
Use a clear hierarchy:
- Header with product name, page title, and concise purpose.
- KPI cards: Total Students, Average Success Score, Students Needing Support, Placement-Ready Students.
- Charts: Success Score distribution, academic vs placement risk, risk by department/cohort, and trend over time if time-series data exists.
- Priority insight panel: top risk drivers and recommended actions.
- Student table: student ID, department, success score, academic risk, placement readiness, and primary reason.

Never invent a time trend if the dataset has no dates or historical snapshots. Instead, show a truthful distribution or comparison.

---

## 6. Visual Design System — Do Not Change Between Features

Inspect the existing UI first. If a visual system already exists, document and preserve its exact tokens. If not, establish the following default system and reuse it everywhere.

### Visual direction
- Professional, modern campus analytics product.
- Calm, accessible, data-focused interface.
- Light neutral background, white content surfaces, restrained indigo/blue accent, readable dark text.
- Use red/amber/green only for meaningful risk/status indicators, not as decoration.
- Avoid random gradients, excessive animation, changing themes, or a different style on each page.

### Default design tokens
```css
:root {
  --color-bg: #F5F7FB;
  --color-surface: #FFFFFF;
  --color-text: #172033;
  --color-muted: #667085;
  --color-border: #E4E7EC;
  --color-primary: #3B5BDB;
  --color-primary-soft: #EEF2FF;
  --color-success: #16803C;
  --color-success-soft: #EAF7EE;
  --color-warning: #B54708;
  --color-warning-soft: #FFF4E5;
  --color-danger: #B42318;
  --color-danger-soft: #FEECEB;
  --radius-card: 14px;
  --radius-control: 9px;
  --shadow-card: 0 2px 10px rgba(16, 24, 40, 0.05);
  --space-page: 24px;
  --space-card: 18px;
}
```
These are defaults for a new UI only. Do not force CSS tokens if the current framework has an established design system.

### Components and consistency rules
- Use one shared component for KPI cards, status badges, section headings, filter bars, data tables, and empty/error states.
- Use the same card radius, padding, border, shadow, and typography across all pages.
- Keep chart titles, legends, hover labels, number formats, and risk colors consistent.
- Keep sidebar width, navigation order, logo placement, and page spacing stable.
- Do not duplicate a component with slightly different styling; extend the shared component instead.
- Do not remove or rename existing navigation items without a strong reason.
- Ensure responsive layouts for laptop and smaller screens.
- Use accessible contrast, clear labels, keyboard-friendly controls, and text labels alongside color.
- Prefer clean charts and readable tables over visual clutter.
- Add new features within the existing page and component patterns. **A feature addition must not trigger a redesign of the rest of the application.**

---

## 7. Unified Data Model

Use a stable `student_id` as the key. Merge data sources on that key, validate joins, and report unmatched or missing records rather than silently dropping them.

### Recommended fields
| Category | Example fields | Notes |
|---|---|---|
| Identity / cohort | `student_id`, `student_name` (optional), `department`, `academic_year`, `semester` | Prefer synthetic names in demo data; IDs are sufficient for most charts. |
| Academic | `cgpa`, `internal_marks_pct`, `backlog_count`, `subject_performance_pct` | Convert values to consistent ranges and document units. |
| Attendance | `attendance_pct` | Percentage 0–100. |
| LMS | `lms_logins_per_week`, `assignment_completion_pct` | Use a defined observation window. |
| Engagement | `events_participated`, `clubs_or_hackathons`, `certifications_count` | Do not treat low extracurricular participation alone as proof of poor potential. |
| Placement | `aptitude_score_pct`, `coding_score_pct`, `mock_interview_pct`, `resume_ready` | May be unavailable for early-year students; handle as missing/not applicable. |
| Skills | `technical_skill_pct`, `communication_skill_pct`, `problem_solving_pct` | Use a consistent assessment rubric. |
| Feedback | `student_feedback_score`, `faculty_feedback_score` | Document scale, such as 1–5, and normalize before scoring. |
| Optional history | `snapshot_date`, `semester_gpa`, `previous_attendance_pct` | Only show trend charts when historical observations exist. |

### Data integration requirements
- Accept one combined CSV or multiple category-specific CSVs.
- Provide a clear upload/replace-data workflow if the existing application supports uploads.
- Validate required columns, numeric types, ranges, duplicate IDs, and join coverage.
- Normalize field names and units.
- Do not silently convert invalid values to plausible values.
- Distinguish **missing**, **not applicable**, and actual zero values.
- Show data coverage and warnings to the user.
- Use safe fallback behavior when optional columns are absent.
- Include a synthetic sample dataset so the app works immediately after setup.
- Include a data dictionary in `data/README.md` or the project README.
- Do not require access to a college database or external API for the core demo.

### Synthetic data
Generate realistic, varied synthetic records for demo use. Label the data clearly as **synthetic demonstration data—not actual SIET student records**. Avoid real student names, roll numbers, phone numbers, emails, or other personal information. Make sure the sample dataset contains enough variety to demonstrate low, medium, and high risk and several meaningful segments.

---

## 8. Student Success Score

Create a transparent 0–100 score. The score is a **prototype decision-support indicator**, not a validated prediction of a student's future.

### Initial weighted formula
Normalize each available input to 0–100, where higher means more favorable. Use these default weights:

| Indicator | Weight |
|---|---:|
| Academic performance | 30% |
| Attendance | 20% |
| LMS learning activity | 10% |
| Placement readiness | 20% |
| Skills | 10% |
| Engagement | 5% |
| Feedback | 5% |
| **Total** | **100%** |

Define the category sub-scores consistently:
- **Academic performance (30%)**: combine CGPA normalized to 0–100, internal marks percentage, and backlog penalty. If CGPA is on a 10-point scale, convert `cgpa / 10 * 100`. Use a documented backlog penalty and cap the result between 0 and 100.
- **Attendance (20%)**: `attendance_pct`.
- **LMS learning activity (10%)**: combine assignment completion and login activity, capped and normalized to 0–100. Do not let extreme login counts dominate the score.
- **Placement readiness (20%)**: combine aptitude, coding, mock interview, and resume readiness when applicable. If placement data is not applicable to a cohort, mark it N/A and re-normalize weights over available applicable categories.
- **Skills (10%)**: average available technical, communication, and problem-solving assessment scores.
- **Engagement (5%)**: use a capped participation indicator based on events, clubs, hackathons, and certifications. Do not make participation a high-weight proxy for a student's worth or potential.
- **Feedback (5%)**: normalize 1–5 ratings to 0–100, for example `(rating - 1) / 4 * 100`.

### Missing data and weight handling
- Never treat missing values as zero by default.
- For each student, calculate the weighted average using only applicable, valid categories and re-normalize the weights to sum to 100%.
- Show a data-coverage indicator so a score based on fewer categories is visibly less complete.
- If critical data is missing, display “Insufficient data” rather than a misleading precise score.
- Keep full-precision values for calculations; display a rounded integer or one decimal consistently.

### Suggested interpretation bands
- **80–100: Strong progress**
- **65–79.9: On track / monitor**
- **50–64.9: Needs support**
- **Below 50: Priority support**

These are initial demo thresholds, not validated institutional standards. Make thresholds easy to configure and document.

### Explainability
For every displayed score, show:
- Category scores and weights.
- Which categories most improved or lowered the result.
- Missing or non-applicable categories.
- A short plain-language explanation, e.g. “Attendance and assignment completion are strong; the current score is mainly lowered by internal marks and coding assessment.”
- Do not claim a feature caused an outcome unless evidence supports causality.

Write scoring logic in a reusable service/module and cover it with unit tests. Do not copy the formula separately into page files.

---

## 9. Risk Identification

Maintain separate, understandable flags for **academic support need** and **placement readiness**. A combined low success score may prompt review, but it should not replace category-specific checks.

### Initial academic-support rules
Flag for review when one or more conditions apply:
- Attendance below 75%.
- Academic performance below 50/100.
- Backlog count greater than zero, with severity adjusted to the actual count.
- Success score below 50/100, when sufficient data exists.

### Initial placement-readiness rules
For cohorts where placement preparation is relevant, flag for review when one or more conditions apply:
- Average of available aptitude, coding, and mock interview scores below 50/100.
- Coding score below 40/100.
- Mock interview score below 50/100.
- Resume not marked ready, if resume readiness data is available.

### Risk levels
- **High:** multiple strong risk signals or a critical threshold is crossed.
- **Medium:** one meaningful risk signal or score in the support range.
- **Low:** no current rule-based signals detected.
- **Insufficient data:** cannot safely determine risk.

Document exact implemented thresholds in the methodology page. Keep the logic in `risk_rules.py` or its equivalent. Make the rules transparent and configurable.

### Responsible use
- Risk flags indicate who may benefit from a conversation or additional support; they are not labels of ability or character.
- Do not automatically penalize students or make high-stakes decisions from the score.
- Show “Review recommended” rather than claiming certainty.
- Allow authorized users to record context and follow-up, where feasible.
- Use only indicators relevant to the stated educational purpose. Do not use caste, religion, gender, disability, health data, family income, or other protected/sensitive traits in scoring.
- Avoid unfairly scoring students down for unavailable placement assessments or optional extracurricular activities.

---

## 10. Student Segmentation

Implement understandable, rule-based segments first; unsupervised clustering is optional and should not be added merely for appearance.

Recommended segments:
1. **Strong Academics, Low Placement Readiness** — academic score high, placement score low.
2. **Attendance Support Needed** — attendance below the configured threshold.
3. **Academic Recovery** — low academic score and/or backlogs.
4. **Low LMS Engagement** — low assignment completion or unusually low learning-platform activity, where measured reliably.
5. **Skills Development** — technical, coding, communication, or problem-solving score below target.
6. **Well-Rounded / On Track** — no current risk signal and a sufficiently complete dataset.
7. **Insufficient Data** — missing information prevents meaningful assignment.

Define the rules in one module, make them inspectable, and allow a student to match more than one support segment if appropriate. Explain each segment and offer a relevant intervention. Do not imply that segmentation proves a cause.

---

## 11. Intervention Recommendations and Follow-up

Recommendations should be specific, constructive, and connected to observed indicators. Examples:
- Low attendance → mentor check-in, review attendance barriers, agree on an attendance plan.
- Low internal marks / backlogs → subject-level tutoring, faculty office hours, weekly progress review.
- Low assignment completion → LMS orientation, smaller milestones, reminder/support plan.
- Low coding score → coding practice plan, lab sessions, weekly mock problems.
- Low aptitude score → structured aptitude practice and progress checks.
- Low mock interview score → mock interview, communication practice, feedback session.
- Strong academics but low placement readiness → placement-readiness roadmap, resume review, coding/interview practice.

Avoid generic, judgmental, or punitive messages. The app should let a user mark an action as planned, in progress, completed, or cancelled. Persist intervention status if storage exists; otherwise make the demo limitation explicit. Do not claim an intervention improved outcomes unless outcome data is available.

---

## 12. Charts, Tables, and Interaction Standards

- Use charts that answer a clear question; avoid decorative graphs.
- Use consistent risk colors and accessible labels.
- Every chart should have a title, units, understandable axes, and tooltips where helpful.
- Provide useful empty states if filters return no records.
- Make tables searchable, sortable, and filterable where the framework supports it.
- Student rows should open a detail/profile view or provide a clear “View details” action.
- Student detail should show score, risk flags, indicator breakdown, data completeness, key drivers, and recommended next actions.
- Use consistent percentage formatting and score precision.
- Avoid exposing personally identifying information in charts or demo screenshots.
- Keep page loading and interactions simple enough for a live hackathon demonstration.

---

## 13. Error Handling and Reliability

The app should:
- Start with sample data when no upload is provided.
- Display helpful messages for missing files, malformed CSVs, absent required columns, invalid numbers, duplicate IDs, and empty datasets.
- Validate score inputs and clamp normalized scores only when the intended transformation is documented.
- Avoid crashing when optional columns are absent.
- Avoid division by zero and empty-category errors.
- Avoid leaking stack traces or private file paths to end users.
- Keep internal logs useful for debugging.
- Provide a clear reset-to-demo-data option if upload/replace-data exists.
- Never overwrite the original sample file when a user uploads a dataset.
- Avoid silent fallbacks that hide bad data.

---

## 14. AI/ML Policy

The challenge mentions analytics and AI, but a clear, explainable rules-based prototype is better than an unsupported black-box model.

Default implementation:
- Build reliable data integration, transparent weighted scoring, explainable risk rules, segmentation, and actionable recommendations first.
- If adding machine learning, use it only when a suitable target label and enough valid historical records exist.
- Split training/test data appropriately, avoid data leakage, and report appropriate evaluation metrics.
- Clearly distinguish observed values, rule-based flags, and model predictions in the UI.
- Never invent model accuracy, training data, or predictions.
- Do not train on synthetic data and present the resulting performance as real-world validation.
- Keep a deterministic fallback when model dependencies or trained models are unavailable.

For the hackathon demo, “AI-powered” can be demonstrated responsibly through integrated analytics, interpretable risk signals, segmentation, and personalized next-step recommendations. Explain this accurately during the demo.

---

## 15. Testing Checklist

Before marking a feature complete, verify the relevant items:
- [ ] App starts using the documented command.
- [ ] Existing pages and navigation still work.
- [ ] Global filters update all related components consistently.
- [ ] Sample data loads successfully.
- [ ] Multiple CSV sources join correctly on `student_id`.
- [ ] Duplicate IDs, invalid ranges, missing fields, and empty data are handled.
- [ ] Scores remain in the 0–100 range.
- [ ] Missing/not-applicable data does not silently become zero.
- [ ] Applicable weights are re-normalized correctly.
- [ ] Risk flags match the documented rules.
- [ ] Explainability shows actual score drivers.
- [ ] Segments match their documented rules.
- [ ] Student details show the same scores and flags as the dashboard.
- [ ] Intervention updates persist as designed.
- [ ] No placeholder buttons or broken links remain.
- [ ] UI remains visually consistent on every page.
- [ ] Layout is usable at laptop and narrow screen widths.
- [ ] Synthetic data is clearly labeled.
- [ ] README includes setup, run, demo data, methodology, and limitations.

Add tests for scoring and risk rules. For any calculation bug, fix the underlying shared function rather than patching a single visual component.

---

## 16. Demo Flow for Judges

Target a concise 3–5 minute demonstration:
1. **Problem (20–30 sec):** student data is fragmented and support can arrive too late.
2. **Unified data (30 sec):** show that academic, attendance, LMS, skills, and placement indicators combine into a student-level view.
3. **Overview (45 sec):** show KPIs, score distribution, and risk patterns.
4. **Explainability (45 sec):** open a student profile and explain the score and specific drivers.
5. **Segmentation (30 sec):** show “strong academics, low placement readiness” or another meaningful group.
6. **Action (30 sec):** show an intervention recommendation and follow-up status.
7. **Trust and limitations (15 sec):** explain transparent rules, missing-data handling, synthetic demo data, and human review.

Keep the demo stable. Prefer seeded synthetic data and deterministic rules so the same demonstration produces the same results every time.

---

## 17. Deployment and Submission Readiness

The hackathon deliverables include a working deployed dashboard prototype, a GitHub repository, a short explanation of the score, and a short demo or slides.

Prepare:
- A working local run command.
- A clear `README.md` with installation, execution, features, data schema, scoring formula, risk thresholds, and limitations.
- A `requirements.txt` or the project's existing dependency lock file.
- A synthetic sample dataset and data dictionary.
- Tests for scoring and risk logic.
- A short methodology note that matches the code.
- A demo script or screenshots.
- A deployed link that has been actually tested, if deployment is available.
- A GitHub repository without secrets, private student data, or local environment folders.

Never claim the app is deployed unless a working public URL has been verified. Never invent a deployment URL or repository URL. Before submission, test the deployed version from a fresh browser/session if possible.

---

## 18. Definition of Done

A task is done only when:
1. The feature works with real input and the sample dataset.
2. The UI follows the existing design system.
3. Loading, empty, invalid-data, and error states are handled.
4. Existing features still work.
5. Relevant tests or manual checks pass.
6. The README/context/status documentation is updated when needed.
7. The final report states what changed, which files changed, how to run it, what was tested, and any remaining limitation.

---

## 19. How to Respond to the User

When communicating progress:
- Use clear, concise language.
- Do not ask for information already in this file or the repository.
- If a reasonable default is documented, use it and proceed.
- If blocked, explain the exact blocker and offer the smallest decision needed.
- Do not claim success without verifying the relevant result.
- At the end of a work session, summarize:
  - Completed work
  - Important files changed
  - Run/test commands and actual results
  - Known issues
  - Next recommended task

**Primary instruction:** Build a stable, coherent, demonstrable student-success platform. Protect existing functionality and visual consistency. Make every score explainable, every risk actionable, and every session resumable.
