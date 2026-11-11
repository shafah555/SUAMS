import copy
import unittest

from core import (
    calculate_result,
    enroll_semester,
    grade_for,
    register_courses,
    submit_exam_form,
    validate_mark,
)
from demo_data import (
    ENROLLMENTS,
    EXAM_FORMS,
    MAX_COURSE_CAPACITY,
    MARKS,
    REGISTRATIONS,
    SEMESTERS,
    STUDENTS,
)


class SUAMSTests(unittest.TestCase):
    def setUp(self):
        self.old_registrations = copy.deepcopy(REGISTRATIONS)
        self.old_students = copy.deepcopy(STUDENTS)
        self.old_enrollments = copy.deepcopy(ENROLLMENTS)
        self.old_exam_forms = copy.deepcopy(EXAM_FORMS)
        REGISTRATIONS.pop("TEST", None)
        STUDENTS[:] = [student for student in STUDENTS if student["id"] != "TEST"]
        STUDENTS.append({
            "id": "TEST",
            "is_registered": True,
            "has_unpaid_dues": False,
        })
        ENROLLMENTS[:] = [e for e in ENROLLMENTS if e["student_id"] != "TEST"]
        EXAM_FORMS[:] = [f for f in EXAM_FORMS if f["student_id"] != "TEST"]

    def tearDown(self):
        REGISTRATIONS.clear()
        REGISTRATIONS.update(self.old_registrations)
        STUDENTS[:] = self.old_students
        ENROLLMENTS[:] = self.old_enrollments
        EXAM_FORMS[:] = self.old_exam_forms

    def fill_course_to_capacity(self, code, number_of_other_students):
        for student_id, courses in list(REGISTRATIONS.items()):
            REGISTRATIONS[student_id] = [course for course in courses if course != code]
        for index in range(number_of_other_students):
            REGISTRATIONS[f"CAP-{index}"] = [code]

    def test_course_registration(self):
        self.assertEqual(register_courses("TEST", ["CSE101", "CSE102"]), 6)

    def test_gpa_calculation(self):
        self.assertEqual(grade_for(85), ("A+", 4.0))

    def test_credit_limit(self):
        with self.assertRaises(ValueError):
            register_courses("TEST", ["CSE101", "CSE102", "CSE201", "CSE202", "EEE101", "MAT101", "CE101"])

    def test_registration_and_semester_integration(self):
        register_courses("TEST", ["CSE101"])
        enroll_semester("TEST", SEMESTERS[0])
        self.assertTrue(any(e["student_id"] == "TEST" for e in ENROLLMENTS))

    def test_exam_form_eligibility_integration(self):
        register_courses("TEST", ["CSE101"])
        enroll_semester("TEST", SEMESTERS[0])
        form = submit_exam_form("TEST", SEMESTERS[0])
        self.assertEqual(form["status"], "Pending")

    def test_black_box_19_credit_rejected(self):
        with self.assertRaises(ValueError):
            register_courses("TEST", ["CSE101", "CSE102", "CSE201", "CSE202", "EEE101", "MAT101", "CE101"])

    def test_black_box_valid_exam_form(self):
        register_courses("TEST", ["CSE101"])
        enroll_semester("TEST", SEMESTERS[0])
        self.assertEqual(submit_exam_form("TEST", SEMESTERS[0])["status"], "Pending")

    def test_white_box_result_decisions(self):
        result = calculate_result({"assignment": 9, "class_test": 8, "attendance": 9, "midterm": 25, "final": 38})
        self.assertEqual(result["status"], "Passed")
        self.assertEqual(result["grade"], "A+")
        with self.assertRaises(ValueError):
            calculate_result({"assignment": 20, "class_test": 8, "attendance": 9, "midterm": 25, "final": 38})

    def test_registration_path_student_not_registered(self):
        next(student for student in STUDENTS if student["id"] == "TEST")["is_registered"] = False
        with self.assertRaisesRegex(ValueError, "Student is not registered"):
            register_courses("TEST", ["CSE101"])
        self.assertNotIn("TEST", REGISTRATIONS)

    def test_registration_path_unpaid_dues(self):
        next(student for student in STUDENTS if student["id"] == "TEST")["has_unpaid_dues"] = True
        with self.assertRaisesRegex(ValueError, "Payment dues must be cleared"):
            register_courses("TEST", ["CSE101"])
        self.assertNotIn("TEST", REGISTRATIONS)

    def test_registration_path_course_full_at_capacity(self):
        self.fill_course_to_capacity("CSE101", MAX_COURSE_CAPACITY)
        with self.assertRaisesRegex(ValueError, "Course is full"):
            register_courses("TEST", ["CSE101"])
        self.assertNotIn("TEST", REGISTRATIONS)

    def test_registration_path_duplicate_course(self):
        register_courses("TEST", ["CSE101"])
        with self.assertRaisesRegex(ValueError, "Already registered"):
            register_courses("TEST", ["CSE101"])
        self.assertEqual(REGISTRATIONS["TEST"], ["CSE101"])

    def test_registration_path_success(self):
        credits = register_courses("TEST", ["CSE101"])
        self.assertEqual(credits, 3)
        self.assertEqual(REGISTRATIONS["TEST"], ["CSE101"])

    def test_course_capacity_boundary_accepts_last_seat(self):
        self.fill_course_to_capacity("CSE101", MAX_COURSE_CAPACITY - 1)
        self.assertEqual(register_courses("TEST", ["CSE101"]), 3)
        self.assertEqual(
            sum("CSE101" in courses for courses in REGISTRATIONS.values()),
            MAX_COURSE_CAPACITY,
        )

    def test_mark_validation_accepts_valid_class_and_boundaries(self):
        self.assertEqual(validate_mark(75), 75)
        self.assertEqual(validate_mark(0), 0)
        self.assertEqual(validate_mark(100), 100)

    def test_mark_validation_rejects_values_outside_range(self):
        for mark in (-1, 110):
            with self.subTest(mark=mark), self.assertRaises(ValueError):
                validate_mark(mark)

    def test_invalid_component_mark_is_not_saved(self):
        original_marks = copy.deepcopy(MARKS)
        marks = {"assignment": 110, "class_test": 8, "attendance": 9, "midterm": 25, "final": 38}
        with self.assertRaises(ValueError):
            calculate_result(marks)
        self.assertEqual(MARKS, original_marks)


if __name__ == "__main__":
    unittest.main(verbosity=2)
