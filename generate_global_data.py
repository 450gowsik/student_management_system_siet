"""
Global Mass Data Generation Script
Populates ALL 12 departments with 8 semesters of academic history.
Total: ~2,880 students with full historical marks (~150,000+ data points).
"""

import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'gowsik',
    'database': 'student_management_v2'
}

# Anna University Grade Scale
GRADE_SCALE = {
    'O': {'min': 91, 'max': 100, 'points': 10},
    'A+': {'min': 81, 'max': 90, 'points': 9},
    'A': {'min': 71, 'max': 80, 'points': 8},
    'B+': {'min': 61, 'max': 70, 'points': 7},
    'B': {'min': 56, 'max': 60, 'points': 6},
    'C': {'min': 50, 'max': 55, 'points': 5},
    'RA': {'min': 0, 'max': 49, 'points': 0}
}

def get_grade(marks):
    for grade, info in GRADE_SCALE.items():
        if info['min'] <= marks <= info['max']:
            return grade, info['points']
    return 'RA', 0

FIRST_NAMES = ["Aarav", "Aditi", "Amit", "Ananya", "Bhanu", "Chetan", "Deepa", "Divya", "Esha", "Gaurav", 
               "Harini", "Ishaan", "Jiya", "Karan", "Leela", "Manoj", "Neha", "Om", "Pooja", "Rahul", 
               "Sana", "Tanmay", "Utkarsh", "Vidya", "Yash", "Zoya", "Arjun", "Kavita", "Siddharth", "Meera",
               "Rohan", "Sonal", "Vikram", "Priya", "Rishi", "Tara", "Varun", "Ishani", "Nakul", "Myra"]
LAST_NAMES = ["Sharma", "Verma", "Gupta", "Nair", "Iyer", "Patel", "Singh", "Reddy", "Choudhury", "Bose",
              "Das", "Mishra", "Joshi", "Kulkarni", "Deshmukh", "Pillai", "Menon", "Saxena", "Malhotra", "Kapoor",
              "Rao", "Shetty", "Nambiar", "Pandey", "Trivedi", "Shukla", "Agrawal", "Bhatt", "Dubey", "Goswami"]

def generate_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def run_global_generation():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 1. Setup metadata
        cursor.execute("SELECT id, code FROM departments WHERE is_active = 1")
        departments = cursor.fetchall()
        
        cursor.execute("SELECT id, short_name FROM assessments")
        assessments = {a['short_name']: a['id'] for a in cursor.fetchall()}
        
        cursor.execute("SELECT id FROM roles WHERE name = 'STUDENT'")
        student_role_id = cursor.fetchone()['id']
        
        admin_id = 1
        
        # Year configurations
        year_configs = [
            {'year_level': 4, 'admission_year': 2021, 'current_sem': 8, 'semesters': [1, 2, 3, 4, 5, 6, 7, 8]},
            {'year_level': 3, 'admission_year': 2022, 'current_sem': 6, 'semesters': [1, 2, 3, 4, 5, 6]},
            {'year_level': 2, 'admission_year': 2023, 'current_sem': 4, 'semesters': [1, 2, 3, 4]},
            {'year_level': 1, 'admission_year': 2024, 'current_sem': 2, 'semesters': [1, 2]}
        ]
        
        total_students = 0
        total_sem_results = 0
        
        print(f"🚀 Starting GLOBAL data expansion for {len(departments)} departments...")
        
        for dept in departments:
            dept_id = dept['id']
            dept_code = dept['code']
            print(f"\n🏢 Processing Department: {dept_code} ({dept['id']})")
            
            for config in year_configs:
                admission_year = config['admission_year']
                current_sem = config['current_sem']
                print(f"  📅 Year {config['year_level']} (Admission {admission_year})")
                
                for i in range(1, 61):
                    roll_no = f"{str(admission_year)[2:]}{dept_code}{str(i).zfill(3)}"
                    name = generate_random_name()
                    email = f"{roll_no.lower()}@srishakthi.ac.in"
                    
                    # Create User + Student (IGNORE if exists)
                    cursor.execute("INSERT IGNORE INTO users (username, password_hash, role_id, is_active, is_approved) VALUES (%s, %s, %s, %s, %s)",
                                   (roll_no, '123', student_role_id, True, True))
                    
                    cursor.execute("SELECT id FROM users WHERE username = %s", (roll_no,))
                    user_id = cursor.fetchone()['id']
                    
                    cursor.execute("""
                        INSERT IGNORE INTO students (roll_number, user_id, name, department_id, admission_year, current_semester, email, phone, gender, address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (roll_no, user_id, name, dept_id, admission_year, current_sem, email, '9876543210', random.choice(['Male', 'Female']), 'Coimbatore'))
                    
                    total_students += 1
                    
                    # Generate historical marks for each semester
                    for sem_num in config['semesters']:
                        # Calculate academic year for this semester
                        # e.g. 2021 Batch: Sem 1,2 is 2021-2022; Sem 3,4 is 2022-2023...
                        start_year = admission_year + (sem_num - 1) // 2
                        academic_year = f"{start_year}-{start_year + 1}"
                        
                        # Get subjects for this dept and semester
                        cursor.execute("SELECT id, credits FROM subjects WHERE department_id = %s AND semester = %s", (dept_id, sem_num))
                        subjects = cursor.fetchall()
                        
                        for subject in subjects:
                            subj_id = subject['id']
                            credits = subject['credits']
                            
                            # Random marks (leaning towards pass)
                            cat1 = random.uniform(35, 50)
                            cat2 = random.uniform(35, 50)
                            cat3 = random.uniform(70, 100)
                            asgn = random.uniform(16, 20)
                            att = random.uniform(80, 100)
                            univ = random.uniform(55, 95) if sem_num < current_sem else random.uniform(0, 95)
                            
                            # Scaling logic
                            cat_avg = (cat1 + cat2) / 2
                            internal = min(40, (cat_avg / 50 * 15) + (cat3 / 100 * 10) + (asgn / 20 * 5) + (att / 100 * 5))
                            external = (univ / 100 * 60)
                            total = round(internal + external)
                            grade, gp = get_grade(total)
                            result = 'Pass' if total >= 50 else 'Fail'
                            
                            # Batching is better, but simple executes for now for reliability
                            cursor.execute("""
                                INSERT INTO semester_results (student_roll, subject_id, academic_year, semester, internal_marks, external_marks, total_marks, grade, grade_point, credits, result)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE 
                                    internal_marks = VALUES(internal_marks),
                                    external_marks = VALUES(external_marks),
                                    total_marks = VALUES(total_marks),
                                    grade = VALUES(grade),
                                    grade_point = VALUES(grade_point),
                                    result = VALUES(result)
                            """, (roll_no, subj_id, academic_year, sem_num, internal, external, total, grade, gp, credits, result))
                            
                            total_sem_results += 1
                
                conn.commit() # Commit after each year group for stability
        
        print(f"\n✅ GLOBAL Data Expansion Complete!")
        print(f"📊 Total Students: {total_students}")
        print(f"📝 Total Semester Results (Historical): {total_sem_results}")
        
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    run_global_generation()
