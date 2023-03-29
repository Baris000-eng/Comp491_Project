import sqlite3
import bcrypt


def initializeStudentTable():
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''CREATE TABLE IF NOT EXISTS students_signup_db
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL, 
                 password TEXT NOT NULL,
                 email TEXT NOT NULL)''')
    

def initializeTeachersTable():
    conn = sqlite3.connect('teachers_signup_db.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''CREATE TABLE IF NOT EXISTS teachers_signup_db
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL, 
                 password TEXT NOT NULL,
                 email TEXT NOT NULL)''')
    

def initializeItStaffTable():
    conn = sqlite3.connect('it_staff_signup_db.db')
    c = conn.cursor()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''CREATE TABLE IF NOT EXISTS it_staff_signup_db
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT NOT NULL, 
                 password TEXT NOT NULL,
                 email TEXT NOT NULL)''')


def createUser(username, password, email):
    """
    Given a username, password, and email, insert new user into the database
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO students_signup_db (username, password, email) VALUES (?, ?, ?)",
        (username, encrypt_password(password=password), email)
    )
    conn.commit()
    conn.close()


def getUserByUsername(username: str):
    """
    Return a user from the database by its username
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Check if the username exists in the database
    c.execute(
        "SELECT * FROM students_signup_db WHERE username = ?", (username,))

    student = c.fetchone()
    return student


def getUserByEmail(email: str):
    """
    Return a user from the database by its email
    """
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Check if the email exists in the database
    c.execute(
        "SELECT * FROM students_signup_db WHERE email = ?", (email,))

    student = c.fetchone()
    return student

def existsByUsername(username: str):
    """
    Return true if a user exists in database with this username, false otherwise.
    """
    user = getUserByUsername(username)

    return not (user is None)

def existsByEmail(email: str):
    """
    Return true if a user exists in database with this email, false otherwise.
    """
    user = getUserByEmail(email)

    return not (user is None)

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
    
    hashed_password = user[2]
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def check_username(user, username: str):
    username_str = user[1]
    return username_str == username


def check_email(user, email: str):
    email_str = user[3]
    return email_str == email


def change_password(email: str, password: str):
    conn = sqlite3.connect('students_signup_db.db')
    c = conn.cursor()

    # Update the password for the student with the given email
    c.execute("UPDATE students_signup_db SET password = ? WHERE email = ?",
                (encrypt_password(password), email))
    conn.commit()
    conn.close()