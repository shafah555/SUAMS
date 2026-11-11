"""Fictional in-memory demonstration data for SUAMS."""

USERS = {
    "student": {"password": "1234", "role": "Student", "name": "Ayesha Rahman", "student_id": "S-1001"},
    "teacher": {"password": "1234", "role": "Teacher", "name": "Dr. Farhan Ahmed", "teacher_id": "T-201"},
    "admin": {"password": "1234", "role": "Administrator", "name": "System Administrator"},
    "exam": {"password": "1234", "role": "Examination Controller", "name": "Examination Controller"},
}

STUDENTS = [
    {"id":"S-1001","name":"Ayesha Rahman","email":"ayesha@example.com","department":"CSE","previous_result":"GPA 5.00"},
    {"id":"S-1002","name":"Tanvir Hasan","email":"tanvir@example.com","department":"EEE","previous_result":"GPA 4.80"},
    {"id":"S-1003","name":"Nusrat Jahan","email":"nusrat@example.com","department":"CSE","previous_result":"GPA 4.90"},
    {"id":"S-1004","name":"Sabbir Hossain","email":"sabbir@example.com","department":"CE","previous_result":"GPA 4.60"},
    {"id":"S-1005","name":"Mim Akter","email":"mim@example.com","department":"ME","previous_result":"GPA 4.75"},
    {"id":"S-1006","name":"Rafi Islam","email":"rafi@example.com","department":"CSE","previous_result":"GPA 4.70"},
    {"id":"S-1007","name":"Sumaiya Noor","email":"sumaiya@example.com","department":"EEE","previous_result":"GPA 4.95"},
    {"id":"S-1008","name":"Arif Chowdhury","email":"arif@example.com","department":"CSE","previous_result":"GPA 4.55"},
    {"id":"S-1009","name":"Jannat Sultana","email":"jannat@example.com","department":"CE","previous_result":"GPA 4.85"},
    {"id":"S-1010","name":"Mahin Kabir","email":"mahin@example.com","department":"ME","previous_result":"GPA 4.65"},
]

TEACHERS = [
    {"id":"T-201","name":"Dr. Farhan Ahmed","department":"CSE","email":"farhan@example.com"},
    {"id":"T-202","name":"Nabila Karim","department":"CSE","email":"nabila@example.com"},
    {"id":"T-203","name":"Imran Hossain","department":"EEE","email":"imran@example.com"},
    {"id":"T-204","name":"Sadia Islam","department":"CE","email":"sadia@example.com"},
    {"id":"T-205","name":"Rashed Mahmud","department":"ME","email":"rashed@example.com"},
]

COURSES = [
    {"code":"CSE101","name":"Introduction to Computing","credit":3,"teacher":"Dr. Farhan Ahmed"},
    {"code":"CSE102","name":"Structured Programming","credit":3,"teacher":"Nabila Karim"},
    {"code":"CSE201","name":"Data Structures","credit":3,"teacher":"Dr. Farhan Ahmed"},
    {"code":"CSE202","name":"Database Systems","credit":3,"teacher":"Nabila Karim"},
    {"code":"EEE101","name":"Basic Electrical Engineering","credit":3,"teacher":"Imran Hossain"},
    {"code":"CE101","name":"Engineering Mechanics","credit":2,"teacher":"Sadia Islam"},
    {"code":"ME101","name":"Workshop Practice","credit":2,"teacher":"Rashed Mahmud"},
    {"code":"MAT101","name":"Calculus and Linear Algebra","credit":3,"teacher":"Dr. Farhan Ahmed"},
]
SEMESTERS = ["Year 1 - Semester 1", "Year 1 - Semester 2", "Year 2 - Semester 1"]
ADMISSIONS = [
    {"application_id":"A-001","name":"Rumana Sarker","student_id":"S-1011","email":"rumana@example.com","department":"CSE","previous_result":"GPA 4.90","status":"Pending"},
    {"application_id":"A-002","name":"Hasib Rahman","student_id":"S-1012","email":"hasib@example.com","department":"EEE","previous_result":"GPA 4.70","status":"Pending"},
]
EXAM_FORMS = [
    {"form_id":"EF-001","student_id":"S-1001","semester":"Year 1 - Semester 1","status":"Pending"},
    {"form_id":"EF-002","student_id":"S-1002","semester":"Year 1 - Semester 1","status":"Approved"},
]
NOTIFICATIONS = [
    {"title":"Course registration open","message":"Register your semester courses before the deadline.","audience":"All","date":"2026-11-01"},
    {"title":"Midterm examination","message":"Check the examination routine before attending.","audience":"All","date":"2026-11-05"},
]
ADVISING = [{"request_id":"ADV-001","student_id":"S-1001","topic":"Course selection","comment":"","status":"Open"}]
ENROLLMENTS = [{"student_id":"S-1001","semester":"Year 1 - Semester 1","status":"Enrolled"}]
REGISTRATIONS = {"S-1001":["CSE101","CSE102"]}
MARKS = {
    "S-1001": {"CSE101":{"assignment":9,"class_test":8,"attendance":9,"midterm":25,"final":38},
               "CSE102":{"assignment":8,"class_test":9,"attendance":10,"midterm":24,"final":36}},
}
ROUTINE = []
