"""
Seed All Semester Subjects for All Departments
This script adds subjects for all 8 semesters across all 12 departments
"""

import mysql.connector
from mysql.connector import Error

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'gowsik',
    'database': 'student_management_v2'
}

# Common subjects for all departments (Semesters 1-2)
COMMON_SUBJECTS_SEM1 = [
    ('HS8151', 'Communicative English', 4, 'Theory'),
    ('MA8151', 'Engineering Mathematics I', 4, 'Theory'),
    ('PH8151', 'Engineering Physics', 3, 'Theory'),
    ('CY8151', 'Engineering Chemistry', 3, 'Theory'),
    ('GE8151', 'Problem Solving and Python Programming', 3, 'Theory'),
    ('GE8152', 'Engineering Graphics', 4, 'Theory'),
    ('GE8161', 'Problem Solving and Python Programming Lab', 2, 'Lab'),
    ('BS8161', 'Physics and Chemistry Lab', 2, 'Lab'),
]

COMMON_SUBJECTS_SEM2 = [
    ('HS8251', 'Technical English', 4, 'Theory'),
    ('MA8251', 'Engineering Mathematics II', 4, 'Theory'),
    ('PH8252', 'Physics for Information Science', 3, 'Theory'),
    ('BE8255', 'Basic Electrical Electronics and Measurement Engineering', 3, 'Theory'),
    ('GE8291', 'Environmental Science and Engineering', 3, 'Theory'),
    ('CS8251', 'Programming in C', 3, 'Theory'),
    ('CS8261', 'C Programming Lab', 2, 'Lab'),
    ('GE8261', 'Engineering Practices Lab', 2, 'Lab'),
]

# Department-specific subjects for semesters 3-8
DEPT_SUBJECTS = {
    'ADS': {
        3: [
            ('AD8301', 'Data Structures', 3, 'Theory'),
            ('AD8302', 'Database Management Systems', 3, 'Theory'),
            ('AD8303', 'Discrete Mathematics', 4, 'Theory'),
            ('AD8304', 'Digital Principles and Computer Organization', 3, 'Theory'),
            ('AD8305', 'Probability and Statistics', 3, 'Theory'),
            ('AD8311', 'Data Structures Lab', 2, 'Lab'),
            ('AD8312', 'DBMS Lab', 2, 'Lab'),
        ],
        4: [
            ('AD8401', 'Design and Analysis of Algorithms', 3, 'Theory'),
            ('AD8402', 'Operating Systems', 3, 'Theory'),
            ('AD8403', 'Computer Networks', 3, 'Theory'),
            ('AD8404', 'Artificial Intelligence', 3, 'Theory'),
            ('AD8405', 'Linear Algebra for Machine Learning', 3, 'Theory'),
            ('AD8411', 'OS Lab', 2, 'Lab'),
            ('AD8412', 'Python for Data Science Lab', 2, 'Lab'),
        ],
        5: [
            ('AD8501', 'Machine Learning', 3, 'Theory'),
            ('AD8502', 'Data Visualization', 3, 'Theory'),
            ('AD8503', 'Big Data Analytics', 3, 'Theory'),
            ('AD8504', 'Natural Language Processing', 3, 'Theory'),
            ('AD8505', 'Software Engineering', 3, 'Theory'),
            ('AD8511', 'Machine Learning Lab', 2, 'Lab'),
            ('AD8512', 'Data Visualization Lab', 2, 'Lab'),
        ],
        6: [
            ('AD8601', 'Deep Learning', 3, 'Theory'),
            ('AD8602', 'Computer Vision', 3, 'Theory'),
            ('AD8603', 'Data Mining', 3, 'Theory'),
            ('AD8604', 'Cloud Computing', 3, 'Theory'),
            ('AD8605', 'Open Elective I', 3, 'Theory'),
            ('AD8611', 'Deep Learning Lab', 2, 'Lab'),
            ('AD8612', 'Mini Project', 2, 'Project'),
        ],
        7: [
            ('AD8701', 'Reinforcement Learning', 3, 'Theory'),
            ('AD8702', 'Internet of Things', 3, 'Theory'),
            ('AD8703', 'Professional Elective I', 3, 'Theory'),
            ('AD8704', 'Professional Elective II', 3, 'Theory'),
            ('AD8705', 'Open Elective II', 3, 'Theory'),
            ('AD8711', 'IoT Lab', 2, 'Lab'),
            ('AD8712', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('AD8801', 'Professional Elective III', 3, 'Theory'),
            ('AD8802', 'Professional Elective IV', 3, 'Theory'),
            ('AD8811', 'Project Work', 10, 'Project'),
        ],
    },
    'CSE': {
        3: [
            ('CS8301', 'Data Structures', 3, 'Theory'),
            ('CS8302', 'Digital Principles and System Design', 3, 'Theory'),
            ('CS8351', 'Discrete Mathematics', 4, 'Theory'),
            ('CS8352', 'Foundations of Data Science', 3, 'Theory'),
            ('CS8391', 'Data Structures Lab', 2, 'Lab'),
            ('CS8381', 'Digital Logic Design Lab', 2, 'Lab'),
            ('CS8382', 'Object Oriented Programming Lab', 2, 'Lab'),
        ],
        4: [
            ('CS8401', 'Design and Analysis of Algorithms', 3, 'Theory'),
            ('CS8402', 'Operating Systems', 3, 'Theory'),
            ('CS8451', 'Database Management Systems', 3, 'Theory'),
            ('CS8491', 'Computer Architecture', 3, 'Theory'),
            ('CS8492', 'Computer Networks', 3, 'Theory'),
            ('CS8481', 'DBMS Lab', 2, 'Lab'),
            ('CS8482', 'OS Lab', 2, 'Lab'),
        ],
        5: [
            ('CS8501', 'Theory of Computation', 3, 'Theory'),
            ('CS8502', 'Compiler Design', 3, 'Theory'),
            ('CS8591', 'Computer Networks', 3, 'Theory'),
            ('CS8592', 'Object Oriented Analysis and Design', 3, 'Theory'),
            ('CS8594', 'Software Engineering', 3, 'Theory'),
            ('CS8581', 'Networks Lab', 2, 'Lab'),
            ('CS8582', 'SS and Compiler Design Lab', 2, 'Lab'),
        ],
        6: [
            ('CS8601', 'Mobile Computing', 3, 'Theory'),
            ('CS8602', 'Compiler Design', 3, 'Theory'),
            ('CS8603', 'Distributed Systems', 3, 'Theory'),
            ('CS8651', 'Internet Programming', 3, 'Theory'),
            ('CS8691', 'Open Elective II', 3, 'Theory'),
            ('CS8681', 'Internet Programming Lab', 2, 'Lab'),
            ('CS8682', 'Mobile Application Development Lab', 2, 'Lab'),
        ],
        7: [
            ('CS8701', 'Artificial Intelligence', 3, 'Theory'),
            ('CS8702', 'Cryptography and Network Security', 3, 'Theory'),
            ('CS8791', 'Professional Elective I', 3, 'Theory'),
            ('CS8792', 'Professional Elective II', 3, 'Theory'),
            ('CS8711', 'Security Lab', 2, 'Lab'),
            ('CS8712', 'Project Work Phase I', 2, 'Project'),
        ],
        8: [
            ('CS8801', 'Professional Elective III', 3, 'Theory'),
            ('CS8802', 'Professional Elective IV', 3, 'Theory'),
            ('CS8811', 'Project Work Phase II', 10, 'Project'),
        ],
    },
    'IT': {
        3: [
            ('IT8301', 'Data Structures', 3, 'Theory'),
            ('IT8302', 'Digital Principles and Computer Organization', 3, 'Theory'),
            ('IT8351', 'Discrete Mathematics', 4, 'Theory'),
            ('IT8352', 'Software Engineering', 3, 'Theory'),
            ('IT8391', 'Data Structures Lab', 2, 'Lab'),
            ('IT8381', 'Digital Electronics Lab', 2, 'Lab'),
        ],
        4: [
            ('IT8401', 'Design and Analysis of Algorithms', 3, 'Theory'),
            ('IT8402', 'Operating Systems', 3, 'Theory'),
            ('IT8451', 'Database Management Systems', 3, 'Theory'),
            ('IT8491', 'Computer Architecture', 3, 'Theory'),
            ('IT8492', 'Computer Networks', 3, 'Theory'),
            ('IT8481', 'DBMS Lab', 2, 'Lab'),
            ('IT8482', 'OS Lab', 2, 'Lab'),
        ],
        5: [
            ('IT8501', 'Theory of Computation', 3, 'Theory'),
            ('IT8502', 'System Software', 3, 'Theory'),
            ('IT8591', 'Information Security', 3, 'Theory'),
            ('IT8592', 'Web Technology', 3, 'Theory'),
            ('IT8594', 'Cloud Computing', 3, 'Theory'),
            ('IT8581', 'Web Technology Lab', 2, 'Lab'),
            ('IT8582', 'SS Lab', 2, 'Lab'),
        ],
        6: [
            ('IT8601', 'Mobile Computing', 3, 'Theory'),
            ('IT8602', 'Software Testing', 3, 'Theory'),
            ('IT8603', 'Internet of Things', 3, 'Theory'),
            ('IT8651', 'Service Oriented Architecture', 3, 'Theory'),
            ('IT8691', 'Open Elective II', 3, 'Theory'),
            ('IT8681', 'SOA Lab', 2, 'Lab'),
            ('IT8682', 'Mobile App Lab', 2, 'Lab'),
        ],
        7: [
            ('IT8701', 'Big Data Analytics', 3, 'Theory'),
            ('IT8702', 'Machine Learning', 3, 'Theory'),
            ('IT8791', 'Professional Elective I', 3, 'Theory'),
            ('IT8792', 'Professional Elective II', 3, 'Theory'),
            ('IT8711', 'Big Data Lab', 2, 'Lab'),
            ('IT8712', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('IT8801', 'Professional Elective III', 3, 'Theory'),
            ('IT8802', 'Professional Elective IV', 3, 'Theory'),
            ('IT8811', 'Project Work', 10, 'Project'),
        ],
    },
    'AML': {
        3: [
            ('AL8301', 'Data Structures', 3, 'Theory'),
            ('AL8302', 'Database Management Systems', 3, 'Theory'),
            ('AL8303', 'Discrete Mathematics', 4, 'Theory'),
            ('AL8304', 'Digital Logic Design', 3, 'Theory'),
            ('AL8305', 'Probability and Statistics', 3, 'Theory'),
            ('AL8311', 'Data Structures Lab', 2, 'Lab'),
            ('AL8312', 'DBMS Lab', 2, 'Lab'),
        ],
        4: [
            ('AL8401', 'Design and Analysis of Algorithms', 3, 'Theory'),
            ('AL8402', 'Operating Systems', 3, 'Theory'),
            ('AL8403', 'Computer Networks', 3, 'Theory'),
            ('AL8404', 'Introduction to AI', 3, 'Theory'),
            ('AL8405', 'Linear Algebra', 3, 'Theory'),
            ('AL8411', 'OS Lab', 2, 'Lab'),
            ('AL8412', 'AI Basics Lab', 2, 'Lab'),
        ],
        5: [
            ('AL8501', 'Machine Learning Fundamentals', 3, 'Theory'),
            ('AL8502', 'Neural Networks', 3, 'Theory'),
            ('AL8503', 'Data Analytics', 3, 'Theory'),
            ('AL8504', 'Natural Language Processing', 3, 'Theory'),
            ('AL8505', 'Software Engineering', 3, 'Theory'),
            ('AL8511', 'ML Lab', 2, 'Lab'),
            ('AL8512', 'NLP Lab', 2, 'Lab'),
        ],
        6: [
            ('AL8601', 'Deep Learning', 3, 'Theory'),
            ('AL8602', 'Computer Vision', 3, 'Theory'),
            ('AL8603', 'Cognitive Computing', 3, 'Theory'),
            ('AL8604', 'Cloud Computing', 3, 'Theory'),
            ('AL8605', 'Open Elective I', 3, 'Theory'),
            ('AL8611', 'Deep Learning Lab', 2, 'Lab'),
            ('AL8612', 'Mini Project', 2, 'Project'),
        ],
        7: [
            ('AL8701', 'Reinforcement Learning', 3, 'Theory'),
            ('AL8702', 'Robotics and Automation', 3, 'Theory'),
            ('AL8703', 'Professional Elective I', 3, 'Theory'),
            ('AL8704', 'Professional Elective II', 3, 'Theory'),
            ('AL8705', 'Open Elective II', 3, 'Theory'),
            ('AL8711', 'Robotics Lab', 2, 'Lab'),
            ('AL8712', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('AL8801', 'Professional Elective III', 3, 'Theory'),
            ('AL8802', 'Professional Elective IV', 3, 'Theory'),
            ('AL8811', 'Project Work', 10, 'Project'),
        ],
    },
    'ECE': {
        3: [
            ('EC8301', 'Electron Devices', 3, 'Theory'),
            ('EC8302', 'Digital Electronics', 3, 'Theory'),
            ('EC8351', 'Signals and Systems', 4, 'Theory'),
            ('EC8352', 'Network Analysis', 3, 'Theory'),
            ('EC8391', 'Control Systems Engineering', 3, 'Theory'),
            ('EC8311', 'Electronics Lab I', 2, 'Lab'),
            ('EC8312', 'Digital Electronics Lab', 2, 'Lab'),
        ],
        4: [
            ('EC8401', 'Electronic Circuits II', 3, 'Theory'),
            ('EC8402', 'Digital Signal Processing', 3, 'Theory'),
            ('EC8451', 'Electromagnetic Fields', 3, 'Theory'),
            ('EC8491', 'Communication Theory', 3, 'Theory'),
            ('EC8492', 'VLSI Design', 3, 'Theory'),
            ('EC8481', 'DSP Lab', 2, 'Lab'),
            ('EC8482', 'Communication Lab', 2, 'Lab'),
        ],
        5: [
            ('EC8501', 'RF and Microwave Engineering', 3, 'Theory'),
            ('EC8502', 'Antenna and Wave Propagation', 3, 'Theory'),
            ('EC8551', 'Wireless Communication', 3, 'Theory'),
            ('EC8552', 'Computer Architecture and Organization', 3, 'Theory'),
            ('EC8553', 'Discrete Time Signal Processing', 3, 'Theory'),
            ('EC8511', 'Microwave Lab', 2, 'Lab'),
            ('EC8512', 'HDL Lab', 2, 'Lab'),
        ],
        6: [
            ('EC8601', 'VLSI Design', 3, 'Theory'),
            ('EC8602', 'Embedded Systems', 3, 'Theory'),
            ('EC8651', 'Optical Communication', 3, 'Theory'),
            ('EC8691', 'Open Elective I', 3, 'Theory'),
            ('EC8693', 'Professional Elective I', 3, 'Theory'),
            ('EC8681', 'VLSI Lab', 2, 'Lab'),
            ('EC8682', 'Embedded Lab', 2, 'Lab'),
        ],
        7: [
            ('EC8701', 'Satellite Communication', 3, 'Theory'),
            ('EC8702', 'Biomedical Instrumentation', 3, 'Theory'),
            ('EC8791', 'Professional Elective II', 3, 'Theory'),
            ('EC8792', 'Professional Elective III', 3, 'Theory'),
            ('EC8793', 'Open Elective II', 3, 'Theory'),
            ('EC8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('EC8801', 'Professional Elective IV', 3, 'Theory'),
            ('EC8802', 'Professional Elective V', 3, 'Theory'),
            ('EC8811', 'Project Work', 10, 'Project'),
        ],
    },
    'EEE': {
        3: [
            ('EE8301', 'Electric Circuit Analysis', 3, 'Theory'),
            ('EE8302', 'Electromagnetic Theory', 3, 'Theory'),
            ('EE8351', 'Digital Logic Circuits', 4, 'Theory'),
            ('EE8352', 'Electronic Devices and Circuits', 3, 'Theory'),
            ('EE8391', 'Control Systems Engineering', 3, 'Theory'),
            ('EE8311', 'Electric Circuits Lab', 2, 'Lab'),
            ('EE8312', 'Electronics Lab', 2, 'Lab'),
        ],
        4: [
            ('EE8401', 'Electrical Machines I', 3, 'Theory'),
            ('EE8402', 'Linear Integrated Circuits', 3, 'Theory'),
            ('EE8451', 'Transmission and Distribution', 3, 'Theory'),
            ('EE8491', 'Measurements and Instrumentation', 3, 'Theory'),
            ('EE8492', 'Power Electronics', 3, 'Theory'),
            ('EE8481', 'Electrical Machines Lab I', 2, 'Lab'),
            ('EE8482', 'LIC Lab', 2, 'Lab'),
        ],
        5: [
            ('EE8501', 'Electrical Machines II', 3, 'Theory'),
            ('EE8502', 'Power System Analysis', 3, 'Theory'),
            ('EE8551', 'Microprocessors and Microcontrollers', 3, 'Theory'),
            ('EE8552', 'Power Plant Engineering', 3, 'Theory'),
            ('EE8553', 'Renewable Energy Sources', 3, 'Theory'),
            ('EE8511', 'Machines Lab II', 2, 'Lab'),
            ('EE8512', 'Microprocessor Lab', 2, 'Lab'),
        ],
        6: [
            ('EE8601', 'Control System Design', 3, 'Theory'),
            ('EE8602', 'Power Electronics and Drives', 3, 'Theory'),
            ('EE8651', 'Analysis of Special Machines', 3, 'Theory'),
            ('EE8691', 'Open Elective I', 3, 'Theory'),
            ('EE8693', 'Professional Elective I', 3, 'Theory'),
            ('EE8681', 'Control and Instrumentation Lab', 2, 'Lab'),
            ('EE8682', 'Power Electronics Lab', 2, 'Lab'),
        ],
        7: [
            ('EE8701', 'High Voltage Engineering', 3, 'Theory'),
            ('EE8702', 'Power System Operation and Control', 3, 'Theory'),
            ('EE8791', 'Professional Elective II', 3, 'Theory'),
            ('EE8792', 'Professional Elective III', 3, 'Theory'),
            ('EE8793', 'Open Elective II', 3, 'Theory'),
            ('EE8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('EE8801', 'Professional Elective IV', 3, 'Theory'),
            ('EE8802', 'Professional Elective V', 3, 'Theory'),
            ('EE8811', 'Project Work', 10, 'Project'),
        ],
    },
    'ME': {
        3: [
            ('ME8301', 'Manufacturing Technology I', 3, 'Theory'),
            ('ME8302', 'Engineering Thermodynamics', 3, 'Theory'),
            ('ME8351', 'Strength of Materials', 4, 'Theory'),
            ('ME8352', 'Fluid Mechanics and Machinery', 3, 'Theory'),
            ('ME8391', 'Kinematics of Machinery', 3, 'Theory'),
            ('ME8311', 'Manufacturing Technology Lab I', 2, 'Lab'),
            ('ME8312', 'Fluid Mechanics Lab', 2, 'Lab'),
        ],
        4: [
            ('ME8401', 'Manufacturing Technology II', 3, 'Theory'),
            ('ME8402', 'Thermal Engineering', 3, 'Theory'),
            ('ME8451', 'Dynamics of Machinery', 3, 'Theory'),
            ('ME8491', 'Engineering Metallurgy', 3, 'Theory'),
            ('ME8492', 'Machine Drawing', 3, 'Theory'),
            ('ME8481', 'Manufacturing Technology Lab II', 2, 'Lab'),
            ('ME8482', 'Thermal Engineering Lab', 2, 'Lab'),
        ],
        5: [
            ('ME8501', 'Design of Machine Elements', 3, 'Theory'),
            ('ME8502', 'Metrology and Measurements', 3, 'Theory'),
            ('ME8551', 'Industrial Engineering', 3, 'Theory'),
            ('ME8552', 'Finite Element Analysis', 3, 'Theory'),
            ('ME8553', 'Heat and Mass Transfer', 3, 'Theory'),
            ('ME8511', 'Metrology Lab', 2, 'Lab'),
            ('ME8512', 'CAD/CAM Lab', 2, 'Lab'),
        ],
        6: [
            ('ME8601', 'Design of Transmission Systems', 3, 'Theory'),
            ('ME8602', 'Power Plant Engineering', 3, 'Theory'),
            ('ME8651', 'Automobile Engineering', 3, 'Theory'),
            ('ME8691', 'Open Elective I', 3, 'Theory'),
            ('ME8693', 'Professional Elective I', 3, 'Theory'),
            ('ME8681', 'Dynamics Lab', 2, 'Lab'),
            ('ME8682', 'Heat Transfer Lab', 2, 'Lab'),
        ],
        7: [
            ('ME8701', 'Mechatronics', 3, 'Theory'),
            ('ME8702', 'Refrigeration and Air Conditioning', 3, 'Theory'),
            ('ME8791', 'Professional Elective II', 3, 'Theory'),
            ('ME8792', 'Professional Elective III', 3, 'Theory'),
            ('ME8793', 'Open Elective II', 3, 'Theory'),
            ('ME8711', 'Mechatronics Lab', 2, 'Lab'),
            ('ME8712', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('ME8801', 'Professional Elective IV', 3, 'Theory'),
            ('ME8802', 'Professional Elective V', 3, 'Theory'),
            ('ME8811', 'Project Work', 10, 'Project'),
        ],
    },
    'CE': {
        3: [
            ('CE8301', 'Mechanics of Solids', 3, 'Theory'),
            ('CE8302', 'Fluid Mechanics', 3, 'Theory'),
            ('CE8351', 'Surveying', 4, 'Theory'),
            ('CE8352', 'Engineering Geology', 3, 'Theory'),
            ('CE8391', 'Structural Analysis I', 3, 'Theory'),
            ('CE8311', 'Fluid Mechanics Lab', 2, 'Lab'),
            ('CE8312', 'Surveying Lab', 2, 'Lab'),
        ],
        4: [
            ('CE8401', 'Structural Analysis II', 3, 'Theory'),
            ('CE8402', 'Soil Mechanics', 3, 'Theory'),
            ('CE8451', 'Construction Technology', 3, 'Theory'),
            ('CE8491', 'Concrete Technology', 3, 'Theory'),
            ('CE8492', 'Building Drawing', 3, 'Theory'),
            ('CE8481', 'Soil Mechanics Lab', 2, 'Lab'),
            ('CE8482', 'Concrete Lab', 2, 'Lab'),
        ],
        5: [
            ('CE8501', 'Design of RC Structures', 3, 'Theory'),
            ('CE8502', 'Highway Engineering', 3, 'Theory'),
            ('CE8551', 'Foundation Engineering', 3, 'Theory'),
            ('CE8552', 'Environmental Engineering I', 3, 'Theory'),
            ('CE8553', 'Hydrology and Water Resources', 3, 'Theory'),
            ('CE8511', 'Highway Lab', 2, 'Lab'),
            ('CE8512', 'Environmental Lab', 2, 'Lab'),
        ],
        6: [
            ('CE8601', 'Steel Structures', 3, 'Theory'),
            ('CE8602', 'Environmental Engineering II', 3, 'Theory'),
            ('CE8651', 'Irrigation Engineering', 3, 'Theory'),
            ('CE8691', 'Open Elective I', 3, 'Theory'),
            ('CE8693', 'Professional Elective I', 3, 'Theory'),
            ('CE8681', 'Structural Engineering Lab', 2, 'Lab'),
            ('CE8682', 'Environmental Engineering Lab II', 2, 'Lab'),
        ],
        7: [
            ('CE8701', 'Quantity Surveying', 3, 'Theory'),
            ('CE8702', 'Traffic Engineering', 3, 'Theory'),
            ('CE8791', 'Professional Elective II', 3, 'Theory'),
            ('CE8792', 'Professional Elective III', 3, 'Theory'),
            ('CE8793', 'Open Elective II', 3, 'Theory'),
            ('CE8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('CE8801', 'Professional Elective IV', 3, 'Theory'),
            ('CE8802', 'Professional Elective V', 3, 'Theory'),
            ('CE8811', 'Project Work', 10, 'Project'),
        ],
    },
    'AG': {
        3: [
            ('AG8301', 'Soil Science', 3, 'Theory'),
            ('AG8302', 'Fluid Mechanics', 3, 'Theory'),
            ('AG8351', 'Surveying and Leveling', 4, 'Theory'),
            ('AG8352', 'Farm Machinery', 3, 'Theory'),
            ('AG8391', 'Agricultural Engineering', 3, 'Theory'),
            ('AG8311', 'Fluid Mechanics Lab', 2, 'Lab'),
            ('AG8312', 'Surveying Lab', 2, 'Lab'),
        ],
        4: [
            ('AG8401', 'Irrigation Engineering', 3, 'Theory'),
            ('AG8402', 'Farm Power', 3, 'Theory'),
            ('AG8451', 'Agro-Processing Engineering', 3, 'Theory'),
            ('AG8491', 'Soil and Water Conservation', 3, 'Theory'),
            ('AG8492', 'Crop Production', 3, 'Theory'),
            ('AG8481', 'Farm Machinery Lab', 2, 'Lab'),
            ('AG8482', 'Irrigation Lab', 2, 'Lab'),
        ],
        5: [
            ('AG8501', 'Agricultural Structures', 3, 'Theory'),
            ('AG8502', 'Agricultural Drainage', 3, 'Theory'),
            ('AG8551', 'Food Technology', 3, 'Theory'),
            ('AG8552', 'Tractors and Power Units', 3, 'Theory'),
            ('AG8553', 'Renewable Energy in Agriculture', 3, 'Theory'),
            ('AG8511', 'Food Processing Lab', 2, 'Lab'),
            ('AG8512', 'CAD Lab', 2, 'Lab'),
        ],
        6: [
            ('AG8601', 'Agricultural Waste Management', 3, 'Theory'),
            ('AG8602', 'Precision Farming', 3, 'Theory'),
            ('AG8651', 'Greenhouse Technology', 3, 'Theory'),
            ('AG8691', 'Open Elective I', 3, 'Theory'),
            ('AG8693', 'Professional Elective I', 3, 'Theory'),
            ('AG8681', 'Agricultural Lab I', 2, 'Lab'),
            ('AG8682', 'Process Engineering Lab', 2, 'Lab'),
        ],
        7: [
            ('AG8701', 'Remote Sensing and GIS', 3, 'Theory'),
            ('AG8702', 'Watershed Management', 3, 'Theory'),
            ('AG8791', 'Professional Elective II', 3, 'Theory'),
            ('AG8792', 'Professional Elective III', 3, 'Theory'),
            ('AG8793', 'Open Elective II', 3, 'Theory'),
            ('AG8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('AG8801', 'Professional Elective IV', 3, 'Theory'),
            ('AG8802', 'Professional Elective V', 3, 'Theory'),
            ('AG8811', 'Project Work', 10, 'Project'),
        ],
    },
    'BME': {
        3: [
            ('BM8301', 'Human Anatomy and Physiology', 3, 'Theory'),
            ('BM8302', 'Biomedical Sensors', 3, 'Theory'),
            ('BM8351', 'Signals and Systems', 4, 'Theory'),
            ('BM8352', 'Electric Circuits', 3, 'Theory'),
            ('BM8391', 'Control Systems', 3, 'Theory'),
            ('BM8311', 'Sensors Lab', 2, 'Lab'),
            ('BM8312', 'Circuits Lab', 2, 'Lab'),
        ],
        4: [
            ('BM8401', 'Biomedical Instrumentation', 3, 'Theory'),
            ('BM8402', 'Biomechanics', 3, 'Theory'),
            ('BM8451', 'Digital Signal Processing', 3, 'Theory'),
            ('BM8491', 'Biomedical Electronics', 3, 'Theory'),
            ('BM8492', 'Medical Physics', 3, 'Theory'),
            ('BM8481', 'Instrumentation Lab', 2, 'Lab'),
            ('BM8482', 'DSP Lab', 2, 'Lab'),
        ],
        5: [
            ('BM8501', 'Medical Imaging', 3, 'Theory'),
            ('BM8502', 'Biomaterials', 3, 'Theory'),
            ('BM8551', 'Hospital Management', 3, 'Theory'),
            ('BM8552', 'Rehabilitation Engineering', 3, 'Theory'),
            ('BM8553', 'Clinical Engineering', 3, 'Theory'),
            ('BM8511', 'Imaging Lab', 2, 'Lab'),
            ('BM8512', 'Biomaterials Lab', 2, 'Lab'),
        ],
        6: [
            ('BM8601', 'Artificial Organs', 3, 'Theory'),
            ('BM8602', 'Biomedical Signal Processing', 3, 'Theory'),
            ('BM8651', 'Medical Informatics', 3, 'Theory'),
            ('BM8691', 'Open Elective I', 3, 'Theory'),
            ('BM8693', 'Professional Elective I', 3, 'Theory'),
            ('BM8681', 'Signal Processing Lab', 2, 'Lab'),
            ('BM8682', 'Clinical Lab', 2, 'Lab'),
        ],
        7: [
            ('BM8701', 'Neural Engineering', 3, 'Theory'),
            ('BM8702', 'Medical Device Regulations', 3, 'Theory'),
            ('BM8791', 'Professional Elective II', 3, 'Theory'),
            ('BM8792', 'Professional Elective III', 3, 'Theory'),
            ('BM8793', 'Open Elective II', 3, 'Theory'),
            ('BM8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('BM8801', 'Professional Elective IV', 3, 'Theory'),
            ('BM8802', 'Professional Elective V', 3, 'Theory'),
            ('BM8811', 'Project Work', 10, 'Project'),
        ],
    },
    'BT': {
        3: [
            ('BT8301', 'Biochemistry', 3, 'Theory'),
            ('BT8302', 'Microbiology', 3, 'Theory'),
            ('BT8351', 'Cell Biology', 4, 'Theory'),
            ('BT8352', 'Molecular Biology', 3, 'Theory'),
            ('BT8391', 'Bioprocess Principles', 3, 'Theory'),
            ('BT8311', 'Biochemistry Lab', 2, 'Lab'),
            ('BT8312', 'Microbiology Lab', 2, 'Lab'),
        ],
        4: [
            ('BT8401', 'Genetic Engineering', 3, 'Theory'),
            ('BT8402', 'Bioprocess Engineering', 3, 'Theory'),
            ('BT8451', 'Immunology', 3, 'Theory'),
            ('BT8491', 'Enzyme Technology', 3, 'Theory'),
            ('BT8492', 'Bioinformatics', 3, 'Theory'),
            ('BT8481', 'Genetic Engineering Lab', 2, 'Lab'),
            ('BT8482', 'Bioprocess Lab', 2, 'Lab'),
        ],
        5: [
            ('BT8501', 'Downstream Processing', 3, 'Theory'),
            ('BT8502', 'Plant Biotechnology', 3, 'Theory'),
            ('BT8551', 'Animal Biotechnology', 3, 'Theory'),
            ('BT8552', 'Industrial Biotechnology', 3, 'Theory'),
            ('BT8553', 'Environmental Biotechnology', 3, 'Theory'),
            ('BT8511', 'Downstream Lab', 2, 'Lab'),
            ('BT8512', 'Plant Tissue Culture Lab', 2, 'Lab'),
        ],
        6: [
            ('BT8601', 'Food Biotechnology', 3, 'Theory'),
            ('BT8602', 'Pharmaceutical Biotechnology', 3, 'Theory'),
            ('BT8651', 'Bioethics', 3, 'Theory'),
            ('BT8691', 'Open Elective I', 3, 'Theory'),
            ('BT8693', 'Professional Elective I', 3, 'Theory'),
            ('BT8681', 'Food Biotech Lab', 2, 'Lab'),
            ('BT8682', 'Pharma Lab', 2, 'Lab'),
        ],
        7: [
            ('BT8701', 'Nanobiotechnology', 3, 'Theory'),
            ('BT8702', 'Genomics and Proteomics', 3, 'Theory'),
            ('BT8791', 'Professional Elective II', 3, 'Theory'),
            ('BT8792', 'Professional Elective III', 3, 'Theory'),
            ('BT8793', 'Open Elective II', 3, 'Theory'),
            ('BT8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('BT8801', 'Professional Elective IV', 3, 'Theory'),
            ('BT8802', 'Professional Elective V', 3, 'Theory'),
            ('BT8811', 'Project Work', 10, 'Project'),
        ],
    },
    'FT': {
        3: [
            ('FT8301', 'Food Chemistry', 3, 'Theory'),
            ('FT8302', 'Food Microbiology', 3, 'Theory'),
            ('FT8351', 'Food Processing Technology', 4, 'Theory'),
            ('FT8352', 'Fluid Mechanics', 3, 'Theory'),
            ('FT8391', 'Heat and Mass Transfer', 3, 'Theory'),
            ('FT8311', 'Food Chemistry Lab', 2, 'Lab'),
            ('FT8312', 'Microbiology Lab', 2, 'Lab'),
        ],
        4: [
            ('FT8401', 'Food Preservation', 3, 'Theory'),
            ('FT8402', 'Food Engineering', 3, 'Theory'),
            ('FT8451', 'Cereal Technology', 3, 'Theory'),
            ('FT8491', 'Dairy Technology', 3, 'Theory'),
            ('FT8492', 'Fruit and Vegetable Technology', 3, 'Theory'),
            ('FT8481', 'Food Processing Lab', 2, 'Lab'),
            ('FT8482', 'Dairy Lab', 2, 'Lab'),
        ],
        5: [
            ('FT8501', 'Food Packaging', 3, 'Theory'),
            ('FT8502', 'Meat and Poultry Technology', 3, 'Theory'),
            ('FT8551', 'Food Quality Control', 3, 'Theory'),
            ('FT8552', 'Bakery and Confectionery', 3, 'Theory'),
            ('FT8553', 'Beverage Technology', 3, 'Theory'),
            ('FT8511', 'Quality Control Lab', 2, 'Lab'),
            ('FT8512', 'Bakery Lab', 2, 'Lab'),
        ],
        6: [
            ('FT8601', 'Food Biotechnology', 3, 'Theory'),
            ('FT8602', 'Food Safety and Regulations', 3, 'Theory'),
            ('FT8651', 'Sensory Evaluation', 3, 'Theory'),
            ('FT8691', 'Open Elective I', 3, 'Theory'),
            ('FT8693', 'Professional Elective I', 3, 'Theory'),
            ('FT8681', 'Sensory Lab', 2, 'Lab'),
            ('FT8682', 'Food Safety Lab', 2, 'Lab'),
        ],
        7: [
            ('FT8701', 'Functional Foods', 3, 'Theory'),
            ('FT8702', 'Food Plant Management', 3, 'Theory'),
            ('FT8791', 'Professional Elective II', 3, 'Theory'),
            ('FT8792', 'Professional Elective III', 3, 'Theory'),
            ('FT8793', 'Open Elective II', 3, 'Theory'),
            ('FT8711', 'Project Phase I', 2, 'Project'),
        ],
        8: [
            ('FT8801', 'Professional Elective IV', 3, 'Theory'),
            ('FT8802', 'Professional Elective V', 3, 'Theory'),
            ('FT8811', 'Project Work', 10, 'Project'),
        ],
    },
}


def seed_subjects():
    """Seed all subjects for all departments and semesters"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Get all departments
        cursor.execute('SELECT id, code FROM departments')
        departments = {d['code']: d['id'] for d in cursor.fetchall()}
        
        subjects_added = 0
        
        # Add common subjects for semester 1 and 2 for all departments
        for dept_code, dept_id in departments.items():
            # Semester 1
            for code, name, credits, subject_type in COMMON_SUBJECTS_SEM1:
                unique_code = f"{dept_code}_{code}"  # Make unique per department
                try:
                    cursor.execute('''
                        INSERT IGNORE INTO subjects (code, name, department_id, semester, credits, subject_type)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (unique_code, name, dept_id, 1, credits, subject_type))
                    if cursor.rowcount > 0:
                        subjects_added += 1
                except Error as e:
                    pass
            
            # Semester 2
            for code, name, credits, subject_type in COMMON_SUBJECTS_SEM2:
                unique_code = f"{dept_code}_{code}"
                try:
                    cursor.execute('''
                        INSERT IGNORE INTO subjects (code, name, department_id, semester, credits, subject_type)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (unique_code, name, dept_id, 2, credits, subject_type))
                    if cursor.rowcount > 0:
                        subjects_added += 1
                except Error as e:
                    pass
        
        # Add department-specific subjects for semesters 3-8
        for dept_code, semesters in DEPT_SUBJECTS.items():
            if dept_code not in departments:
                print(f"⚠️ Department {dept_code} not found, skipping...")
                continue
            
            dept_id = departments[dept_code]
            
            for semester, subjects in semesters.items():
                for code, name, credits, subject_type in subjects:
                    try:
                        cursor.execute('''
                            INSERT IGNORE INTO subjects (code, name, department_id, semester, credits, subject_type)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (code, name, dept_id, semester, credits, subject_type))
                        if cursor.rowcount > 0:
                            subjects_added += 1
                    except Error as e:
                        pass
        
        conn.commit()
        print(f"\n✅ Successfully added {subjects_added} subjects!")
        
        # Show summary
        cursor.execute('''
            SELECT d.code, d.name, COUNT(s.id) as subject_count 
            FROM departments d 
            LEFT JOIN subjects s ON d.id = s.department_id 
            GROUP BY d.id 
            ORDER BY d.code
        ''')
        summary = cursor.fetchall()
        
        print("\n📊 Subjects per Department:")
        print("-" * 50)
        for row in summary:
            print(f"   {row['code']}: {row['name']} - {row['subject_count']} subjects")
        
        # Show semester-wise breakdown for first department
        cursor.execute('''
            SELECT semester, COUNT(*) as count 
            FROM subjects 
            WHERE department_id = (SELECT id FROM departments WHERE code = 'ADS')
            GROUP BY semester 
            ORDER BY semester
        ''')
        sem_summary = cursor.fetchall()
        
        print("\n📚 Semester-wise breakdown (ADS Department):")
        print("-" * 50)
        for row in sem_summary:
            print(f"   Semester {row['semester']}: {row['count']} subjects")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    print("🚀 Seeding subjects for all departments (Semesters 1-8)...")
    print("=" * 60)
    seed_subjects()
    print("\n✅ Done! All subjects have been added to the database.")
