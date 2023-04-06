class Role:
    def __init__(self, priority, db):
        self.priority = priority
        self.db = db

ROLES = {
    "student": Role(10, "students_signup_db"),
    "teacher": Role(20, "teachers_signup_db"),
<<<<<<< HEAD
    "it": Role(10, "it_staff_signup_db")
=======
    "it_staff": Role(10, "it_staff_signup_db")
>>>>>>> b5a8ff882caf06338b17d72bf5a854edc33d6cd8
}