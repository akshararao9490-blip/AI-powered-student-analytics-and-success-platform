"""
Smart Campus Analytics & Student Success Platform
Intervention Tracker Service — Persists and manages intervention lifecycle in SQLite.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "interventions.db")


def get_connection() -> sqlite3.Connection:
    """Returns SQLite database connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes interventions database table schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT,
            department TEXT,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            action TEXT NOT NULL,
            owner TEXT NOT NULL,
            target_timeline TEXT,
            status TEXT NOT NULL DEFAULT 'Planned',
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_intervention(
    student_id: str,
    category: str,
    priority: str,
    action: str,
    owner: str,
    student_name: str = "",
    department: str = "",
    target_timeline: str = "",
    status: str = "Planned",
    notes: str = ""
) -> int:
    """Adds a new student intervention record."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO interventions (
            student_id, student_name, department, category, priority,
            action, owner, target_timeline, status, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id, student_name, department, category, priority,
        action, owner, target_timeline, status, notes, now_str, now_str
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_intervention(
    intervention_id: int,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    owner: Optional[str] = None
) -> bool:
    """Updates status or notes for an intervention record."""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    updates = ["updated_at = ?"]
    params = [now_str]

    if status is not None:
        updates.append("status = ?")
        params.append(status)
    if notes is not None:
        updates.append("notes = ?")
        params.append(notes)
    if owner is not None:
        updates.append("owner = ?")
        params.append(owner)

    params.append(intervention_id)
    sql = f"UPDATE interventions SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount > 0
    conn.close()
    return affected


def get_all_interventions() -> List[Dict[str, Any]]:
    """Retrieves all tracked intervention records."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interventions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_interventions_for_student(student_id: str) -> List[Dict[str, Any]]:
    """Retrieves intervention records for a specific student."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interventions WHERE student_id = ? ORDER BY id DESC", (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def seed_demo_interventions_if_empty(students_records: List[Dict[str, Any]]) -> None:
    """Populates realistic initial intervention records for demo purposes."""
    init_db()
    existing = get_all_interventions()
    if existing:
        return

    # Find sample students needing support
    demo_samples = [
        {
            "student_id": "STU-2026-004",
            "student_name": "Aarav Sharma",
            "department": "Computer Science & Engineering",
            "category": "Attendance Counseling",
            "priority": "High",
            "action": "Proctor 1-on-1 counseling regarding medical leaves; established daily attendance card.",
            "owner": "Dr. R. Sundaram (Proctor)",
            "target_timeline": "Within 3 days",
            "status": "In Progress",
            "notes": "Student met with mentor; family notified. Commuting issue identified.",
        },
        {
            "student_id": "STU-2026-007",
            "student_name": "Divya Patel",
            "department": "Information Technology",
            "category": "Placement Technical Training",
            "priority": "High",
            "action": "Enrolled in 4-week intensive Python DSA bootcamp with daily coding submissions.",
            "owner": "Prof. Ananya Roy (Placement Cell)",
            "target_timeline": "Ongoing (Bi-weekly review)",
            "status": "In Progress",
            "notes": "Completed Week 1 arrays module. Scoring improved on portal test.",
        },
        {
            "student_id": "STU-2026-012",
            "student_name": "Rohan Verma",
            "department": "Electronics & Communication",
            "category": "Academic Remediation",
            "priority": "High",
            "action": "Remedial coaching for Signals & Systems backlog; assigned peer tutor.",
            "owner": "Dr. K. Narayanan",
            "target_timeline": "Within 7 days",
            "status": "Planned",
            "notes": "Scheduled first study group meeting for coming Friday.",
        },
        {
            "student_id": "STU-2026-015",
            "student_name": "Neha Gupta",
            "department": "Data Science",
            "category": "Interview Coaching",
            "priority": "Medium",
            "action": "Completed HR mock interview rehearsal; structured feedback provided on behavioral answers.",
            "owner": "Placement Soft-Skills Cell",
            "target_timeline": "Completed",
            "status": "Completed",
            "notes": "Score upgraded from 42% to 78% after 2 rehearsal rounds.",
        },
    ]

    for item in demo_samples:
        add_intervention(
            student_id=item["student_id"],
            student_name=item["student_name"],
            department=item["department"],
            category=item["category"],
            priority=item["priority"],
            action=item["action"],
            owner=item["owner"],
            target_timeline=item["target_timeline"],
            status=item["status"],
            notes=item["notes"]
        )
