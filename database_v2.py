"""
Enterprise Database Schema v2
Normalized, scalable structure following university ERP standards
With Anna University CGPA calculation support
"""

import mysql.connector
from mysql.connector import Error, pooling
from datetime import datetime

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Root@123',
    'database': 'student_management_v2'
}

# Connection Pool Configuration - PERFORMANCE OPTIMIZATION
POOL_CONFIG = {
    **DB_CONFIG,
    'pool_name': 'student_pool',
    'pool_size': 10,  # Number of connections to keep ready
    'pool_reset_session': True
}

# Initialize connection pool (lazy initialization)
_connection_pool = None

def _get_pool():
    """Get or create connection pool (singleton pattern)"""
    global _connection_pool
    if _connection_pool is None:
        try:
            _connection_pool = pooling.MySQLConnectionPool(**POOL_CONFIG)
            print("✅ Connection pool created with 10 connections")
        except Error as e:
            print(f"Error creating connection pool: {e}")
            return None
    return _connection_pool

# Anna University Grading Scale
GRADE_SCALE = {
    'O': {'min': 91, 'max': 100, 'points': 10, 'description': 'Outstanding'},
    'A+': {'min': 81, 'max': 90, 'points': 9, 'description': 'Excellent'},
    'A': {'min': 71, 'max': 80, 'points': 8, 'description': 'Very Good'},
    'B+': {'min': 61, 'max': 70, 'points': 7, 'description': 'Good'},
    'B': {'min': 56, 'max': 60, 'points': 6, 'description': 'Above Average'},
    'C': {'min': 50, 'max': 55, 'points': 5, 'description': 'Average'},
    'RA': {'min': 0, 'max': 49, 'points': 0, 'description': 'Reappear'}
}

def get_grade(marks):
    """Get grade and grade points from marks"""
    for grade, info in GRADE_SCALE.items():
        if info['min'] <= marks <= info['max']:
            return grade, info['points']
    return 'RA', 0

def calculate_cgpa(grades_with_credits):
    """
    Calculate CGPA using Anna University formula
    grades_with_credits: list of (credits, grade_points)
    CGPA = Σ(Credit × Grade Point) / Σ(Credits)
    """
    total_credit_points = sum(c * gp for c, gp in grades_with_credits)
    total_credits = sum(c for c, gp in grades_with_credits)
    if total_credits == 0:
        return 0.0
    return round(total_credit_points / total_credits, 2)

def get_db_connection():
    """Get connection from pool (much faster than creating new connection)"""
    pool = _get_pool()
    if pool:
        try:
            return pool.get_connection()
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            # Fallback to direct connection
            try:
                return mysql.connector.connect(**DB_CONFIG)
            except Error as e2:
                print(f"Fallback connection failed: {e2}")
                return None
    # If pool not available, create direct connection
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database with normalized schema"""
    # Create database if not exists
    try:
        config_no_db = DB_CONFIG.copy()
        db_name = config_no_db.pop('database')
        conn = mysql.connector.connect(**config_no_db)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error creating database: {e}")

    conn = get_db_connection()
    if not conn:
        return
        
    cursor = conn.cursor()
    
    # 1. Roles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Users Table (Authentication)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role_id INT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            is_approved BOOLEAN DEFAULT FALSE,
            last_login TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')
    
    # 3. Departments Master Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            degree_type VARCHAR(50) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    ''')
    
    # 4. Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number VARCHAR(20) PRIMARY KEY,
            user_id INT UNIQUE,
            name VARCHAR(255) NOT NULL,
            department_id INT NOT NULL,
            admission_year INT NOT NULL,
            current_semester INT DEFAULT 1,
            email VARCHAR(100),
            phone VARCHAR(20),
            gender ENUM('Male', 'Female', 'Other'),
            dob DATE,
            address TEXT,
            guardian_name VARCHAR(255),
            guardian_phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            INDEX idx_dept (department_id),
            INDEX idx_year (admission_year),
            INDEX idx_semester (current_semester)
        )
    ''')
    
    # 5. Staffs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staffs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            name VARCHAR(255) NOT NULL,
            department_id INT,
            designation VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            qualification VARCHAR(255),
            experience_years INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            INDEX idx_dept (department_id)
        )
    ''')
    
    # 6. Subjects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            department_id INT NOT NULL,
            semester INT NOT NULL,
            credits INT NOT NULL,
            subject_type ENUM('Theory', 'Lab', 'Project') DEFAULT 'Theory',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            INDEX idx_dept_sem (department_id, semester)
        )
    ''')
    
    # 7. Assessments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            short_name VARCHAR(20) NOT NULL,
            max_marks INT NOT NULL,
            weightage DECIMAL(5,2) DEFAULT 0,
            description VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 8. Student Marks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_roll VARCHAR(20) NOT NULL,
            subject_id INT NOT NULL,
            assessment_id INT NOT NULL,
            academic_year VARCHAR(10) NOT NULL,
            marks_obtained DECIMAL(5,2),
            remarks VARCHAR(255),
            entered_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (student_roll) REFERENCES students(roll_number) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (assessment_id) REFERENCES assessments(id),
            FOREIGN KEY (entered_by) REFERENCES users(id),
            UNIQUE KEY unique_mark (student_roll, subject_id, assessment_id, academic_year),
            INDEX idx_student (student_roll),
            INDEX idx_subject (subject_id),
            INDEX idx_year (academic_year)
        )
    ''')
    
    # 9. Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_roll VARCHAR(20) NOT NULL,
            subject_id INT NOT NULL,
            date DATE NOT NULL,
            period INT,
            status ENUM('Present', 'Absent', 'OD', 'Leave') DEFAULT 'Present',
            marked_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_roll) REFERENCES students(roll_number) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (marked_by) REFERENCES users(id),
            UNIQUE KEY unique_attendance (student_roll, subject_id, date, period),
            INDEX idx_student (student_roll),
            INDEX idx_date (date),
            INDEX idx_subject (subject_id)
        )
    ''')
    
    # 10. Semester Results Table (for CGPA calculation)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS semester_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_roll VARCHAR(20) NOT NULL,
            subject_id INT NOT NULL,
            academic_year VARCHAR(10) NOT NULL,
            semester INT NOT NULL,
            internal_marks DECIMAL(5,2),
            external_marks DECIMAL(5,2),
            total_marks DECIMAL(5,2),
            grade VARCHAR(5),
            grade_point DECIMAL(3,1),
            credits INT,
            result ENUM('Pass', 'Fail', 'Arrear', 'Withheld') DEFAULT 'Pass',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (student_roll) REFERENCES students(roll_number) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            UNIQUE KEY unique_result (student_roll, subject_id, academic_year),
            INDEX idx_student (student_roll),
            INDEX idx_semester (semester),
            INDEX idx_year (academic_year)
        )
    ''')
    
    conn.commit()
    print("✅ All tables created successfully!")
    
    # Seed default data
    _seed_defaults(cursor, conn)
    
    cursor.close()
    conn.close()

def _seed_defaults(cursor, conn):
    """Seed default roles, departments, and assessment types"""
    
    # Roles
    roles = [
        ('ADMIN', 'System Administrator with full access'),
        ('STAFF', 'Teaching and non-teaching staff'),
        ('STUDENT', 'Student with limited access')
    ]
    for name, desc in roles:
        cursor.execute('''
            INSERT IGNORE INTO roles (name, description) VALUES (%s, %s)
        ''', (name, desc))
    
    # Departments
    departments = [
        ('AG', 'Agricultural Engineering', 'B.E'),
        ('BME', 'Biomedical Engineering', 'B.E'),
        ('BT', 'Biotechnology', 'B.Tech'),
        ('CE', 'Civil Engineering', 'B.E'),
        ('CSE', 'Computer Science and Engineering', 'B.E'),
        ('EEE', 'Electrical and Electronics Engineering', 'B.E'),
        ('ECE', 'Electronics and Communication Engineering', 'B.E'),
        ('FT', 'Food Technology', 'B.Tech'),
        ('IT', 'Information Technology', 'B.Tech'),
        ('ME', 'Mechanical Engineering', 'B.E'),
        ('AML', 'Artificial Intelligence and Machine Learning', 'B.Tech'),
        ('ADS', 'Artificial Intelligence and Data Science', 'B.Tech')
    ]
    for code, name, degree in departments:
        cursor.execute('''
            INSERT IGNORE INTO departments (code, name, degree_type) VALUES (%s, %s, %s)
        ''', (code, name, degree))
    
    # Assessment Types
    assessments = [
        ('CAT-1', 'CAT1', 50, 15, 'Continuous Assessment Test 1'),
        ('CAT-2', 'CAT2', 50, 15, 'Continuous Assessment Test 2'),
        ('CAT-3 (Model)', 'CAT3', 100, 20, 'Model Examination'),
        ('Assignment', 'ASGN', 20, 10, 'Assignments and Tutorials'),
        ('Lab Internal', 'LAB', 50, 20, 'Lab Internal Assessment'),
        ('Attendance', 'ATT', 100, 5, 'Attendance Marks'),
        ('University Exam', 'UNI', 100, 75, 'End Semester University Examination')
    ]
    for name, short, max_m, weight, desc in assessments:
        cursor.execute('''
            INSERT IGNORE INTO assessments (name, short_name, max_marks, weightage, description) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, short, max_m, weight, desc))
    
    # Create default admin user
    cursor.execute('SELECT id FROM roles WHERE name = %s', ('ADMIN',))
    admin_role = cursor.fetchone()
    if admin_role:
        cursor.execute('''
            INSERT IGNORE INTO users (username, password_hash, role_id, is_active, is_approved) 
            VALUES (%s, %s, %s, %s, %s)
        ''', ('admin', '123', admin_role[0], True, True))
        
        # Create admin staff profile
        cursor.execute('SELECT id FROM users WHERE username = %s', ('admin',))
        admin_user = cursor.fetchone()
        if admin_user:
            cursor.execute('''
                INSERT IGNORE INTO staffs (user_id, name, designation) 
                VALUES (%s, %s, %s)
            ''', (admin_user[0], 'Administrator', 'System Admin'))
    
    # Create default teacher user
    cursor.execute('SELECT id FROM roles WHERE name = %s', ('STAFF',))
    staff_role = cursor.fetchone()
    if staff_role:
        cursor.execute('''
            INSERT IGNORE INTO users (username, password_hash, role_id, is_active, is_approved) 
            VALUES (%s, %s, %s, %s, %s)
        ''', ('teacher', '123', staff_role[0], True, True))
        
        # Create teacher staff profile
        cursor.execute('SELECT id FROM users WHERE username = %s', ('teacher',))
        teacher_user = cursor.fetchone()
        if teacher_user:
            cursor.execute('''
                INSERT IGNORE INTO staffs (user_id, name, designation) 
                VALUES (%s, %s, %s)
            ''', (teacher_user[0], 'Sample Teacher', 'Assistant Professor'))
    
    # Create default student user
    cursor.execute('SELECT id FROM roles WHERE name = %s', ('STUDENT',))
    student_role = cursor.fetchone()
    cursor.execute('SELECT id FROM departments WHERE code = %s', ('CSE',))
    cse_dept = cursor.fetchone()
    
    if student_role and cse_dept:
        cursor.execute('''
            INSERT IGNORE INTO users (username, password_hash, role_id, is_active, is_approved) 
            VALUES (%s, %s, %s, %s, %s)
        ''', ('student', '123', student_role[0], True, True))
        
        # Create student profile
        cursor.execute('SELECT id FROM users WHERE username = %s', ('student',))
        student_user = cursor.fetchone()
        if student_user:
            cursor.execute('''
                INSERT IGNORE INTO students (roll_number, user_id, name, department_id, admission_year, current_semester) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', ('22CSE001', student_user[0], 'Sample Student', cse_dept[0], 2022, 1))
    
    conn.commit()
    print("✅ Default data seeded (roles, departments, assessments, admin, teacher, student)")

def get_departments():
    """Get all departments as dict {code: full_name}"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT code, name, degree_type FROM departments WHERE is_active = TRUE')
    depts = cursor.fetchall()
    cursor.close()
    conn.close()
    return {d['code']: f"{d['degree_type']} - {d['name']}" for d in depts}

def get_department_by_code(code):
    """Get department details by code"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM departments WHERE code = %s', (code,))
    dept = cursor.fetchone()
    cursor.close()
    conn.close()
    return dept

def get_student_cgpa(roll_number):
    """Calculate CGPA for a student"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT sr.grade_point, s.credits
        FROM semester_results sr
        JOIN subjects s ON sr.subject_id = s.id
        WHERE sr.student_roll = %s AND sr.result = 'Pass'
    ''', (roll_number,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not results:
        return 0.0
    
    grades_with_credits = [(r['credits'], float(r['grade_point'])) for r in results]
    return calculate_cgpa(grades_with_credits)

def get_semester_gpa(roll_number, semester, academic_year):
    """Calculate GPA for a specific semester"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT sr.grade_point, s.credits
        FROM semester_results sr
        JOIN subjects s ON sr.subject_id = s.id
        WHERE sr.student_roll = %s 
        AND sr.semester = %s 
        AND sr.academic_year = %s
        AND sr.result = 'Pass'
    ''', (roll_number, semester, academic_year))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not results:
        return 0.0
    
    grades_with_credits = [(r['credits'], float(r['grade_point'])) for r in results]
    return calculate_cgpa(grades_with_credits)


if __name__ == '__main__':
    init_db()
    print("\n📊 Database initialized with enterprise schema!")
    print("   - 10 normalized tables created")
    print("   - Roles, Departments, Assessments seeded")
    print("   - Admin user created (admin / 123)")
