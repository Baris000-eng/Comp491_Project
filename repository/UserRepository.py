import sqlite3
import bcrypt
import deprecation
from flask import session

from constants import ROLES
from constants import DB
from constants import UserModel


def initializeUserTables():
    conn = sqlite3.connect(DB.users + '.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.users}
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                priority INTEGER)''')

def intializeITReportLog():
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''CREATE TABLE IF NOT EXISTS IT_Report_logdb
                (it_report_no INTEGER PRIMARY KEY AUTOINCREMENT, 
                 room_name TEXT  NOT NULL, 
                 faculty_name TEXT NOT NULL,
                 problem_description TEXT NOT NULL,
                 date DATE NOT NULL, 
                 time TIME NOT NULL
                 )''')


def createITReport(room_name, faculty_name, problem_description, date, time):
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''INSERT INTO IT_Report_logdb (room_name, faculty_name, problem_description, date, time) 
             VALUES (?, ?, ?, ?, ?)''', (room_name, faculty_name, problem_description, date, time))
    conn.commit()
    conn.close()


def initializeReservationsTable():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS reservations_db 
             (role TEXT NOT NULL,
              date DATE NOT NULL, 
              time TIME NOT NULL, 
              username TEXT DEFAULT "NO_NAME_GIVEN", 
              public_or_private TEXT,
              classroom TEXT,
              priority_reserved INTEGER)''')


def createReservation(date, time, username, priority, public_or_private, classroom):
    """
    Given a date, time, username, priority, insert new reservation into the reservation database
    """
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    c.execute('''INSERT INTO reservations_db (date, time, username, public_or_private, classroom, priority_reserved) 
             VALUES (?, ?, ?, ?, ?, ?)''', (date, time, username, public_or_private, classroom, priority))

    conn.commit()
    conn.close()


@deprecation.deprecated("Use createUser() instead")
def createStudent(username, password, email):
    """
    Given a username, password, and email, insert new student into the student database
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO students_signup_db (username, password, email) VALUES (?, ?, ?)",
        (username, encrypt_password(password=password), email)
    )

    conn.commit()
    conn.close()


@deprecation.deprecated("Use createUser() instead")
def createTeacher(username, password, email):
    """
    Given a username, password, and email, insert new teacher into the teacher database
    """
    print("hi from previous teacher")
    session["username"] = username
    conn = sqlite3.connect('teachers_signup_db.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO teachers_signup_db (username, password, email) VALUES (?, ?, ?)",
        (username, encrypt_password(password=password), email)
    )
    conn.commit()
    conn.close()


@deprecation.deprecated("Use createUser() instead")
def createItStaff(username, password, email):
    """
    Given a username, password, and email, insert new it staff into the it staff database
    """
    conn = sqlite3.connect('it_staff_signup_db.db')
    c = conn.cursor()
    session["username"] = username
    c.execute(
        "INSERT INTO it_staff_signup_db (username, password, email) VALUES (?, ?, ?)",
        (username, encrypt_password(password=password), email)
    )
    conn.commit()
    conn.close()

# Role-based signup


def createUser(username: str, password: str, email: str, role: str):
    """
    Given a username, password, email, and role, insert user into corresponding database
    """

    session["username"] = username
    print("hi")
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()
    c.execute(
        f"INSERT INTO {DB.users} (username, password, email, role, priority) VALUES (?, ?, ?, ?, ?)",
        (username, encrypt_password(password), email, role, ROLES[role].priority)
    )
    conn.commit()
    conn.close()

# Role-based get methods


def getUserByUsername(username: str):
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.users} WHERE username = ?", (username,))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def getUserByEmail(email: str):
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.users} WHERE email = ?", (email,))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def getUserByUsernameAndEmail(username: str, email: str, role: str):
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    c.execute(
        f"SELECT * FROM {DB.users} WHERE username = ? AND email = ?", (username, email))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def userExistsByUsername(username: str):
    """
    Return true if a user exists in corresponding database with this username, false otherwise.
    """
    user = getUserByUsername(username)

    return not (user is None)


def userExistsByEmail(email: str):
    """
    Return true if a user exists in corresponding database with this email, false otherwise.
    """
    user = getUserByEmail(email)

    return not (user is None)

def checkUserRole(user, role: str):
    """
    Given a user and a role, check if user.role matches with role
    """
    return role == user[UserModel.role]


@deprecation.deprecated("Use getUserByUsername() instead")
def getStudentByUsername(username: str):
    """
    Return a user from the database by its username
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        "SELECT * FROM students_signup_db WHERE username = ?", (username,))

    student = c.fetchone()
    conn.commit()
    conn.close()
    return student


@deprecation.deprecated("Use getUserByEmail() instead")
def getStudentByEmail(email: str):
    """
    Return a user from the database by its email
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Check if the email exists in the database
    c.execute(
        "SELECT * FROM students_signup_db WHERE email = ?", (email,))

    student = c.fetchone()
    conn.commit()
    conn.close()
    return student


@deprecation.deprecated("Use getUserByUsername() instead")
def getTeacherByUsername(username: str):
    """
    Return a teacher from the teacher database by its username
    """
    conn = sqlite3.connect('teachers_signup_db.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        "SELECT * FROM teachers_signup_db WHERE username = ?", (username,))

    teach = c.fetchone()
    return teach


@deprecation.deprecated("Use getUserByEmail() instead")
def getTeacherByEmail(email: str):
    """
    Return a teacher from the teacher database by its email
    """
    conn = sqlite3.connect('teachers_signup_db.db')
    c = conn.cursor()

    # Check if the email exists in the database
    c.execute(
        "SELECT * FROM teachers_signup_db WHERE email = ?", (email,))

    teach = c.fetchone()
    return teach

###### for it staff ##########################


@deprecation.deprecated("Use getUserByUsername() instead")
def getItStaffByUsername(username: str):
    """
    Return a it staff from the it staff database by its username
    """
    conn = sqlite3.connect('it_staff_signup_db.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        "SELECT * FROM it_staff_signup_db WHERE username = ?", (username,))

    itStaff = c.fetchone()
    return itStaff


@deprecation.deprecated("Use getUserByEmail() instead")
def getItStaffByEmail(email: str):
    """
    Return a it staff from the it staff database by its email
    """
    conn = sqlite3.connect('it_staff_signup_db.db')
    c = conn.cursor()

    # Check if the email exists in the database
    c.execute("SELECT * FROM it_staff_signup_db WHERE email = ?", (email,))

    itStaff = c.fetchone()
    return itStaff
###### for it staff ##########################


@deprecation.deprecated("Use userExistsByUsername() instead")
def teacherExistsByUsername(username: str):
    """
    Return true if a teacher exists in teacher database with this username, false otherwise.
    """
    teacher = getTeacherByUsername(username)

    return not (teacher is None)


@deprecation.deprecated("Use userExistsByEmail() instead")
def teacherExistsByEmail(email: str):
    """
    Return true if a teacher exists in teacher database with this email, false otherwise.
    """
    teacher = getTeacherByEmail(email)

    return not (teacher is None)


@deprecation.deprecated("Use userExistsByUsername() instead")
def studentExistsByUsername(username: str):
    """
    Return true if a student exists in database with this username, false otherwise.
    """
    student = getStudentByUsername(username)

    return not (student is None)


@deprecation.deprecated("Use userExistsByEmail() instead")
def studentExistsByEmail(email: str):
    """
    Return true if a student exists in database with this email, false otherwise.
    """
    student = getStudentByEmail(email)

    return not (student is None)


@deprecation.deprecated("Use userExistsByUsername() instead")
def itStaffExistsByUsername(username: str):
    """
    Return true if a it staff exists in database with this username, false otherwise.
    """
    it_staff = getItStaffByUsername(username)

    return not (it_staff is None)


@deprecation.deprecated("Use userExistsByEmail() instead")
def itStaffExistsByEmail(email: str):
    """
    Return true if a it staff exists in database with this email, false otherwise.
    """
    it_staff = getItStaffByEmail(email)

    return not (it_staff is None)


def encrypt_password(password: str):
    """
    Takes a string, applies salting and hashing
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def check_password(user, password: str):
    """
    Given a user and a raw password, checks if password is correct
    """

    hashed_password = user[UserModel.password]
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def check_username(user, username: str):
    username_str = user[UserModel.username]
    return username_str == username


def check_email(user, email: str):
    email_str = user[UserModel.email]
    return email_str == email


def change_user_password(email: str, password: str):

    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    # Update the password for the student with the given email
    c.execute(f"UPDATE {DB.users} SET password = ? WHERE email = ?",
              (encrypt_password(password), email))
    conn.commit()
    conn.close()


@deprecation.deprecated("Use change_user_password() instead")
def change_student_password(email: str, password: str):
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Update the password for the student with the given email
    c.execute("UPDATE students_signup_db SET password = ? WHERE email = ?",
              (encrypt_password(password), email))
    conn.commit()
    conn.close()


@deprecation.deprecated("Use change_user_password() instead")
def change_teacher_password(email: str, password: str):
    conn = sqlite3.connect('teachers_signup_db.db')
    c = conn.cursor()

    # Update the password for the student with the given email
    c.execute("UPDATE teachers_signup_db SET password = ? WHERE email = ?",
              (encrypt_password(password), email))
    conn.commit()
    conn.close()


@deprecation.deprecated("Use change_user_password() instead")
def change_it_staff_password(email: str, password: str):
    conn = sqlite3.connect('it_staff_signup_db.db')
    c = conn.cursor()

    # Update the password for the student with the given email
    c.execute("UPDATE it_staff_signup_db SET password = ? WHERE email = ?",
              (encrypt_password(password), email))
    conn.commit()
    conn.close()
