# Smart Campus Analytics & Student Success Platform

> **Hackathon:** HacXLerate 2026 — Round 1  
> **Challenge Owner:** KPMG in India  
> **Team:** BIG BUSTERS  
> **Domain:** AI-Powered Student Analytics and Success Platform

---

## 1. Executive Summary & Problem Understanding

Higher education institutions face significant fragmentation across student data silos. Academic grades, daily classroom attendance, LMS digital coursework activity, campus engagement, and career placement preparation are traditionally monitored in isolation. Consequently, student learning deficits and placement readiness gaps are often discovered too late for effective faculty intervention.

**Smart Campus Analytics** by Team **BIG BUSTERS** bridges these silos into a unified student intelligence platform. It replaces opaque black-box models with a **transparent, explainable Student Success Score (0–100)**, an early-warning **dual risk engine** (Academic Support Need vs. Placement Readiness), **actionable student segmentation**, and a **persistent intervention tracking center** that closes the feedback loop.

---

## 2. Key Capabilities

1. **Unified Multi-Domain Integration:**
   - Synthesizes 7 key domains: Academics, Attendance, LMS Coursework, Placement Assessments, Skills Rubrics, Campus Engagement, and Mentor Feedback.
2. **Transparent Student Success Score (0–100):**
   - Weighted composite formula with **dynamic weight re-normalization** that handles missing or non-applicable indicators (e.g. junior cohorts without placement tests) without penalty.
3. **Explainable Dual Risk Engine:**
   - Decoupled early-warning flags for **Academic Support Need** and **Placement Readiness**, with plain-language diagnostic triggers and positive driver attributions.
4. **Behavioral Student Segmentation:**
   - Rule-based cohort clustering (e.g. *Strong Academics but Low Placement Readiness*, *Attendance Support Needed*, *Academic Recovery*, *Low LMS Engagement*) to prescribe differentiated, targeted interventions.
5. **Persistent Intervention Tracking (Closing the Loop):**
   - SQLite-backed action center allowing mentors, proctors, and placement coordinators to assign, update, and track resolution of student support plans.
6. **Data Integrity & Validation:**
   - Automated range checking, duplicate detection, completeness scoring, and custom CSV import with safe fallback to demonstration datasets.

---

## 3. Technology Stack

- **UI & Dashboard:** Streamlit 1.65+
- **Data Processing:** pandas 3.0+, NumPy 2.5+
- **Data Visualizations:** Plotly 7.1+
- **Persistence:** SQLite3 (standard library)
- **Testing:** pytest 9.1+
- **Language Environment:** Python 3.10+ (Tested on Python 3.14.0)

---

## 4. Quickstart & Installation

### Step 1: Clone and Navigate
```bash
git clone <repository-url>
cd pranitha
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python -m streamlit run app.py
```
Or with specific Python interpreter:
```bash
& "C:\Users\rajip\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py
```

The application will start and open automatically in your browser at `http://localhost:8501`.

### Step 4: Run Automated Tests
```bash
python -m pytest
```

---

## 5. Repository Structure

```text
pranitha/
├── app.py                      # Main landing page & executive summary dashboard
├── pages/
│   ├── 1_Overview.py           # Macro institutional performance & department comparisons
│   ├── 2_Student_Explorer.py   # Searchable roster & detailed explainable student profiles
│   ├── 3_Risk_Insights.py      # Dual risk engine, attendance vs CGPA scatter & triggers
│   ├── 4_Segments.py           # Behavioral cohort segmentation & cluster actions
│   ├── 5_Interventions.py      # SQLite persistent action center & lifecycle tracker
│   └── 6_Data_Methodology.py   # Mathematical formulas, validation report & ethics
├── components/
│   ├── layout.py               # Design tokens, custom CSS surfaces & header
│   ├── sidebar.py              # Global cohort filters & CSV upload switcher
│   ├── metric_cards.py         # Standardized KPI cards
│   ├── charts.py               # Plotly accessible chart components & radar visualizer
│   └── tables.py               # Searchable student tables & profile selector
├── services/
│   ├── data_loader.py          # Data ingestion, schema normalization & enrichment pipeline
│   ├── data_validation.py      # Range bounds, duplicate checks & completeness report
│   ├── scoring.py              # Transparent Student Success Score & weight re-normalization
│   ├── risk_rules.py           # Academic & placement early-warning diagnostic rules
│   ├── segmentation.py         # Rule-based student cohort segmentation
│   ├── recommendations.py      # Actionable, constructive intervention generator
│   ├── intervention_tracker.py # SQLite database persistence for interventions
│   └── state.py                # Cross-page session state caching
├── data/
│   ├── sample_students.csv     # 150 diverse synthetic demo records
│   ├── interventions.db        # SQLite database storing student action logs
│   └── README.md               # Data dictionary & schema documentation
├── tests/
│   ├── test_scoring.py         # Unit tests for scoring, clamping & re-normalization
│   ├── test_risk_rules.py      # Unit tests for academic & placement risk rules
│   ├── test_data_validation.py # Unit tests for dataset validation & boundary handling
│   └── test_segmentation.py    # Unit tests for cohort segmentation logic
├── context.md                  # Hackathon requirements & architectural source of truth
├── PROJECT_STATUS.md           # Persistent session tracker & verification log
├── requirements.txt            # Dependency specification
└── README.md                   # This documentation
```

---

## 6. Mathematical Methodology & Scoring Formulation

### Composite Base Indicator Weights
| Domain Indicator | Base Weight | Subscore Formulation |
|---|---:|---|
| **Academic Performance** | 30% | $0.5 \times (\text{CGPA} \times 10) + 0.3 \times \text{Internal\%} + 0.2 \times \text{Subject\%} - (\text{Backlogs} \times 10\text{ pts})$ |
| **Classroom Attendance** | 20% | Direct verified attendance percentage ($0 - 100\%$) |
| **LMS Learning Activity** | 10% | $0.7 \times \text{Assignment Completion\%} + 0.3 \times \min(100, \frac{\text{Logins}}{15} \times 100)$ |
| **Placement Readiness** | 20% | $0.35 \times \text{Coding\%} + 0.30 \times \text{Aptitude\%} + 0.25 \times \text{Mock\%} + 0.10 \times \text{Resume (100 if Yes else 30)}$ |
| **Skills Rubrics** | 10% | Arithmetic mean of Technical, Problem Solving & Communication assessment rubrics |
| **Campus Engagement** | 5% | $\min(100, \text{Events} \times 15 + \text{Clubs} \times 20 + \text{Certs} \times 25)$ |
| **Feedback Pulse** | 5% | Normalized mean of student pulse & faculty feedback: $\frac{\text{Rating} - 1}{4} \times 100$ |

### Dynamic Weight Re-normalization
When indicators are non-applicable (e.g. 1st-year students who have not yet undertaken placement assessments) or temporarily missing, the system **never assumes a zero score**. Instead, applicable weights are dynamically re-scaled:
$$w_i' = \frac{w_i}{\sum_{j \in \mathcal{A}} w_j}, \quad \text{Composite Score} = \sum_{i \in \mathcal{A}} (S_i \times w_i')$$

If data completeness falls below 35%, the platform displays an explicit **Insufficient Data** badge to maintain algorithmic trust.

### Score Interpretation Bands
- **80.0 – 100.0:** Strong Progress (Honors track, peer mentor, research recommendation)
- **65.0 – 79.9:** On Track / Monitor (Routine proctor review)
- **50.0 – 64.9:** Needs Support (Targeted subject assistance or attendance counseling)
- **Below 50.0:** Priority Support (High-priority multimodal intervention plan)

---

## 7. Dual Risk Engine & Diagnostic Rules

### Academic Support Signals
- **Critical Attendance:** Attendance $< 65\%$ (or below $75\%$ statutory minimum)
- **Active Backlogs:** $\ge 2$ active backlogs is classified as High Risk; $1$ backlog as Medium Risk
- **Academic Deficit:** Composite academic subscore $< 40/100$ or CGPA $< 5.0$
- **Low Composite Score:** Success score $< 50/100$ triggers immediate academic review

### Placement Readiness Signals (Year 3 & 4)
- **Coding Benchmark:** Coding assessment $< 40\%$ is High Risk; $< 50\%$ is Medium Risk
- **Interview Gap:** Mock interview score $< 45\%$ triggers communication workshop
- **Aptitude Deficit:** Aptitude score $< 45\%$ assigns quantitative problem sets
- **Resume Status:** Unverified or unapproved resume flags career services consultation

---

## 8. Responsible AI, Privacy & Demo Data Notice

- **Decision-Support Indicator:** All scores and risk classifications are decision-support aids designed to empower faculty mentors in having empathetic, timely check-ins. They are not automated high-stakes determinations.
- **Fairness & Non-Discrimination:** Protected personal attributes (gender, caste, religion, disability, socioeconomic background) are strictly excluded from data ingestion and calculation models.
- **Human-in-the-Loop:** Interventions must be validated and assigned to an authorized mentor or faculty advisor.
- **Synthetic Data Notice:** All 150 student records in `data/sample_students.csv` are 100% synthetically generated for the HacXLerate 2026 hackathon demonstration.

---

## 9. Evaluation Criteria Mapping (KPMG in India — HacXLerate 2026)

| Challenge Criterion | Weight | Implementation in Platform |
|---|---:|---|
| **Data Integration & Analysis** | 30% | Integrates 7 distinct domains into unified schema, handles missing/N/A values, validates ranges, detects duplicates, and supports CSV uploads. |
| **Success Score & Risk Identification** | 25% | Fully documented mathematical formula, dynamic re-normalization, dual early-warning risk engine with plain-language trigger attribution. |
| **Dashboard & Visualization** | 25% | Interactive Plotly dashboards, multi-page Streamlit application, cohort filters, radar subscore visualizer, and SQLite action tracking. |
| **Problem Understanding** | 10% | Solves data fragmentation with actionable "What / Why / What Action" tripartite paradigm tailored to Admin, Mentor, and Placement roles. |
| **Presentation & Demo Flow** | 10% | Clean professional UI tokens, seeded realistic demo personas, instantaneous execution, and 3-5 minute judge demo script. |

---

## 10. Judge Demonstration Flow (3–5 Minutes)

1. **The Problem (30 sec):** Point out how colleges struggle with fragmented data across LMS, attendance registers, and placement drives.
2. **Unified Data & Executive Overview (60 sec):** Show `app.py` or `1_Overview.py` with campus KPIs, success score distribution, and department breakdown.
3. **Deep-Dive Explainability (60 sec):** Open `2_Student_Explorer.py`, select a student (e.g. `STU-2026-007`), show the 7-domain radar chart and explain *why* the score was assigned.
4. **Targeted Segmentation (45 sec):** Navigate to `4_Segments.py`, show the *Strong Academics, Low Placement Readiness* segment to demonstrate differentiated intervention strategies.
5. **Closing the Loop (45 sec):** Go to `5_Interventions.py`, log an action plan for a student, update its status from *In Progress* to *Completed*, and show persistence in SQLite.
6. **Methodology & Ethics (30 sec):** Conclude on `6_Data_Methodology.py` showing the mathematical formula, dynamic re-normalization, and responsible AI governance.
