"""
Student Management System - Flask Application
Enterprise Edition with Normalized Schema
Anna University CGPA Calculation
"""

from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
import database_v2 as database
import mysql.connector
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Email Configuration (SMTP)
# Configured for: gowsikbabubabu@gmail.com
EMAIL_CONFIG = {
    'SMTP_SERVER': 'smtp.gmail.com',
    'SMTP_PORT': 587,
    'SENDER_EMAIL': 'gowsikbabubabu@gmail.com',
    'SENDER_PASSWORD': 'fmyucsyfsiarkapn',  # App Password (no spaces)
    'SENDER_NAME': 'Student Management System',
    'ADMIN_EMAIL': 'gowsikbabubabu@gmail.com'  # Admin receives signup notifications
}

# Email Sending Function
def send_approval_email(user_email, user_name):
    """Send approval notification email to user"""
    if not user_email:
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Account Approval - Student Management System'
        msg['From'] = f"{EMAIL_CONFIG['SENDER_NAME']} <{EMAIL_CONFIG['SENDER_EMAIL']}>"
        msg['To'] = user_email
        
        # HTML email content - Formal institutional style
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.8; color: #2c3e50; background-color: #f4f4f4; margin: 0; padding: 0; }}
                    .email-container {{ max-width: 650px; margin: 40px auto; background: white; }}
                    .header {{ background: #1a365d; color: white; padding: 25px 40px; border-bottom: 4px solid #2563eb; }}
                    .header h2 {{ margin: 0; font-size: 20px; font-weight: 600; }}
                    .content {{ padding: 40px; }}
                    .content p {{ margin: 15px 0; color: #374151; }}
                    .info-box {{ background: #f8fafc; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; }}
                    .footer {{ background: #f9fafb; padding: 20px 40px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }}
                    .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h2>Student Management System</h2>
                        <div style="font-size: 13px; margin-top: 5px; opacity: 0.9;">Academic Information Services</div>
                    </div>
                    <div class="content">
                        <p>Dear {user_name},</p>
                        
                        <p>We are pleased to inform you that your account registration has been reviewed and <strong>approved</strong> by the system administrator.</p>
                        
                        <div class="info-box">
                            <p style="margin: 0;"><strong>Account Status:</strong> Active</p>
                            <p style="margin: 8px 0 0 0;"><strong>Access Level:</strong> Teacher</p>
                        </div>
                        
                        <p>You may now access the Student Management System using your registered credentials. Please visit the portal to log in and begin using the system.</p>
                        
                        <p><strong>Portal URL:</strong> <a href="http://localhost:5000/login" style="color: #2563eb;">http://localhost:5000/login</a></p>
                        
                        <p>If you experience any difficulties accessing your account or have questions regarding system usage, please contact the system administrator.</p>
                        
                        <div class="signature">
                            <p style="margin: 5px 0;">Regards,</p>
                            <p style="margin: 5px 0; font-weight: 600;">System Administrator</p>
                            <p style="margin: 5px 0; font-size: 13px; color: #6b7280;">Student Management System</p>
                        </div>
                    </div>
                    <div class="footer">
                        <p style="margin: 5px 0;">This is an automated notification from the Student Management System.</p>
                        <p style="margin: 5px 0;">Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text fallback
        text_content = f"""
STUDENT MANAGEMENT SYSTEM
Academic Information Services

{'='*60}

Dear {user_name},

We are pleased to inform you that your account registration has been reviewed and approved by the system administrator.

Account Status: Active
Access Level: Teacher

You may now access the Student Management System using your registered credentials. Please visit the portal to log in and begin using the system.

Portal URL: http://localhost:5000/login

If you experience any difficulties accessing your account or have questions regarding system usage, please contact the system administrator.

Regards,
System Administrator
Student Management System

{'='*60}

This is an automated notification from the Student Management System.
Please do not reply to this email.
        """
        
        # Attach both HTML and plain text versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['SMTP_SERVER'], EMAIL_CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['SENDER_EMAIL'], EMAIL_CONFIG['SENDER_PASSWORD'])
            server.send_message(msg)
        
        print(f"✓ Approval email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email to {user_email}: {str(e)}")
        return False

def send_deletion_email(user_email, user_name):
    """Send account deletion notification email to user"""
    if not user_email:
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Account Deactivation Notice - Student Management System'
        msg['From'] = f"{EMAIL_CONFIG['SENDER_NAME']} <{EMAIL_CONFIG['SENDER_EMAIL']}>"
        msg['To'] = user_email
        
        # HTML email content - Formal institutional style
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.8; color: #2c3e50; background-color: #f4f4f4; margin: 0; padding: 0; }}
                    .email-container {{ max-width: 650px; margin: 40px auto; background: white; }}
                    .header {{ background: #7f1d1d; color: white; padding: 25px 40px; border-bottom: 4px solid #dc2626; }}
                    .header h2 {{ margin: 0; font-size: 20px; font-weight: 600; }}
                    .content {{ padding: 40px; }}
                    .content p {{ margin: 15px 0; color: #374151; }}
                    .notice-box {{ background: #fef2f2; border-left: 4px solid #dc2626; padding: 20px; margin: 25px 0; }}
                    .footer {{ background: #f9fafb; padding: 20px 40px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }}
                    .signature {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h2>Student Management System</h2>
                        <div style="font-size: 13px; margin-top: 5px; opacity: 0.9;">Academic Information Services</div>
                    </div>
                    <div class="content">
                        <p>Dear {user_name},</p>
                        
                        <p>This message is to inform you that your account access to the Student Management System has been <strong>deactivated</strong> by the system administrator.</p>
                        
                        <div class="notice-box">
                            <p style="margin: 0;"><strong>Effective Date:</strong> Immediate</p>
                            <p style="margin: 8px 0 0 0;"><strong>Account Status:</strong> Deactivated</p>
                        </div>
                        
                        <p>As a result of this action, you will no longer have access to the system and its associated resources.</p>
                        
                        <p>If you believe this action was taken in error or require further clarification, please contact the system administrator at your earliest convenience.</p>
                        
                        <div class="signature">
                            <p style="margin: 5px 0;">Regards,</p>
                            <p style="margin: 5px 0; font-weight: 600;">System Administrator</p>
                            <p style="margin: 5px 0; font-size: 13px; color: #6b7280;">Student Management System</p>
                        </div>
                    </div>
                    <div class="footer">
                        <p style="margin: 5px 0;">This is an automated notification from the Student Management System.</p>
                        <p style="margin: 5px 0;">Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text fallback
        text_content = f"""
STUDENT MANAGEMENT SYSTEM
Academic Information Services

{'='*60}

Dear {user_name},

This message is to inform you that your account access to the Student Management System has been deactivated by the system administrator.

Effective Date: Immediate
Account Status: Deactivated

As a result of this action, you will no longer have access to the system and its associated resources.

If you believe this action was taken in error or require further clarification, please contact the system administrator at your earliest convenience.

Regards,
System Administrator
Student Management System

{'='*60}

This is an automated notification from the Student Management System.
Please do not reply to this email.
        """
        
        # Attach both HTML and plain text versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['SMTP_SERVER'], EMAIL_CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['SENDER_EMAIL'], EMAIL_CONFIG['SENDER_PASSWORD'])
            server.send_message(msg)
        
        print(f"✓ Deletion notification email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send deletion email to {user_email}: {str(e)}")
        return False

def send_admin_new_signup_notification(new_user_name, new_user_username, new_user_email):
    """Send notification to admin when a new teacher signs up"""
    admin_email = EMAIL_CONFIG.get('ADMIN_EMAIL')
    if not admin_email:
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'New Teacher Registration Pending Approval - Student Management System'
        msg['From'] = f"{EMAIL_CONFIG['SENDER_NAME']} <{EMAIL_CONFIG['SENDER_EMAIL']}>"
        msg['To'] = admin_email
        
        # HTML email content - Formal institutional style
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.8; color: #2c3e50; background-color: #f4f4f4; margin: 0; padding: 0; }}
                    .email-container {{ max-width: 650px; margin: 40px auto; background: white; }}
                    .header {{ background: #0f172a; color: white; padding: 25px 40px; border-bottom: 4px solid #3b82f6; }}
                    .header h2 {{ margin: 0; font-size: 20px; font-weight: 600; }}
                    .content {{ padding: 40px; }}
                    .content p {{ margin: 15px 0; color: #374151; }}
                    .applicant-details {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 25px; margin: 25px 0; }}
                    .applicant-details table {{ width: 100%; border-collapse: collapse; }}
                    .applicant-details td {{ padding: 8px 0; }}
                    .applicant-details td:first-child {{ font-weight: 600; width: 140px; color: #1e293b; }}
                    .action-button {{ display: inline-block; padding: 12px 28px; background: #3b82f6; color: white; text-decoration: none; border-radius: 4px; margin-top: 20px; font-weight: 500; }}
                    .footer {{ background: #f9fafb; padding: 20px 40px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h2>Student Management System</h2>
                        <div style="font-size: 13px; margin-top: 5px; opacity: 0.9;">Administrative Notification Service</div>
                    </div>
                    <div class="content">
                        <p><strong>New Teacher Registration</strong></p>
                        
                        <p>A new teacher account registration has been submitted and requires administrative review and approval.</p>
                        
                        <div class="applicant-details">
                            <table>
                                <tr>
                                    <td>Full Name:</td>
                                    <td>{new_user_name}</td>
                                </tr>
                                <tr>
                                    <td>Username:</td>
                                    <td>{new_user_username}</td>
                                </tr>
                                <tr>
                                    <td>Email Address:</td>
                                    <td>{new_user_email}</td>
                                </tr>
                                <tr>
                                    <td>Status:</td>
                                    <td><span style="color: #f59e0b; font-weight: 600;">Pending Approval</span></td>
                                </tr>
                            </table>
                        </div>
                        
                        <p>Please review the applicant's information and take appropriate action through the User Management portal.</p>
                        
                        <p style="margin-top: 25px;">
                            <a href="http://localhost:5000/admin/user-management" class="action-button">Access User Management</a>
                        </p>
                    </div>
                    <div class="footer">
                        <p style="margin: 5px 0;">This is an automated administrative notification from the Student Management System.</p>
                        <p style="margin: 5px 0;">Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text fallback
        text_content = f"""
STUDENT MANAGEMENT SYSTEM
Administrative Notification Service

{'='*60}

NEW TEACHER REGISTRATION

A new teacher account registration has been submitted and requires administrative review and approval.

APPLICANT DETAILS:
Full Name: {new_user_name}
Username: {new_user_username}
Email Address: {new_user_email}
Status: Pending Approval

Please review the applicant's information and take appropriate action through the User Management portal.

Portal URL: http://localhost:5000/admin/user-management

{'='*60}

This is an automated administrative notification from the Student Management System.
Please do not reply to this email.
        """
        
        # Attach both HTML and plain text versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['SMTP_SERVER'], EMAIL_CONFIG['SMTP_PORT']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['SENDER_EMAIL'], EMAIL_CONFIG['SENDER_PASSWORD'])
            server.send_message(msg)
        
        print(f"✓ Admin notification sent to {admin_email} for new signup: {new_user_username}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send admin notification: {str(e)}")
        return False

# Authentication Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'ADMIN':
            flash("Only admin can access this page.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] not in ['TEACHER', 'ADMIN']:
            if session.get('role') == 'STUDENT':
                return redirect(url_for('student_profile'))
            flash("Only teachers can access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'STUDENT':
            flash("Only students can access this page.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_student(roll_no):
    """Get a single student by roll_number from students table"""
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM students WHERE roll_number = %s', (roll_no,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student is None:
        abort(404)
    return student

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@login_required
@teacher_required
def index():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get all departments
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE ORDER BY name')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}
    
    # Get selected department from query param, default to first one
    selected_dept = request.args.get('dept', str(departments[0]['id']) if departments else '1')
    selected_year = request.args.get('year', 'all')
    selected_sem = request.args.get('sem', 'all')
    
    # OPTIMIZED: Single query to get students WITH their CGPA and Prev Sem Avg
    query = '''
        SELECT s.*, d.code as dept_code, d.name as dept_name,
               COALESCE(cgpa_calc.cgpa, 0) as cgpa,
               COALESCE(prev_sem.avg_marks, 0) as prev_sem_avg
        FROM students s
        JOIN departments d ON s.department_id = d.id
        LEFT JOIN (
            SELECT sr.student_roll,
                   ROUND(SUM(sr.grade_point * sr.credits) / NULLIF(SUM(sr.credits), 0), 2) as cgpa
            FROM semester_results sr
            WHERE sr.result = 'Pass'
            GROUP BY sr.student_roll
        ) cgpa_calc ON s.roll_number = cgpa_calc.student_roll
        LEFT JOIN (
            SELECT sr.student_roll, ROUND(AVG(sr.total_marks), 2) as avg_marks
            FROM semester_results sr
            JOIN students st ON sr.student_roll = st.roll_number
            WHERE sr.semester = st.current_semester - 1
            GROUP BY sr.student_roll
        ) prev_sem ON s.roll_number = prev_sem.student_roll
        WHERE s.department_id = %s
    '''
    params = [selected_dept]
    
    # Filter by year (each year has 2 semesters: I Year = 1,2; II Year = 3,4; etc.)
    if selected_year != 'all':
        year_num = int(selected_year)
        sem1 = (year_num - 1) * 2 + 1
        sem2 = (year_num - 1) * 2 + 2
        
        if selected_sem != 'all':
            # Specific semester within the year
            query += " AND s.current_semester = %s"
            params.append(selected_sem)
        else:
            # Both semesters of the year
            query += " AND s.current_semester IN (%s, %s)"
            params.extend([sem1, sem2])
    elif selected_sem != 'all':
        query += " AND s.current_semester = %s"
        params.append(selected_sem)
    
    query += " ORDER BY s.roll_number"

    cursor.execute(query, params)
    students = cursor.fetchall()
    
    # NO MORE N+1 QUERIES! CGPA is already calculated in the query above
    
    cursor.close()
    conn.close()
    
    return render_template('home.html', 
                           students=students, 
                           departments=dept_dict,
                           dept_list=departments,
                           selected_dept=selected_dept,
                           selected_year=selected_year,
                           selected_sem=selected_sem)

@app.route('/api/subjects/<int:dept_id>/<int:semester>')
@login_required
def get_subjects_api(dept_id, semester):
    """API endpoint to get subjects for a department and semester"""
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT id, code, name, credits, subject_type
        FROM subjects
        WHERE department_id = %s AND semester = %s AND is_active = TRUE
        ORDER BY subject_type, code
    ''', (dept_id, semester))
    subjects = cursor.fetchall()
    cursor.close()
    conn.close()
    return {'subjects': subjects}


@app.route('/create', methods=('GET', 'POST'))
@login_required
@teacher_required
def create():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get departments for form
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE ORDER BY name')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}
    
    # Get assessment type IDs
    cursor.execute('SELECT id, short_name FROM assessments')
    assessments = {a['short_name']: a['id'] for a in cursor.fetchall()}
    
    # Get current academic year
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    if current_month >= 6:
        academic_year = f"{current_year}-{current_year + 1}"
    else:
        academic_year = f"{current_year - 1}-{current_year}"
    
    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department_id']
        roll_number = request.form['roll_number']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        gender = request.form.get('gender', 'Male')
        admission_year = request.form.get('admission_year', 2024)
        current_semester = int(request.form.get('current_semester', 1))
        address = request.form.get('address', '')

        if not name or not roll_number or not department_id:
            flash('Name, Roll Number and Department are required!', 'danger')
        else:
            try:
                # Get student role id
                cursor.execute('SELECT id FROM roles WHERE name = %s', ('STUDENT',))
                role = cursor.fetchone()
                student_role_id = role['id'] if role else 3
                
                # Create user account first
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role_id, is_active, is_approved)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (roll_number, '123', student_role_id, True, True))
                user_id = cursor.lastrowid
                
                # Create student profile
                cursor.execute('''
                    INSERT INTO students (roll_number, user_id, name, department_id, admission_year, 
                    current_semester, email, phone, gender, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (roll_number, user_id, name, department_id, admission_year, 
                      current_semester, email, phone, gender, address))
                
                # Get subjects for this department and semester
                cursor.execute('''
                    SELECT id, credits FROM subjects 
                    WHERE department_id = %s AND semester = %s AND is_active = TRUE
                ''', (department_id, current_semester))
                subjects = cursor.fetchall()
                
                # Process marks for each subject if provided
                for subject in subjects:
                    subj_id = subject['id']
                    
                    # Get marks from form
                    cat1 = request.form.get(f'cat1_{subj_id}', '')
                    cat2 = request.form.get(f'cat2_{subj_id}', '')
                    cat3 = request.form.get(f'cat3_{subj_id}', '')
                    assignment = request.form.get(f'assignment_{subj_id}', '')
                    attendance = request.form.get(f'attendance_{subj_id}', '')
                    university = request.form.get(f'university_{subj_id}', '')
                    
                    # Skip if no marks entered for this subject
                    if not any([cat1, cat2, cat3, assignment, attendance, university]):
                        continue
                    
                    # Convert to float
                    cat1 = float(cat1) if cat1 else 0
                    cat2 = float(cat2) if cat2 else 0
                    cat3 = float(cat3) if cat3 else 0
                    assignment = float(assignment) if assignment else 0
                    attendance = float(attendance) if attendance else 0
                    university = float(university) if university else 0
                    
                    # Save individual marks
                    marks_data = [
                        (assessments.get('CAT1'), cat1),
                        (assessments.get('CAT2'), cat2),
                        (assessments.get('CAT3'), cat3),
                        (assessments.get('ASGN'), assignment),
                        (assessments.get('ATT'), attendance),
                        (assessments.get('UNI'), university),
                    ]
                    
                    for assess_id, marks in marks_data:
                        if assess_id and marks > 0:
                            cursor.execute('''
                                INSERT INTO student_marks 
                                (student_roll, subject_id, assessment_id, academic_year, marks_obtained, entered_by)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE marks_obtained = %s, entered_by = %s
                            ''', (roll_number, subj_id, assess_id, academic_year, marks, session['user_id'], marks, session['user_id']))
                    
                    # Calculate totals
                    cat_avg = (cat1 + cat2) / 2
                    cat_scaled = (cat_avg / 50) * 15
                    cat3_scaled = (cat3 / 100) * 10
                    assign_scaled = (assignment / 20) * 5
                    attend_scaled = (attendance / 100) * 5
                    internal_total = min(40, cat_scaled + cat3_scaled + assign_scaled + attend_scaled)
                    external_scaled = (university / 100) * 60
                    total = round(internal_total + external_scaled)
                    grade, grade_point = database.get_grade(total)
                    result_status = 'Pass' if total >= 50 else 'Fail'
                    
                    # Save to semester_results
                    cursor.execute('''
                        INSERT INTO semester_results 
                        (student_roll, subject_id, academic_year, semester, internal_marks, external_marks, 
                         total_marks, grade, grade_point, credits, result)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                        internal_marks = %s, external_marks = %s, total_marks = %s, 
                        grade = %s, grade_point = %s, result = %s
                    ''', (roll_number, subj_id, academic_year, current_semester, 
                          internal_total, external_scaled, total, grade, grade_point, 
                          subject['credits'], result_status,
                          internal_total, external_scaled, total, grade, grade_point, result_status))
                
                conn.commit()
                flash(f'Student "{name}" added successfully with marks!', 'success')
                cursor.close()
                conn.close()
                return redirect(url_for('index'))
            except mysql.connector.errors.IntegrityError as e:
                conn.rollback()
                flash(f'Error: Roll Number "{roll_number}" already exists!', 'danger')
            except Exception as e:
                conn.rollback()
                flash(f'Error: {str(e)}', 'danger')
    
    cursor.close()
    conn.close()
    return render_template('add_edit.html', departments=dept_dict, dept_list=departments)

@app.route('/<roll_no>/edit', methods=('GET', 'POST'))
@login_required
@teacher_required
def edit(roll_no):
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get student with department info
    cursor.execute('''
        SELECT s.*, d.id as dept_id, d.name as dept_name, d.degree_type
        FROM students s
        JOIN departments d ON s.department_id = d.id
        WHERE s.roll_number = %s
    ''', (roll_no,))
    student = cursor.fetchone()
    
    if not student:
        cursor.close()
        conn.close()
        abort(404)
    
    # Get departments for form
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE ORDER BY name')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}

    if request.method == 'POST':
        name = request.form['name']
        new_roll_number = request.form['roll_number']
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        gender = request.form.get('gender', 'Male')
        admission_year = request.form.get('admission_year', student['admission_year'])
        current_semester = request.form.get('current_semester', student['current_semester'])
        address = request.form.get('address', '')
        department_id = request.form.get('department_id', student['department_id'])

        cursor.execute('''
            UPDATE students SET name = %s, roll_number = %s, email = %s, phone = %s, 
            gender = %s, admission_year = %s, current_semester = %s, address = %s, department_id = %s
            WHERE roll_number = %s
        ''', (name, new_roll_number, email, phone, gender, admission_year, current_semester, address, department_id, roll_no))
        
        # Also update username in users table if roll number changed
        if new_roll_number != roll_no and student.get('user_id'):
            cursor.execute('UPDATE users SET username = %s WHERE id = %s', (new_roll_number, student['user_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash(f'Student "{name}" updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('add_edit.html', student=student, departments=dept_dict, dept_list=departments, current_dept=str(student['department_id']))

@app.route('/<roll_no>/view')
@login_required
@teacher_required
def view_student(roll_no):
    """View full student details (for teachers)"""
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT s.*, d.name as dept_name, d.degree_type, d.code as dept_code
        FROM students s
        JOIN departments d ON s.department_id = d.id
        WHERE s.roll_number = %s
    ''', (roll_no,))
    student = cursor.fetchone()
    
    if student is None:
        cursor.close()
        conn.close()
        abort(404)
    
    # Calculate CGPA
    student['cgpa'] = database.get_student_cgpa(roll_no)
    dept_name = f"{student['degree_type']} - {student['dept_name']}"
    
    # Fetch results for all 8 semesters
    all_semesters_results = []
    for sem in range(1, 9):
        cursor.execute('''
            SELECT sr.*, s.name as subject_name, s.credits
            FROM semester_results sr
            JOIN subjects s ON sr.subject_id = s.id
            WHERE sr.student_roll = %s AND sr.semester = %s
        ''', (roll_no, sem))
        results = cursor.fetchall()
        
        if results:
            total_points = sum(float(r['grade_point']) * r['credits'] for r in results)
            total_credits = sum(r['credits'] for r in results)
            sgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0
            
            all_semesters_results.append({
                'semester': sem,
                'results': results,
                'sgpa': sgpa,
                'has_arrears': any(r['result'] != 'Pass' for r in results)
            })
        else:
            all_semesters_results.append({
                'semester': sem,
                'results': [],
                'sgpa': 0,
                'has_arrears': False
            })
            
    cursor.close()
    conn.close()
    
    return render_template('view_student.html', 
                           student=student, 
                           dept_name=dept_name,
                           semester_results=all_semesters_results)

@app.route('/analytics')
@login_required
@teacher_required
def analytics():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get departments for filter
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE ORDER BY name')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}
    
    selected_dept = request.args.get('dept', 'all')
    selected_sem = request.args.get('sem', 'all')
    
    # Build base query with filters
    where_clauses = []
    params = []
    
    if selected_dept != 'all':
        where_clauses.append("s.department_id = %s")
        params.append(selected_dept)
    
    if selected_sem != 'all':
        where_clauses.append("s.current_semester = %s")
        params.append(selected_sem)
    
    where_clause = ""
    if where_clauses:
        where_clause = " WHERE " + " AND ".join(where_clauses)
    
    # Get summary stats (count and gender breakdown)
    cursor.execute(f'''
        SELECT 
            COUNT(*) as total_students
        FROM students s {where_clause}
    ''', params)
    summary = cursor.fetchone()
    summary['avg_cgpa'] = 0.0
    
    # Get department breakdown
    if selected_dept == 'all':
        cursor.execute('''
            SELECT 
                d.name as course,
                d.code,
                COUNT(*) as student_count
            FROM students s
            JOIN departments d ON s.department_id = d.id
            GROUP BY d.id, d.name, d.code
            ORDER BY d.name
        ''')
    else:
        cursor.execute(f'''
            SELECT 
                CONCAT('Semester ', s.current_semester) as course,
                COUNT(*) as student_count
            FROM students s {where_clause}
            GROUP BY s.current_semester
            ORDER BY s.current_semester
        ''', params)
    course_stats = cursor.fetchall()
    
    # Get gender stats
    cursor.execute(f'''
        SELECT gender, COUNT(*) as count FROM students s {where_clause} GROUP BY gender
    ''', params)
    gender_stats = cursor.fetchall()
    
    # Get top students by semester results (if any exist)
    cursor.execute('''
        SELECT s.name, s.roll_number, 
               COALESCE(AVG(sr.grade_point), 0) as avg_gp
        FROM students s
        LEFT JOIN semester_results sr ON s.roll_number = sr.student_roll
        GROUP BY s.roll_number, s.name
        ORDER BY avg_gp DESC
        LIMIT 5
    ''')
    top_students = cursor.fetchall()
    
    # Set display name
    if selected_dept != 'all':
        dept_name = dept_dict.get(selected_dept, 'Selected Department')
        display_name = f"{dept_name} ({f'Sem {selected_sem}' if selected_sem != 'all' else 'All Semesters'})"
    else:
        display_name = f"All Departments ({f'Sem {selected_sem}' if selected_sem != 'all' else 'All Semesters'})"
    
    cursor.close()
    conn.close()
    
    return render_template('analytics.html', 
                           summary=summary, 
                           course_stats=course_stats, 
                           gender_stats=gender_stats,
                           top_students=top_students,
                           departments=dept_dict,
                           dept_list=departments,
                           selected_dept=selected_dept,
                           selected_sem=selected_sem,
                           display_name=display_name)


@app.route('/<roll_no>/delete', methods=('POST',))
@login_required
@teacher_required
def delete(roll_no):
    student = get_student(roll_no)
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE roll_number = %s', (roll_no,))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f'Student "{student["name"]}" was successfully deleted!')
    return redirect(url_for('index'))

# --- Authentication Routes ---

@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'user_id' in session:
        if session['role'] == 'STUDENT':
            return redirect(url_for('student_profile'))
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_selection = request.form.get('role', 'teacher')
        
        conn = database.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        user = None
        
        if role_selection in ['admin', 'teacher']:
            # Check users table with role join for admin/teacher login
            cursor.execute('''
                SELECT u.*, r.name as role_name, s.name as full_name, s.department_id
                FROM users u
                JOIN roles r ON u.role_id = r.id
                LEFT JOIN staffs s ON u.id = s.user_id
                WHERE u.username = %s
            ''', (username,))
            db_user = cursor.fetchone()
            
            if db_user and db_user['password_hash'] == password:
                role_name = db_user['role_name']
                # Validate role matches selection
                if role_selection == 'admin' and role_name != 'ADMIN':
                    db_user = None
                elif role_selection == 'teacher' and role_name != 'STAFF':
                    db_user = None
                elif not db_user['is_approved']:
                    flash("Your account is pending approval.", "warning")
                    db_user = None
                else:
                    user = {
                        'id': db_user['id'],
                        'username': db_user['username'],
                        'full_name': db_user['full_name'] or db_user['username'],
                        'role': role_name if role_name != 'STAFF' else 'TEACHER'
                    }
        else:
            # Student login: Check users table with student join
            cursor.execute('''
                SELECT u.*, r.name as role_name, s.roll_number, s.name as full_name, s.department_id
                FROM users u
                JOIN roles r ON u.role_id = r.id
                JOIN students s ON u.id = s.user_id
                WHERE u.username = %s
            ''', (username,))
            db_user = cursor.fetchone()
            
            if db_user and db_user['password_hash'] == password:
                user = {
                    'id': db_user['roll_number'],
                    'username': db_user['roll_number'],
                    'full_name': db_user['full_name'],
                    'role': 'STUDENT',
                    'department_id': db_user['department_id']
                }
        
        cursor.close()
        conn.close()
        
        if user:
            session.clear()
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            
            if user['role'] == 'STUDENT':
                session['department_id'] = user.get('department_id')
            
            flash(f"Welcome, {user['full_name']}!", "success")
            
            if user['role'] == 'STUDENT':
                return redirect(url_for('student_profile'))
            return redirect(url_for('index'))
        
        flash("Invalid credentials or role selection.", "danger")
    
    return render_template('auth/login.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form.get('email', '')
        
        conn = database.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Get STAFF role id
            cursor.execute('SELECT id FROM roles WHERE name = %s', ('STAFF',))
            role = cursor.fetchone()
            staff_role_id = role['id'] if role else 2
            
            # Create user in users table (not approved by default)
            cursor.execute('''
                INSERT INTO users (username, password_hash, role_id, is_active, is_approved)
                VALUES (%s, %s, %s, %s, %s)
            ''', (username, password, staff_role_id, True, False))
            user_id = cursor.lastrowid
            
            # Create staff profile
            cursor.execute('''
                INSERT INTO staffs (user_id, name, email, designation)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, full_name, email, 'Teacher'))
            conn.commit()
            
            # Send notification to admin about new signup
            send_admin_new_signup_notification(full_name, username, email)
            
            flash("Signup successful! Please wait for admin approval. You will be notified by email.", "success")
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            conn.rollback()
            if err.errno == 1062:  # Duplicate entry
                flash("Username already exists.", "danger")
            else:
                flash(f"Error: {err.msg}", "danger")
            cursor.close()
            conn.close()
            
    return render_template('auth/signup.html')

@app.route('/admin-signup', methods=('GET', 'POST'))
def admin_signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form.get('email', '')
        
        conn = database.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Get ADMIN role id
            cursor.execute('SELECT id FROM roles WHERE name = %s', ('ADMIN',))
            role = cursor.fetchone()
            admin_role_id = role['id'] if role else 1
            
            # Create user in users table (not approved by default)
            cursor.execute('''
                INSERT INTO users (username, password_hash, role_id, is_active, is_approved)
                VALUES (%s, %s, %s, %s, %s)
            ''', (username, password, admin_role_id, True, False))
            user_id = cursor.lastrowid
            
            # Create staff profile
            cursor.execute('''
                INSERT INTO staffs (user_id, name, email, designation)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, full_name, email, 'Administrator'))
            conn.commit()
            
            # Send notification to existing admins about new admin signup
            send_admin_new_signup_notification(full_name, username, email)
            
            flash("Admin registration submitted! Please wait for approval.", "success")
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            conn.rollback()
            if err.errno == 1062:
                flash("Username already exists.", "danger")
            else:
                flash(f"Error: {err.msg}", "danger")
            cursor.close()
            conn.close()
            
    return render_template('auth/admin_signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# --- Admin Routes ---

@app.route('/admin/user-management')
@login_required
@admin_required
def user_management():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Join users and staffs tables
    cursor.execute('''
        SELECT u.id, u.username, u.is_approved, u.is_active, r.name as role,
               s.name as full_name, s.email
        FROM users u
        JOIN roles r ON u.role_id = r.id
        LEFT JOIN staffs s ON u.id = s.user_id
        WHERE r.name IN ('STAFF', 'ADMIN')
        ORDER BY u.id
    ''')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/users.html', users=users)

@app.route('/admin/approve_user/<int:id>')
@login_required
@admin_required
def approve_user(id):
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user details before approving
    cursor.execute('''
        SELECT s.email, s.name as full_name 
        FROM users u
        LEFT JOIN staffs s ON u.id = s.user_id
        WHERE u.id = %s
    ''', (id,))
    user = cursor.fetchone()
    
    # Approve the user in users table
    cursor.execute('UPDATE users SET is_approved = TRUE WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Send approval email
    if user and user['email']:
        email_sent = send_approval_email(user['email'], user['full_name'])
        if email_sent:
            flash("User approved successfully! Notification email sent.", "success")
        else:
            flash("User approved successfully! (Email notification failed)", "warning")
    else:
        flash("User approved successfully! (No email address on file)", "info")
    
    return redirect(url_for('user_management'))

@app.route('/admin/delete_user/<int:id>', methods=('POST',))
@login_required
@admin_required
def delete_user(id):
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user details before deleting
    cursor.execute('''
        SELECT s.email, s.name as full_name 
        FROM users u
        LEFT JOIN staffs s ON u.id = s.user_id
        WHERE u.id = %s
    ''', (id,))
    user = cursor.fetchone()
    
    # Delete from staffs first (FK), then users
    cursor.execute('DELETE FROM staffs WHERE user_id = %s', (id,))
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Send deletion notification email
    if user and user['email']:
        email_sent = send_deletion_email(user['email'], user['full_name'])
        if email_sent:
            flash("User deleted. Notification email sent.", "info")
        else:
            flash("User deleted. (Email notification failed)", "warning")
    else:
        flash("User deleted.", "info")
    
    return redirect(url_for('user_management'))

@app.route('/admin/master-view')
@login_required
@admin_required
def master_view():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get departments
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE ORDER BY name')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}
    
    # Get department-wise statistics
    cursor.execute('''
        SELECT 
            d.name as department,
            d.code,
            COUNT(s.roll_number) as total_students,
            ROUND(AVG(prev_sem.avg_marks), 2) as prev_sem_avg
        FROM departments d
        LEFT JOIN students s ON s.department_id = d.id
        LEFT JOIN (
            SELECT sr.student_roll, AVG(sr.total_marks) as avg_marks
            FROM semester_results sr
            JOIN students st ON sr.student_roll = st.roll_number
            WHERE sr.semester = st.current_semester - 1
            GROUP BY sr.student_roll
        ) prev_sem ON s.roll_number = prev_sem.student_roll
        WHERE d.is_active = TRUE
        GROUP BY d.id, d.name, d.code
        ORDER BY d.name
    ''')
    dept_stats = cursor.fetchall()
    
    # Get overall statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total
        FROM students
    ''')
    overall = cursor.fetchone()
    overall['avg_cgpa'] = 0.0
    overall['toppers'] = 0
    overall['passed'] = overall['total']
    overall['failed'] = 0
    
    # Get top 10 students by CGPA (from semester_results)
    cursor.execute('''
        SELECT s.roll_number, s.name, d.name as dept_name,
               COALESCE(AVG(sr.grade_point), 0) as cgpa
        FROM students s
        JOIN departments d ON s.department_id = d.id
        LEFT JOIN semester_results sr ON s.roll_number = sr.student_roll
        GROUP BY s.roll_number, s.name, d.name
        ORDER BY cgpa DESC
        LIMIT 10
    ''')
    top_students = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/master_view.html', 
                           dept_stats=dept_stats, 
                           overall=overall,
                           top_students=top_students,
                           departments=dept_dict)

@app.route('/teacher/search')
@login_required
@teacher_required
def teacher_search():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT s.*, d.name as dept_name, d.degree_type, d.code as dept_code
        FROM students s
        JOIN departments d ON s.department_id = d.id
        ORDER BY s.roll_number
    ''')
    students = cursor.fetchall()
    
    # Get departments for filter
    cursor.execute('SELECT id, code, name, degree_type FROM departments WHERE is_active = TRUE')
    departments = cursor.fetchall()
    dept_dict = {str(d['id']): f"{d['degree_type']} - {d['name']}" for d in departments}
    
    # Calculate CGPA for each student
    for student in students:
        student['cgpa'] = database.get_student_cgpa(student['roll_number'])
    
    cursor.close()
    conn.close()
    
    return render_template('teacher_search.html', students=students, departments=dept_dict)

@app.route('/student/profile')
@login_required
@student_required
def student_profile():
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    student_roll = session.get('user_id')
    
    cursor.execute('''
        SELECT s.*, d.name as dept_name, d.degree_type, d.code as dept_code
        FROM students s
        JOIN departments d ON s.department_id = d.id
        WHERE s.roll_number = %s
    ''', (student_roll,))
    student = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not student:
        flash("Profile not found.", "danger")
        return redirect(url_for('logout'))
    
    # Calculate CGPA
    student['cgpa'] = database.get_student_cgpa(student_roll)
    dept_name = f"{student['degree_type']} - {student['dept_name']}"
    
    # Calculate year string
    year_map = {1: 'I Year', 2: 'I Year', 3: 'II Year', 4: 'II Year', 
                5: 'III Year', 6: 'III Year', 7: 'IV Year', 8: 'IV Year'}
    year_str = year_map.get(student['current_semester'], 'I Year')
        
    return render_template('student_profile.html', student=student, dept_name=dept_name, year_str=year_str)


# --- Marks Entry Routes ---

@app.route('/student/<roll_no>/marks', methods=['GET', 'POST'])
@login_required
@teacher_required
def marks_entry(roll_no):
    """Marks entry page for a student following Anna University format"""
    conn = database.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get student info
    cursor.execute('''
        SELECT s.*, d.name as dept_name, d.degree_type, d.code as dept_code
        FROM students s
        JOIN departments d ON s.department_id = d.id
        WHERE s.roll_number = %s
    ''', (roll_no,))
    student = cursor.fetchone()
    
    if not student:
        cursor.close()
        conn.close()
        abort(404)
    
    # Get semester from query param, default to student's current semester
    selected_sem = request.args.get('sem', str(student['current_semester']))
    try:
        selected_sem = int(selected_sem)
    except ValueError:
        selected_sem = student['current_semester']

    # Get subjects for selected semester and department
    cursor.execute('''
        SELECT id, code, name, credits, subject_type
        FROM subjects
        WHERE department_id = %s AND semester = %s AND is_active = TRUE
        ORDER BY subject_type, code
    ''', (student['department_id'], selected_sem))
    subjects = cursor.fetchall()
    
    # Get current academic year
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    if current_month >= 6:  # June onwards = new academic year
        academic_year = f"{current_year}-{current_year + 1}"
    else:
        academic_year = f"{current_year - 1}-{current_year}"
    
    # Get assessment type IDs
    cursor.execute('SELECT id, short_name FROM assessments')
    assessments = {a['short_name']: a['id'] for a in cursor.fetchall()}
    
    if request.method == 'POST':
        try:
            # Process marks for each subject
            for subject in subjects:
                subj_id = subject['id']
                
                # Get marks from form
                cat1 = request.form.get(f'cat1_{subj_id}', 0)
                cat2 = request.form.get(f'cat2_{subj_id}', 0)
                cat3 = request.form.get(f'cat3_{subj_id}', 0)
                assignment = request.form.get(f'assignment_{subj_id}', 0)
                attendance = request.form.get(f'attendance_{subj_id}', 0)
                university = request.form.get(f'university_{subj_id}', 0)
                
                # Convert to float
                cat1 = float(cat1) if cat1 else 0
                cat2 = float(cat2) if cat2 else 0
                cat3 = float(cat3) if cat3 else 0
                assignment = float(assignment) if assignment else 0
                attendance = float(attendance) if attendance else 0
                university = float(university) if university else 0
                
                # Save individual marks to student_marks table
                marks_data = [
                    (assessments.get('CAT1'), cat1),
                    (assessments.get('CAT2'), cat2),
                    (assessments.get('CAT3'), cat3),
                    (assessments.get('ASGN'), assignment),
                    (assessments.get('ATT'), attendance),
                    (assessments.get('UNI'), university),
                ]
                
                for assess_id, marks in marks_data:
                    if assess_id and marks > 0:
                        cursor.execute('''
                            INSERT INTO student_marks 
                            (student_roll, subject_id, assessment_id, academic_year, marks_obtained, entered_by)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE marks_obtained = %s, entered_by = %s
                        ''', (roll_no, subj_id, assess_id, academic_year, marks, session['user_id'], marks, session['user_id']))
                
                # Calculate totals for semester_results
                # Internal calculation (40 marks)
                cat_avg = (cat1 + cat2) / 2  # Average of CAT1 and CAT2
                cat_scaled = (cat_avg / 50) * 15  # Scale to 15
                cat3_scaled = (cat3 / 100) * 10  # Scale to 10
                assign_scaled = (assignment / 20) * 5  # Scale to 5
                attend_scaled = (attendance / 100) * 5  # Scale to 5
                internal_total = min(40, cat_scaled + cat3_scaled + assign_scaled + attend_scaled)
                
                # External (60 marks)
                external_scaled = (university / 100) * 60
                
                # Total and grade
                total = round(internal_total + external_scaled)
                grade, grade_point = database.get_grade(total)
                result_status = 'Pass' if total >= 50 else 'Fail'
                
                # Save to semester_results
                cursor.execute('''
                    INSERT INTO semester_results 
                    (student_roll, subject_id, academic_year, semester, internal_marks, external_marks, 
                     total_marks, grade, grade_point, credits, result)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    internal_marks = %s, external_marks = %s, total_marks = %s, 
                    grade = %s, grade_point = %s, result = %s
                ''', (roll_no, subj_id, academic_year, selected_sem, 
                      internal_total, external_scaled, total, grade, grade_point, 
                      subject['credits'], result_status,
                      internal_total, external_scaled, total, grade, grade_point, result_status))
            
            conn.commit()
            flash(f'Marks for Semester {selected_sem} saved successfully!', 'success')
            
        except Exception as e:
            conn.rollback()
            flash(f'Error saving marks: {str(e)}', 'danger')
    
    # Get existing marks for display
    marks = {}
    for subject in subjects:
        cursor.execute('''
            SELECT a.short_name, sm.marks_obtained
            FROM student_marks sm
            JOIN assessments a ON sm.assessment_id = a.id
            WHERE sm.student_roll = %s AND sm.subject_id = %s AND sm.academic_year = %s
        ''', (roll_no, subject['id'], academic_year))
        
        subject_marks = cursor.fetchall()
        marks[subject['id']] = {}
        for m in subject_marks:
            if m['short_name'] == 'CAT1':
                marks[subject['id']]['cat1'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
            elif m['short_name'] == 'CAT2':
                marks[subject['id']]['cat2'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
            elif m['short_name'] == 'CAT3':
                marks[subject['id']]['cat3'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
            elif m['short_name'] == 'ASGN':
                marks[subject['id']]['assignment'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
            elif m['short_name'] == 'ATT':
                marks[subject['id']]['attendance'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
            elif m['short_name'] == 'UNI':
                marks[subject['id']]['university'] = float(m['marks_obtained']) if m['marks_obtained'] else ''
    
    cursor.close()
    conn.close()
    
    dept_name = f"{student['degree_type']} - {student['dept_name']}"
    
    return render_template('add_marks.html', 
                          student=student, 
                          subjects=subjects, 
                          marks=marks,
                          dept_name=dept_name,
                          academic_year=academic_year,
                          selected_sem=selected_sem)


if __name__ == '__main__':
    # Initialize DB if not exists
    database.init_db()
    app.run(debug=True, port=5000)
