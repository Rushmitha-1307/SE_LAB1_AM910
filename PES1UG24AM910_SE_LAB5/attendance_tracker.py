
"""Track student attendance and export attendance reports."""

import csv
import os
import ssl
import zipfile
from pathlib import Path

import requests

STUDENTS = {}
ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = os.environ.get("ERP_API_KEY", "")
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Add a student to the attendance register."""
    STUDENTS[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and update the date register."""
    if roll_no not in STUDENTS:
        raise KeyError(f"Student {roll_no} does not exist.")

    if status not in {"P", "A", "L", "H"}:
        raise ValueError("Status must be P, A, L, or H.")

    if register is None:
        register = {}

    register.setdefault(date, []).append(roll_no)
    STUDENTS[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Return the percentage of recorded sessions marked present."""
    records = STUDENTS[roll_no]["records"]

    if not records:
        return 0

    present = sum(status == "P" for _, status in records)
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Check whether attendance meets the minimum requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return students below the minimum attendance threshold."""
    result = [
        roll_no
        for roll_no in STUDENTS
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return result or None


def has_long_absence(roll_no, days=3):
    """Check for consecutive recorded absences."""
    if days <= 0:
        return True

    statuses = [
        status for _, status in STUDENTS[roll_no]["records"]
    ]

    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Return the latest recorded date for a student."""
    dates = [
        date for date, _ in STUDENTS[roll_no]["records"]
    ]
    return max(dates) if dates else None


def _safe_csv_text(value):
    """Reduce spreadsheet-formula injection risk in exported text."""
    text_value = str(value)

    if text_value.startswith(("=", "+", "-", "@")):
        return "'" + text_value

    return text_value


def export_csv(path="attendance.csv"):
    """Export attendance percentages to a UTF-8 CSV file."""
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in STUDENTS.items():
            writer.writerow([
                _safe_csv_text(roll_no),
                _safe_csv_text(student["name"]),
                attendance_percentage(roll_no),
            ])

    return path


def sync_to_erp(roll_no):
    """Send a student's attendance percentage to the ERP service."""
    if not ERP_API_KEY:
        raise RuntimeError(
            "Set the ERP_API_KEY environment variable first."
        )

    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }

    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


def backup_reports():
    """Create a ZIP archive of CSV reports in the current directory."""
    csv_files = sorted(Path(".").glob("*.csv"))

    with zipfile.ZipFile(
        "reports_backup.zip",
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for csv_file in csv_files:
            archive.write(csv_file, arcname=csv_file.name)


def legacy_channel():
    """Create a TLS context using secure system defaults."""
    return ssl.create_default_context()


def run_job(command, shell=False):
    """Describe a reminder job without executing a shell command."""
    if shell:
        raise ValueError("Shell execution is not permitted.")

    if isinstance(command, str):
        command = [command]

    return {"command": command, "shell": False}


def schedule_reminders():
    """Describe the reminder command without shell execution."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the sample attendance-tracker demonstration."""
    add_student("R01", "Aditi")
    add_student(
        "R02",
        '=HYPERLINK("http://evil.example","Bharat")',
    )

    first_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]

    second_student_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-9-3", "P"),
    ]

    # Share one register so it records both students' entries.
    register = {}

    for date, status in first_student_records:
        mark_attendance("R01", date, status, register)

    for date, status in second_student_records:
        mark_attendance("R02", date, status, register)

    mark_attendance("R01", "2030-01-01", "P", register)

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        register["2026-09-01"],
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
