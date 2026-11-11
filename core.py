"""Application services and business rules. All data is stored in memory."""
from demo_data import *

GRADE_SCALE = [
    (80, "A+", 4.00), (75, "A", 3.75), (70, "A-", 3.50),
    (65, "B+", 3.25), (60, "B", 3.00), (55, "B-", 2.75),
    (50, "C+", 2.50), (45, "C", 2.25), (40, "D", 2.00), (0, "F", 0.00)
]

def authenticate(username, password):
    user = USERS.get(username.strip().lower())
    if user and user["password"] == password:
        return {"username": username.strip().lower(), **user}
    return None

def grade_for(total):
    total = float(total)
    if not 0 <= total <= 100:
        raise ValueError("Total marks must be between 0 and 100.")
    for minimum, grade, point in GRADE_SCALE:
        if total >= minimum:
            return grade, point
    return "F", 0.0

def calculate_result(marks):
    """Three decision points: range validation, pass/fail, and grade selection."""
    required = ["assignment", "class_test", "attendance", "midterm", "final"]
    if any(k not in marks for k in required):
        raise ValueError("All assessment components are required.")
    values = [float(marks[k]) for k in required]
    if any(v < 0 for v in values):
        raise ValueError("Marks cannot be negative.")
    if values[0] > 10 or values[1] > 10 or values[2] > 10 or values[3] > 30 or values[4] > 40:
        raise ValueError("Maximum marks: assignment 10, class test 10, attendance 10, midterm 30, final 40.")
    total = sum(values)
    grade, point = grade_for(total)
    if total < 40:
        status = "Failed"
    else:
        status = "Passed"
    return {"total": round(total, 2), "grade": grade, "gpa": point, "status": status}

def register_courses(student_id, course_codes):
    if not course_codes:
        raise ValueError("Select at least one course.")
    if len(course_codes) != len(set(course_codes)):
        raise ValueError("Duplicate course selection is not allowed.")
    known = {c["code"]: c for c in COURSES}
    if any(code not in known for code in course_codes):
        raise ValueError("Unknown course selected.")
    credits = sum(known[c]["credit"] for c in course_codes)
    if credits > 18:
        raise ValueError("Credit limit exceeded. Maximum allowed is 18.")
    REGISTRATIONS[student_id] = list(course_codes)
    return credits

def enroll_semester(student_id, semester):
    if semester not in SEMESTERS:
        raise ValueError("Please select a valid semester.")
    if any(e["student_id"] == student_id and e["semester"] == semester for e in ENROLLMENTS):
        raise ValueError("You are already enrolled in this semester.")
    ENROLLMENTS.append({"student_id":student_id,"semester":semester,"status":"Enrolled"})
    return True

def submit_exam_form(student_id, semester):
    if not REGISTRATIONS.get(student_id):
        raise ValueError("Register at least one course before submitting the exam form.")
    if not any(e["student_id"] == student_id and e["semester"] == semester for e in ENROLLMENTS):
        raise ValueError("Semester enrollment is required before exam form submission.")
    if any(f["student_id"] == student_id and f["semester"] == semester for f in EXAM_FORMS):
        raise ValueError("An examination form already exists for this semester.")
    form = {"form_id":f"EF-{len(EXAM_FORMS)+1:03d}","student_id":student_id,"semester":semester,"status":"Pending"}
    EXAM_FORMS.append(form)
    return form

def generate_routine():
    """Simple sequential scheduler; each course gets a unique date/slot/room."""
    from datetime import date, timedelta
    result = []
    slots = ["09:00 AM - 12:00 PM", "02:00 PM - 05:00 PM"]
    for i, course in enumerate(COURSES):
        day = date.today() + timedelta(days=7 + i // 2)
        result.append({"date":day.strftime("%d %b %Y"),"time":slots[i % 2],
                       "course":course["code"]+" - "+course["name"],"room":f"Room {301 + i}"})
    ROUTINE[:] = result
    return result

def publish_notification(title, message, audience="All"):
    if not title.strip() or not message.strip():
        raise ValueError("Title and message are required.")
    item = {"title":title.strip(),"message":message.strip(),"audience":audience,"date":__import__("datetime").date.today().isoformat()}
    NOTIFICATION_SERVICE.publish(item)
    return item

class NotificationService:
    """Observer pattern: registered dashboard observers receive published notices."""
    def __init__(self):
        self.observers = []
    def subscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    def publish(self, notice):
        NOTIFICATIONS.insert(0, notice)
        for observer in list(self.observers):
            observer(notice)

NOTIFICATION_SERVICE = NotificationService()
