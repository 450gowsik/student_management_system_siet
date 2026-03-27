"""
Generate sample student database JSON for the dashboard.

Output:
- 12 departments
- 180 students per year
- 720 students total
- 2,880 academic records total
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


INSTITUTION_NAME = "Sri Shakthi Institute of Engineering & Technology"
DEFAULT_OUTPUT = Path(__file__).with_name("student_db_720.json")
RANDOM_SEED = 20260327


@dataclass(frozen=True)
class Department:
    id: int
    code: str
    name: str
    degree: str


DEPARTMENTS = [
    Department(1, "AG", "Agricultural Engineering", "B.E"),
    Department(2, "ADS", "Artificial Intelligence and Data Science", "B.Tech"),
    Department(3, "AML", "Artificial Intelligence and Machine Learning", "B.Tech"),
    Department(4, "BME", "Biomedical Engineering", "B.E"),
    Department(5, "BT", "Biotechnology", "B.Tech"),
    Department(6, "CE", "Civil Engineering", "B.E"),
    Department(7, "CSE", "Computer Science and Engineering", "B.E"),
    Department(8, "EEE", "Electrical and Electronics Engineering", "B.E"),
    Department(9, "ECE", "Electronics and Communication Engineering", "B.E"),
    Department(10, "FT", "Food Technology", "B.Tech"),
    Department(11, "IT", "Information Technology", "B.Tech"),
    Department(12, "ME", "Mechanical Engineering", "B.E"),
]

YEAR_CONFIGS = [
    {
        "year": 1,
        "year_label": "I",
        "admission_year": 2024,
        "current_semester": 2,
        "completed_semesters": [1],
    },
    {
        "year": 2,
        "year_label": "II",
        "admission_year": 2023,
        "current_semester": 4,
        "completed_semesters": [1, 2, 3],
    },
    {
        "year": 3,
        "year_label": "III",
        "admission_year": 2022,
        "current_semester": 6,
        "completed_semesters": [1, 2, 3, 4, 5],
    },
    {
        "year": 4,
        "year_label": "IV",
        "admission_year": 2021,
        "current_semester": 8,
        "completed_semesters": [1, 2, 3, 4, 5, 6, 7],
    },
]

MALE_FIRST_NAMES = [
    "Arun", "Vignesh", "Suriya", "Karthik", "Saravanan", "Rohith", "Kishore",
    "Bharath", "Dinesh", "Vikram", "Prabhu", "Ramesh", "Naveen", "Harish",
    "Mohan", "Senthil", "Ashwin", "Manoj", "Gokul", "Ajith",
]

FEMALE_FIRST_NAMES = [
    "Harini", "Keerthana", "Sowmiya", "Nivetha", "Mahalakshmi", "Deepa",
    "Saranya", "Lavanya", "Janani", "Priyanka", "Aarthi", "Meena",
    "Kavitha", "Shobana", "Ananya", "Divya", "Vaishnavi", "Sangeetha",
    "Indhu", "Bhavana",
]

LAST_NAMES = [
    "Ramasamy", "Rajendran", "Subramanian", "Murugesan", "Govindarajan",
    "Sivasubramanian", "Chandrasekaran", "Jayakumar", "Anbalagan",
    "Selvaraj", "Mahalingam", "Palanisamy", "Thangavel", "Kandasamy",
    "Venkatesan", "Ramamoorthy", "Krishnamurthy", "Soundararajan",
    "Periasamy", "Rajagopal",
]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def academic_year_for_semester(admission_year: int, semester: int) -> str:
    start_year = admission_year + ((semester - 1) // 2)
    return f"{start_year}-{start_year + 1}"


def build_student_dob(rng: random.Random, year_level: int) -> str:
    base_year = 2006 - (year_level - 1)
    start = date(base_year - 1, 1, 1)
    end = date(base_year, 12, 31)
    span = (end - start).days
    return (start + timedelta(days=rng.randint(0, span))).isoformat()


def build_created_at(rng: random.Random, admission_year: int) -> str:
    created_day = rng.randint(1, 30)
    created_time = datetime(admission_year, 6, created_day, 9, 0, 0)
    return created_time.isoformat()


def build_name(rng: random.Random, gender: str) -> str:
    if gender == "Male":
        first = rng.choice(MALE_FIRST_NAMES)
    else:
        first = rng.choice(FEMALE_FIRST_NAMES)
    return f"{first} {rng.choice(LAST_NAMES)}"


def build_phone(rng: random.Random) -> str:
    first = rng.choice(["9", "8", "7"])
    rest = "".join(str(rng.randint(0, 9)) for _ in range(9))
    return first + rest


def build_performance_profile(rng: random.Random, year_level: int, slot: int) -> float:
    base = 6.4 + (slot % 5) * 0.38 + rng.uniform(-0.35, 1.15)
    if slot in {1, 5, 9, 13}:
        base += 0.8
    if year_level == 4:
        base += 0.2
    return clamp(base, 6.1, 9.7)


def build_dataset() -> dict:
    rng = random.Random(RANDOM_SEED)
    students = []
    academic_records = []
    next_student_id = 1
    next_record_id = 1

    for config in YEAR_CONFIGS:
        for dept in DEPARTMENTS:
            for slot in range(1, 16):
                gender = rng.choice(["Male", "Female"])
                roll_number = f"{config['admission_year']}{dept.code}{slot:03d}"
                name = build_name(rng, gender)
                email = f"{roll_number.lower()}@siet.ac.in"
                student = {
                    "id": next_student_id,
                    "register_no": roll_number,
                    "name": name,
                    "department_id": dept.id,
                    "department_name": dept.name,
                    "department_code": dept.code,
                    "degree": dept.degree,
                    "year": config["year"],
                    "year_label": config["year_label"],
                    "semester": config["current_semester"],
                    "dob": build_student_dob(rng, config["year"]),
                    "gender": gender,
                    "email": email,
                    "phone": build_phone(rng),
                    "batch": config["admission_year"],
                    "created_at": build_created_at(rng, config["admission_year"]),
                }
                students.append(student)

                running_points = 0.0
                base_performance = build_performance_profile(rng, config["year"], slot)
                for sem_index, semester in enumerate(config["completed_semesters"], start=1):
                    semester_lift = (sem_index - 1) * rng.uniform(0.02, 0.12)
                    sgpa = clamp(
                        base_performance + semester_lift + rng.uniform(-0.45, 0.45),
                        6.0,
                        9.92,
                    )
                    running_points += sgpa
                    cgpa = round(running_points / sem_index, 2)
                    academic_records.append(
                        {
                            "id": next_record_id,
                            "student_id": next_student_id,
                            "student_roll": roll_number,
                            "semester": semester,
                            "academic_year": academic_year_for_semester(
                                config["admission_year"], semester
                            ),
                            "sgpa": round(sgpa, 2),
                            "cgpa": cgpa,
                            "status": "Pass",
                        }
                    )
                    next_record_id += 1

                next_student_id += 1

    return {
        "meta": {
            "institution": INSTITUTION_NAME,
            "total_students": len(students),
            "per_year": 180,
            "years": 4,
            "departments": len(DEPARTMENTS),
            "per_dept_per_year": 15,
            "academic_records": len(academic_records),
            "generated_on": datetime.now().strftime("%Y-%m-%d"),
        },
        "departments": [
            {
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "degree": dept.degree,
            }
            for dept in DEPARTMENTS
        ],
        "students": students,
        "academic_records": academic_records,
    }


def write_dataset(path: Path = DEFAULT_OUTPUT) -> Path:
    dataset = build_dataset()
    path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    output_path = write_dataset()
    print(f"Created {output_path} with sample dashboard data.")
