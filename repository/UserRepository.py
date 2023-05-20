import sqlite3
import bcrypt
import deprecation
from flask import session
from constants import ROLES
from constants import DB
from constants import UserModel
import sqlite3


def getAllUsers():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users_db')
    users = c.fetchall()
    conn.close()
    return users


def updateITReport(report_no, room_name, faculty_name, problem_description, date, time):
    conn = sqlite3.connect("IT_Report_logdb.db")
    c = conn.cursor()

    c.execute("UPDATE IT_Report_logdb SET room_name=?, faculty_name=?, problem_description=?, date=?, time=? WHERE it_report_no=?",
              (room_name, faculty_name, problem_description, date, time, report_no))

    conn.commit()
    conn.close()


def getAllITReports():
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM IT_Report_logdb')
    data = c.fetchall()
    conn.close()
    return data


def delete_it_report_from_db(report_no, room_name, faculty_name, problem_description, date, time):
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()
    c.execute('''DELETE FROM IT_Report_logdb WHERE
                 it_report_no = ? AND
                 room_name = ? AND
                 faculty_name = ? AND
                 problem_description = ? AND
                 date = ? AND
                 time = ?''',
              (report_no, room_name, faculty_name, problem_description, date, time))
    conn.commit()
    conn.close()


def insert_news_to_newsdb(news_message, time, date, time_end, date_end, sender, role):
    conn = sqlite3.connect('news_db.db')
    c = conn.cursor()
    c.execute('''INSERT INTO news_db (news_message, time, date, time_end, date_end, sender, role) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (news_message, time, date, time_end, date_end, sender, role))
    conn.commit()
    conn.close()


def getAllITReports():
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM IT_Report_logdb')
    rows = c.fetchall()
    return rows


def getAllUsernames():
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users_db')
    usernames = [row[0] for row in c.fetchall()]
    conn.close()
    return usernames


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


def initializeChatTable():
    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS chat_db
             (classroom TEXT,
              time TIME NOT NULL, 
              date DATE NOT NULL, 
              sender TEXT DEFAULT "NO_NAME_GIVEN", 
              message TEXT )''')


def initializeNewsTable():
    conn = sqlite3.connect('news_db.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS news_db
             (news_message TEXT,
              time str DEFAULT "NO_NAME_GIVEN" , 
              date DATE DEFAULT "NO_NAME_GIVEN", 
              time_end TIME DEFAULT "NO_NAME_GIVEN", 
              date_end DATE DEFAULT "NO_NAME_GIVEN", 
              sender TEXT DEFAULT "NO_NAME_GIVEN", 
              role TEXT DEFAULT "NO_NAME_GIVEN"
              )''')


def getNews():
    conn = sqlite3.connect('news_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news_db')
    news_data = c.fetchall()
    conn.close()
    return news_data


def getNewsCount():
    conn = sqlite3.connect('news_db.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM news_db')
    news_count = c.fetchone()[0]
    conn.close()
    return news_count


def createNews(news_message, time, date, time_end, date_end, sender, role):
    """
    Given a news_message, time, date, time_end, date_end, sender, role insert new news message into the news_db database
    """
    conn = sqlite3.connect('news_db.db')
    c = conn.cursor()
    if news_message == None:
        news_message = "not specified"
    if time == None:
        time = "not specified"
    if date == None:
        date = "not specified"
    if time_end == None:
        time_end = "not specified"
    if date_end == None:
        date_end = "not specified"
    if sender == None:
        sender = "not specified"
    if role == None:
        role = "not specified"

    c.execute('''INSERT INTO news_db (news_message, time, date, time_end, date_end, sender, role) 
             VALUES (?, ?, ?, ?, ?, ?, ?)''', (news_message, time, date, time_end, date_end, sender, role))

    conn.commit()
    conn.close()


def createChat(classroom, time, date, sender, message):
    """
    Given a classroom, time, date, sender, role, flagged, insert new chat message into the chat database
    """
    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()

    c.execute('''INSERT INTO chat_db (classroom, time, date, sender, message) 
             VALUES (?, ?, ?, ?, ?)''', (classroom, time, date, sender, message))

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


def getUserByUsernameAndEmail(username: str, email: str):
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


def userExistsByUsernameAndEmail(username: str, email: str):
    """
    Return true if a user exists in corresponding database with this email and username, false otherwise.
    """
    user = getUserByUsernameAndEmail(username=username, email=email)
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


def deleteUser(username, user_email, user_role, user_priority, user_id):
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    c.execute(f"DELETE FROM {DB.users} WHERE username=? AND email=? AND role=? AND priority=? AND id=?",
              (username, user_email, user_role, user_priority, user_id))

    conn.commit()
    conn.close()


def updateUserInformation(user_id, username, user_email, user_role, user_priority):
    conn = sqlite3.connect(f'{DB.users}.db')
    c = conn.cursor()

    c.execute(f"UPDATE {DB.users} SET username=?, email=?, role=?, priority=? WHERE id=?",
              (username, user_email, user_role, user_priority, user_id))

    conn.commit()
    conn.close()
