from typing import Dict, List, Tuple

# --- CONSTANTS ---
MIN_MARK = 0.0
MAX_MARK = 100.0
MIN_CREDIT = 0.5
MAX_CREDIT = 5.0

GRADE_SCALE = [
    (80.0, "A+", 4.00),
    (75.0, "A",  3.75),
    (70.0, "A-", 3.50),
    (65.0, "B+", 3.25),
    (60.0, "B",  3.00),
    (55.0, "B-", 2.75),
    (50.0, "C+", 2.50),
    (45.0, "C",  2.25),
    (40.0, "D",  2.00),
    (0.0,  "F",  0.00),
]


# --- MODELS ---
class Student:
    def __init__(self, student_id: str, name: str):
        if not student_id or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")
        if not name or not name.strip():
            raise ValueError("Student Name cannot be empty.")
        self.student_id = student_id.strip()
        self.name = name.strip()


class Course:
    def __init__(self, course_code: str, title: str, credit: float):
        if not course_code or not course_code.strip():
            raise ValueError("Course Code cannot be empty.")
        if not title or not title.strip():
            raise ValueError("Course Title cannot be empty.")
        if not (MIN_CREDIT <= credit <= MAX_CREDIT):
            raise ValueError(f"Credit must be between {MIN_CREDIT} and {MAX_CREDIT}.")
        
        self.course_code = course_code.strip().upper()
        self.title = title.strip()
        self.credit = float(credit)


class CourseResult:
    def __init__(self, student_id: str, course_code: str, mark: float):
        if not (MIN_MARK <= mark <= MAX_MARK):
            raise ValueError(f"Mark must be between {MIN_MARK} and {MAX_MARK}.")
        
        self.student_id = student_id
        self.course_code = course_code
        self.mark = float(mark)


# --- GRADE CALCULATOR ---
class GradeCalculator:
    @staticmethod
    def get_grade_and_point(mark: float) -> Tuple[str, float]:
        for min_score, letter_grade, grade_point in GRADE_SCALE:
            if mark >= min_score:
                return letter_grade, grade_point
        return "F", 0.00

    @classmethod
    def calculate_cgpa(cls, results: List[CourseResult], courses_dict: Dict[str, Course]) -> float:
        if not results:
            return 0.00
        
        total_weighted_points = 0.0
        total_credits = 0.0

        for res in results:
            course = courses_dict.get(res.course_code)
            if course:
                _, grade_point = cls.get_grade_and_point(res.mark)
                total_weighted_points += grade_point * course.credit
                total_credits += course.credit

        return round(total_weighted_points / total_credits, 2) if total_credits > 0 else 0.00


# --- RESULT MANAGER ---
class ResultManager:
    def __init__(self):
        self._students: Dict[str, Student] = {}
        self._courses: Dict[str, Course] = {}
        self._records: Dict[str, List[CourseResult]] = {}
        self._load_default_data()

    def _load_default_data(self):
        # প্রি-লোডেড স্যাম্পল ডাটা
        self.add_student(Student("241118037", "Razu Ahmed"))
        self.add_course(Course("CSE101", "Structured Programming", 3.0))
        self.add_course(Course("MAT101", "Engineering Mathematics", 3.0))

    def add_student(self, student: Student) -> None:
        if student.student_id in self._students:
            raise ValueError(f"Student ID '{student.student_id}' already exists!")
        self._students[student.student_id] = student
        self._records[student.student_id] = []

    def add_course(self, course: Course) -> None:
        if course.course_code in self._courses:
            raise ValueError(f"Course Code '{course.course_code}' already exists!")
        self._courses[course.course_code] = course

    def record_mark(self, student_id: str, course_code: str, mark: float) -> None:
        sid = student_id.strip()
        ccode = course_code.strip().upper()

        if sid not in self._students:
            raise KeyError(f"Student ID '{sid}' not found.")
        if ccode not in self._courses:
            raise KeyError(f"Course Code '{ccode}' not found.")

        new_result = CourseResult(sid, ccode, mark)
        student_results = self._records[sid]
        
        for idx, res in enumerate(student_results):
            if res.course_code == ccode:
                student_results[idx] = new_result
                return

        student_results.append(new_result)

    def generate_result_sheet(self, student_id: str) -> str:
        sid = student_id.strip()
        if sid not in self._students:
            raise KeyError(f"Student ID '{sid}' not found.")

        student = self._students[sid]
        results = self._records.get(sid, [])
        cgpa = GradeCalculator.calculate_cgpa(results, self._courses)

        lines = [
            "=" * 68,
            f"                  OFFICIAL ACADEMIC RESULT SHEET",
            "=" * 68,
            f"Student Name : {student.name}",
            f"Student ID   : {student.student_id}",
            "-" * 68,
            f"{'Course Code':<15} {'Course Title':<25} {'Credit':<8} {'Mark':<8} {'Grade':<6} {'Point':<6}",
            "-" * 68,
        ]

        if not results:
            lines.append("No marks recorded for this student yet.")
        else:
            for res in results:
                course = self._courses[res.course_code]
                grade, point = GradeCalculator.get_grade_and_point(res.mark)
                lines.append(
                    f"{course.course_code:<15} {course.title:<25} "
                    f"{course.credit:<8.1f} {res.mark:<8.2f} {grade:<6} {point:<6.2f}"
                )

        lines.extend([
            "-" * 68,
            f"Cumulative Grade Point Average (CGPA): {cgpa:.2f}",
            "=" * 68,
        ])
        return "\n".join(lines)


# --- CLI INTERFACE ---
def run_cli():
    manager = ResultManager()

    while True:
        print("\n=== UNIVERSITY RESULT MANAGEMENT SYSTEM ===")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enter/Update Student Mark")
        print("4. View Student Result Sheet")
        print("5. Exit")

        try:
            choice = input("Enter your choice (1-5): ").strip()
        except EOFError:
            print("\n[Error] Online compiler input stream ended. Please use Interactive Console.")
            break

        if choice == "5":
            print("Exiting system. Goodbye!")
            break

        try:
            if choice == "1":
                sid = input("Enter Student ID: ")
                name = input("Enter Student Name: ")
                manager.add_student(Student(sid, name))
                print("[Success] Student added successfully.")

            elif choice == "2":
                code = input("Enter Course Code: ")
                title = input("Enter Course Title: ")
                credit = float(input("Enter Course Credit (0.5 - 5.0): "))
                manager.add_course(Course(code, title, credit))
                print("[Success] Course added successfully.")

            elif choice == "3":
                sid = input("Enter Student ID: ")
                code = input("Enter Course Code: ")
                mark = float(input("Enter Mark (0 to 100): "))
                manager.record_mark(sid, code, mark)
                print("[Success] Mark recorded successfully.")

            elif choice == "4":
                sid = input("Enter Student ID: ")
                print("\n" + manager.generate_result_sheet(sid))

            else:
                print("[Error] Invalid choice! Please enter 1-5.")

        except (ValueError, KeyError) as e:
            print(f"[Validation Error]: {e}")


if __name__ == "__main__":
    run_cli()