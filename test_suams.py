import unittest
from core import register_courses, grade_for, calculate_result, enroll_semester, submit_exam_form
from demo_data import REGISTRATIONS, ENROLLMENTS, SEMESTERS, EXAM_FORMS

class SUAMSTests(unittest.TestCase):
    def setUp(self):
        self.old_reg=REGISTRATIONS.get("TEST",None)
        REGISTRATIONS.pop("TEST",None)
        ENROLLMENTS[:] = [e for e in ENROLLMENTS if e["student_id"]!="TEST"]
        EXAM_FORMS[:] = [f for f in EXAM_FORMS if f["student_id"]!="TEST"]
    def tearDown(self):
        REGISTRATIONS.pop("TEST",None)
        if self.old_reg is not None: REGISTRATIONS["TEST"]=self.old_reg
        ENROLLMENTS[:] = [e for e in ENROLLMENTS if e["student_id"]!="TEST"]
        EXAM_FORMS[:] = [f for f in EXAM_FORMS if f["student_id"]!="TEST"]
    def test_course_registration(self):
        self.assertEqual(register_courses("TEST",["CSE101","CSE102"]),6)
    def test_gpa_calculation(self):
        self.assertEqual(grade_for(85),("A+",4.0))
    def test_credit_limit(self):
        with self.assertRaises(ValueError):
            register_courses("TEST",["CSE101","CSE102","CSE201","CSE202","EEE101","MAT101","CE101"])
    def test_registration_and_semester_integration(self):
        register_courses("TEST",["CSE101"])
        enroll_semester("TEST",SEMESTERS[0])
        self.assertTrue(any(e["student_id"]=="TEST" for e in ENROLLMENTS))
    def test_exam_form_eligibility_integration(self):
        register_courses("TEST",["CSE101"])
        enroll_semester("TEST",SEMESTERS[0])
        form=submit_exam_form("TEST",SEMESTERS[0])
        self.assertEqual(form["status"],"Pending")
    def test_black_box_19_credit_rejected(self):
        with self.assertRaises(ValueError):
            register_courses("TEST",["CSE101","CSE102","CSE201","CSE202","EEE101","MAT101","CE101"])
    def test_black_box_valid_exam_form(self):
        register_courses("TEST",["CSE101"])
        enroll_semester("TEST",SEMESTERS[0])
        self.assertEqual(submit_exam_form("TEST",SEMESTERS[0])["status"],"Pending")
    def test_white_box_result_decisions(self):
        result=calculate_result({"assignment":9,"class_test":8,"attendance":9,"midterm":25,"final":38})
        self.assertEqual(result["status"],"Passed")
        self.assertEqual(result["grade"],"A+")
        with self.assertRaises(ValueError):
            calculate_result({"assignment":20,"class_test":8,"attendance":9,"midterm":25,"final":38})

if __name__=="__main__":
    unittest.main(verbosity=2)
