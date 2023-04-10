class Role:
    def __init__(self, priority):
        self.priority = priority

ROLES = {
    "student": Role(10),
    "teacher": Role(20),
    "it_staff": Role(10),
    "admin": Role(30)
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

