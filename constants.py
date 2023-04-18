class Role:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

ROLES = {
    "student": Role(10, 'Student'),
    "teacher": Role(20, 'Teacher'),
    "it_staff": Role(10, 'IT Staff'),
    "admin": Role(30, 'Admin')
}

class DB:
    users = "users_db"

# To map column names to column numbers
class UserModel:
    id = 0
    username = 1
    password = 2
    email = 3
    role = 4
    priority = 5

