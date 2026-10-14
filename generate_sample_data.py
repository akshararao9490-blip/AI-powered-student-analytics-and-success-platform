"""
Synthetic Data Generator for Smart Campus Analytics Platform
Creates 150 realistic, diverse demo student records covering all risk categories and cohorts.
"""

import os
import random
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

FIRST_NAMES = [
    "Aarav", "Aditi", "Advait", "Akash", "Ananya", "Aniket", "Anushka", "Arjun",
    "Ayush", "Bhavya", "Chetan", "Dev", "Divya", "Diya", "Gaurav", "Harsh",
    "Ishaan", "Jhanvi", "Kabir", "Kavya", "Karan", "Kunal", "Manish", "Meera",
    "Mohit", "Neha", "Nikhil", "Nisha", "Pranav", "Pooja", "Rahul", "Riya",
    "Rohan", "Saanvi", "Sahil", "Sakshi", "Samarth", "Sneha", "Tanvi", "Tarun",
    "Utkarsh", "Varun", "Vidya", "Vikram", "Yash", "Zara", "Karthik", "Swati",
    "Gautam", "Lavanya", "Siddharth", "Priyanka", "Deepak", "Shreya", "Abhishek"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Rao", "Gupta",
    "Singh", "Mehta", "Joshi", "Bhat", "Deshmukh", "Kulkarni", "Chopra",
    "Kapoor", "Chatterjee", "Banerjee", "Menon", "Pillai", "Das", "Roy",
    "Sen", "Kumar", "Choudhury", "Narayanan", "Murthy", "Krishnan", "Malhotra"
]

DEPARTMENTS = [
    "Computer Science & Engineering",
    "Information Technology",
    "Electronics & Communication",
    "Data Science",
    "Mechanical Engineering",
    "Civil Engineering"
]

records = []

for i in range(1, 151):
    student_id = f"STU-2026-{i:03d}"
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    student_name = f"{first} {last}"
    dept = random.choice(DEPARTMENTS)

    # Distribute across academic years:
    # 1: 20%, 2: 25%, 3: 30%, 4: 25%
    year_roll = random.random()
    if year_roll < 0.20:
        year = 1
        sem = random.choice([1, 2])
    elif year_roll < 0.45:
        year = 2
        sem = random.choice([3, 4])
    elif year_roll < 0.75:
        year = 3
        sem = random.choice([5, 6])
    else:
        year = 4
        sem = random.choice([7, 8])

    # Distinct student persona types:
    # 0: High Achiever / Well-Rounded (30%)
    # 1: Strong Academic, Low Placement (15%) - Year 3/4 only
    # 2: Attendance Shortage (15%)
    # 3: Academic Recovery / Backlogs (15%)
    # 4: Low LMS Activity (10%)
    # 5: Skills Gap (10%)
    # 6: Insufficient Data demo (5%)
    persona_type = random.choices(
        [0, 1, 2, 3, 4, 5, 6],
        weights=[30, 15, 15, 15, 10, 10, 5],
        k=1
    )[0]

    # Force persona 1 to only be Year 3 or 4
    if persona_type == 1 and year < 3:
        year = random.choice([3, 4])
        sem = random.choice([5, 6, 7, 8])

    # Default profile values
    cgpa = round(np.random.normal(7.6, 0.8), 2)
    internal = round(np.random.normal(74, 10), 1)
    backlogs = 0
    subject_perf = round(np.random.normal(75, 9), 1)
    attendance = round(np.random.normal(82, 7), 1)
    lms_logins = round(max(0.5, np.random.normal(8.5, 3.0)), 1)
    assignment = round(np.random.normal(82, 10), 1)
    events = random.randint(1, 5)
    clubs = random.randint(1, 4)
    certs = random.randint(0, 3)

    tech_skill = round(np.random.normal(72, 11), 1)
    comm_skill = round(np.random.normal(75, 10), 1)
    prob_skill = round(np.random.normal(73, 11), 1)

    stu_feed = round(max(1.0, min(5.0, np.random.normal(4.0, 0.6))), 1)
    fac_feed = round(max(1.0, min(5.0, np.random.normal(4.1, 0.5))), 1)

    aptitude = round(np.random.normal(72, 12), 1)
    coding = round(np.random.normal(70, 14), 1)
    mock = round(np.random.normal(74, 11), 1)
    resume = "Yes"

    if persona_type == 0:  # Well rounded / High performer
        cgpa = round(np.random.uniform(8.4, 9.7), 2)
        internal = round(np.random.uniform(82.0, 96.0), 1)
        subject_perf = round(np.random.uniform(80.0, 95.0), 1)
        attendance = round(np.random.uniform(85.0, 97.0), 1)
        lms_logins = round(np.random.uniform(9.0, 16.0), 1)
        assignment = round(np.random.uniform(85.0, 99.0), 1)
        coding = round(np.random.uniform(75.0, 95.0), 1)
        aptitude = round(np.random.uniform(78.0, 94.0), 1)
        mock = round(np.random.uniform(78.0, 95.0), 1)
        tech_skill = round(np.random.uniform(80.0, 95.0), 1)
        comm_skill = round(np.random.uniform(80.0, 96.0), 1)
        prob_skill = round(np.random.uniform(82.0, 96.0), 1)
        events = random.randint(3, 7)
        clubs = random.randint(2, 5)
        certs = random.randint(2, 5)
        resume = "Yes"

    elif persona_type == 1:  # Strong Academic, Low Placement
        cgpa = round(np.random.uniform(8.3, 9.4), 2)
        internal = round(np.random.uniform(80.0, 92.0), 1)
        subject_perf = round(np.random.uniform(78.0, 91.0), 1)
        attendance = round(np.random.uniform(82.0, 94.0), 1)
        lms_logins = round(np.random.uniform(7.0, 12.0), 1)
        assignment = round(np.random.uniform(80.0, 95.0), 1)
        coding = round(np.random.uniform(28.0, 44.0), 1)
        aptitude = round(np.random.uniform(42.0, 58.0), 1)
        mock = round(np.random.uniform(35.0, 48.0), 1)
        tech_skill = round(np.random.uniform(50.0, 62.0), 1)
        comm_skill = round(np.random.uniform(45.0, 58.0), 1)
        prob_skill = round(np.random.uniform(55.0, 68.0), 1)
        resume = random.choice(["No", "Yes"])

    elif persona_type == 2:  # Attendance Shortage
        attendance = round(np.random.uniform(52.0, 71.5), 1)
        cgpa = round(np.random.uniform(6.5, 8.2), 2)
        internal = round(np.random.uniform(60.0, 78.0), 1)
        lms_logins = round(np.random.uniform(3.0, 7.0), 1)
        fac_feed = round(np.random.uniform(2.5, 3.4), 1)

    elif persona_type == 3:  # Academic Recovery / Backlogs
        backlogs = random.choice([1, 2, 3])
        cgpa = round(np.random.uniform(4.8, 6.2), 2)
        internal = round(np.random.uniform(36.0, 48.0), 1)
        subject_perf = round(np.random.uniform(38.0, 49.0), 1)
        attendance = round(np.random.uniform(62.0, 74.0), 1)
        fac_feed = round(np.random.uniform(2.0, 3.2), 1)

    elif persona_type == 4:  # Low LMS Engagement
        lms_logins = round(np.random.uniform(0.5, 2.5), 1)
        assignment = round(np.random.uniform(35.0, 55.0), 1)
        events = 0
        clubs = 0
        certs = 0

    elif persona_type == 5:  # Skills Gap
        tech_skill = round(np.random.uniform(35.0, 50.0), 1)
        coding = round(np.random.uniform(32.0, 46.0), 1)
        prob_skill = round(np.random.uniform(38.0, 52.0), 1)
        comm_skill = round(np.random.uniform(42.0, 56.0), 1)

    elif persona_type == 6:  # Insufficient Data Demo
        cgpa = None
        attendance = None
        coding = None
        aptitude = None
        mock = None
        resume = None

    # For Year 1 and 2, placement data is typically N/A
    if year in (1, 2) and persona_type != 6:
        aptitude = None
        coding = None
        mock = None
        resume = None

    # Safety clamp all values
    row = {
        "student_id": student_id,
        "student_name": student_name,
        "department": dept,
        "academic_year": year,
        "semester": sem,
        "cgpa": cgpa if cgpa is not None else "",
        "internal_marks_pct": min(100.0, max(0.0, internal)) if internal is not None else "",
        "backlog_count": backlogs if backlogs is not None else "",
        "subject_performance_pct": min(100.0, max(0.0, subject_perf)) if subject_perf is not None else "",
        "attendance_pct": min(100.0, max(0.0, attendance)) if attendance is not None else "",
        "lms_logins_per_week": min(50.0, max(0.0, lms_logins)) if lms_logins is not None else "",
        "assignment_completion_pct": min(100.0, max(0.0, assignment)) if assignment is not None else "",
        "events_participated": events if events is not None else "",
        "clubs_or_hackathons": clubs if clubs is not None else "",
        "certifications_count": certs if certs is not None else "",
        "aptitude_score_pct": min(100.0, max(0.0, aptitude)) if aptitude is not None else "",
        "coding_score_pct": min(100.0, max(0.0, coding)) if coding is not None else "",
        "mock_interview_pct": min(100.0, max(0.0, mock)) if mock is not None else "",
        "resume_ready": resume if resume is not None else "",
        "technical_skill_pct": min(100.0, max(0.0, tech_skill)) if tech_skill is not None else "",
        "communication_skill_pct": min(100.0, max(0.0, comm_skill)) if comm_skill is not None else "",
        "problem_solving_pct": min(100.0, max(0.0, prob_skill)) if prob_skill is not None else "",
        "student_feedback_score": min(5.0, max(1.0, stu_feed)) if stu_feed is not None else "",
        "faculty_feedback_score": min(5.0, max(1.0, fac_feed)) if fac_feed is not None else "",
    }
    records.append(row)

out_df = pd.DataFrame(records)
os.makedirs("data", exist_ok=True)
out_df.to_csv("data/sample_students.csv", index=False)
print(f"Generated {len(out_df)} synthetic student records in data/sample_students.csv")
