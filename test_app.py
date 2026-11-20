import unittest
from app import Course, GradeCalculator, ResultManager, Student


class TestResultManager(unittest.TestCase):
    def setUp(self):
        self.manager = ResultManager()
        self.manager.add_course(Course("ENG101", "English Composition", 2.0))

    def test_duplicate_student_id_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_student(Student("241118037", "Another Student"))

    def test_invalid_marks_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.record_mark("241118037", "CSE101", -1)
        with self.assertRaises(ValueError):
            self.manager.record_mark("241118037", "CSE101", 101)

    def test_grade_and_point_boundaries(self):
        self.assertEqual(GradeCalculator.get_grade_and_point(80), ("A+", 4.00))
        self.assertEqual(GradeCalculator.get_grade_and_point(75), ("A", 3.75))
        self.assertEqual(GradeCalculator.get_grade_and_point(70), ("A-", 3.50))
        self.assertEqual(GradeCalculator.get_grade_and_point(40), ("D", 2.00))
        self.assertEqual(GradeCalculator.get_grade_and_point(39), ("F", 0.00))

    def test_weighted_cgpa_calculation(self):
        self.manager.record_mark("241118037", "CSE101", 85)  # 4.00 * 3 = 12.00
        self.manager.record_mark("241118037", "MAT101", 72)  # 3.50 * 3 = 10.50
        self.manager.record_mark("241118037", "ENG101", 62)  # 3.00 * 2 =  6.00
        # Total = 28.50 / 8.0 credits = 3.5625 -> 3.56

        results = self.manager.get_student_results("241118037")
        cgpa = GradeCalculator.calculate_cgpa(results)
        self.assertEqual(cgpa, 3.56)

    def test_result_sheet_generation(self):
        self.manager.record_mark("241118037", "CSE101", 90)
        sheet = self.manager.generate_result_sheet("241118037")
        self.assertIn("Razu Ahmed", sheet)
        self.assertIn("241118037", sheet)
        self.assertIn("A+", sheet)


if __name__ == "__main__":
    unittest.main()