class Role:
    def __init__(self, priority, db):
        self.priority = priority
        self.db = db

ROLES = {
    "student": Role(10, "students_signup_db"),
    "teacher": Role(20, "teachers_signup_db"),
    "it_staff": Role(10, "it_staff_signup_db")
}