import mysql.connector

from database_v2 import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Count subjects per department
cursor.execute('''
    SELECT d.code, d.name, COUNT(s.id) as cnt 
    FROM departments d 
    LEFT JOIN subjects s ON d.id = s.department_id 
    GROUP BY d.id 
    ORDER BY d.code
''')
print("Subjects per Department:")
print("-" * 50)
for r in cursor.fetchall():
    print(f"  {r[0]}: {r[2]} subjects")

# Check ADS semesters
cursor.execute('''
    SELECT semester, COUNT(*) 
    FROM subjects 
    WHERE department_id = (SELECT id FROM departments WHERE code = 'ADS') 
    GROUP BY semester 
    ORDER BY semester
''')
print("\nADS Semester-wise Subjects:")
print("-" * 50)
for r in cursor.fetchall():
    print(f"  Semester {r[0]}: {r[1]} subjects")

cursor.close()
conn.close()
