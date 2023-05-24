class Role:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name


ROLES = {
    "student": Role(10, 'Student'),
    "teacher": Role(30, 'Teacher'),
    "it_staff": Role(40, 'IT Staff'),
    "admin": Role(50, 'Admin')
}


class DB:
    users = "users_db"
    classrooms = "classrooms_db"
    courses = "courses_db"
    exams = "exams_db"
    reservations = "reservations_db"
    itReports = "IT_Report_logdb"
    kuclass_db = "kuclass.db"

# To map column names to column numbers


class UserModel:
    id = 0
    username = 1
    password = 2
    email = 3
    role = 4
    priority = 5


class ClassroomModel:
    code = 0
    department = 1
    room_type = 2
    seats = 3
    area = 4
    board_num = 5
    board_type = 6
    board_size = 7
    connections = 8
    projector_size = 9
    panopto_capture = 10
    touch_screen = 11
    document_camera = 12
    outlets_for_students = 13
    projector_num = 14


FilterOperations = {
    "code": "=",
    "department": "=",
    "seats": ">",
    "area": ">",
    "board_num": "=",
    "connections": "like",
    "panopto_capture": "like",
    "outlets_for_students": "like",
    "projector_num": "=",
    "room_type": "like"
}

VacancyCheckRequirements = ["date", "start_time", "duration"]

class ReservationConstants:
    RESERVATION_UPPER_LIMIT = 180
    reservation_in_past_error = "This reservation is for the past!"
    reservation_too_long_error = f"The duration of a reservation cannot exceed {(RESERVATION_UPPER_LIMIT/60):.0f} hours"
    reservation_conflicting_error = "There is another reservation that conflicts with your reservation interval."