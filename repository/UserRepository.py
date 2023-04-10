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


def createUser(username: str, password: str, email: str, role: str, priority: int):
    """
    Given a username, password, email, and role, insert user into corresponding database
    """

    session["username"] = username
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()
    priority = ROLES[role].priority
    c.execute(
        f"INSERT INTO {DB.users} (username, password, email, role, priority) VALUES (?, ?, ?, ?, ?)",
        (username, encrypt_password(password), email, role, priority)
    )
    conn.commit()
    conn.close()


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

def userExistsByUsernameAndEmail(username: str, email: str, role: str):
    """
    Return true if a user exists in corresponding database with this email and username, false otherwise.
    """
    user = getUserByUsernameAndEmail(username=username, email=email, role = role)
    return not (user is None)

def checkUserRole(user, role: str):
    """
    Given a user and a role, check if user.role matches with role
    """
    return role == user[UserModel.role]


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


