import sqlite3
import bcrypt
from flask import session
from constants import ROLES
from constants import DB
from constants import UserModel
import repository.Repository as Repo
import sqlite3


def getAllUsers():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT * FROM users_db')
    users = c.fetchall()
    conn.close()
    return users


def updateITReport(report_no, room_name, faculty_name, problem_description, date, time):
    c, conn = Repo.getCursorAndConnection()

    c.execute("UPDATE IT_Report_logdb SET room_name=?, faculty_name=?, problem_description=?, date=?, time=? WHERE it_report_no=?",
              (room_name, faculty_name, problem_description, date, time, report_no))

    conn.commit()
    conn.close()


def getAllITReports():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT * FROM IT_Report_logdb')
    data = c.fetchall()
    conn.close()
    return data


def delete_it_report_from_db(report_no, room_name, faculty_name, problem_description, date, time):
    c, conn = Repo.getCursorAndConnection()
    c.execute('''DELETE FROM IT_Report_logdb WHERE
                 it_report_no = ? AND
                 room_name = ? AND
                 faculty_name = ? AND
                 problem_description = ? AND
                 date = ? AND
                 time = ?''',
              (report_no, room_name, faculty_name, problem_description, date, time))
    c.execute(f'''
        UPDATE {DB.itReports}
        SET it_report_no = (SELECT COUNT(*) FROM {DB.itReports} AS sub WHERE sub.it_report_no < {DB.itReports}.it_report_no) + 1
    ''')
    conn.commit()
    conn.close()


def insert_news_to_newsdb(news_message, time, date, time_end, date_end, sender, role):
    c, conn = Repo.getCursorAndConnection()
    c.execute('''INSERT INTO news_db (news_message, time, date, time_end, date_end, sender, role) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (news_message, time, date, time_end, date_end, sender, role))
    conn.commit()
    conn.close()


def getAllITReports():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT * FROM IT_Report_logdb')
    rows = c.fetchall()
    return rows


def getAllUsernames():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT username FROM users_db')
    usernames = [row[0] for row in c.fetchall()]
    conn.close()
    return usernames


def initializeUserTables():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.users}
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL, 
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL,
                priority INTEGER)''')
    conn.commit()
    conn.close()

def intializeITReportLog():
    c, conn = Repo.getCursorAndConnection()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''CREATE TABLE IF NOT EXISTS IT_Report_logdb
                (it_report_no INTEGER PRIMARY KEY AUTOINCREMENT, 
                 room_name TEXT  NOT NULL, 
                 faculty_name TEXT NOT NULL,
                 problem_description TEXT NOT NULL,
                 date DATE NOT NULL, 
                 time TIME NOT NULL
                 )''')
    conn.commit()
    conn.close()

def createITReport(room_name, faculty_name, problem_description, date, time):
    c, conn = Repo.getCursorAndConnection()

    # Create the students_signup_db table if it doesn't exist yet
    c.execute('''INSERT INTO IT_Report_logdb (room_name, faculty_name, problem_description, date, time) 
             VALUES (?, ?, ?, ?, ?)''', (room_name, faculty_name, problem_description, date, time))
    conn.commit()
    conn.close()


def initializeChatTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute('''CREATE TABLE IF NOT EXISTS chat_db
             (classroom TEXT,
              time TIME NOT NULL, 
              date DATE NOT NULL, 
              sender TEXT DEFAULT "NO_NAME_GIVEN", 
              message TEXT )''')
    conn.commit()
    conn.close()

def initializeNewsTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute('''CREATE TABLE IF NOT EXISTS news_db
             (news_message TEXT,
              time str DEFAULT "NO_NAME_GIVEN" , 
              date DATE DEFAULT "NO_NAME_GIVEN", 
              time_end TIME DEFAULT "NO_NAME_GIVEN", 
              date_end DATE DEFAULT "NO_NAME_GIVEN", 
              sender TEXT DEFAULT "NO_NAME_GIVEN", 
              role TEXT DEFAULT "NO_NAME_GIVEN"
              )''')
    conn.commit()
    conn.close()

def getNews():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT * FROM news_db')
    news_data = c.fetchall()
    conn.close()
    return news_data


def getNewsCount():
    c, conn = Repo.getCursorAndConnection()
    c.execute('SELECT COUNT(*) FROM news_db')
    news_count = c.fetchone()[0]
    conn.close()
    return news_count

def createNews(news_message, time, date, time_end, date_end, sender, role):
    """
    Given a news_message, time, date, time_end, date_end, sender, role insert new news message into the news_db database
    """
    c, conn = Repo.getCursorAndConnection()
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
    c, conn = Repo.getCursorAndConnection()

    c.execute('''INSERT INTO chat_db (classroom, time, date, sender, message) 
             VALUES (?, ?, ?, ?, ?)''', (classroom, time, date, sender, message))

    conn.commit()
    conn.close()


def createUser(username: str, password: str, email: str, role: str, priority: int):
    """
    Given a username, password, email, and role, insert user into corresponding database
    """

    session["username"] = username
    c, conn = Repo.getCursorAndConnection()
    priority = ROLES[role].priority
    c.execute(
        f"INSERT INTO {DB.users} (username, password, email, role, priority) VALUES (?, ?, ?, ?, ?)",
        (username, encrypt_password(password), email, role, priority)
    )
    conn.commit()
    conn.close()


def getUserByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.users} WHERE username = ?", (username,))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def getPriorityByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    # Check if the username exists in the database
    c.execute(
        f"SELECT priority FROM {DB.users} WHERE username = ?", (username,))

    priority = c.fetchone()
    conn.close()

    return priority


def getIdByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    c.execute(
        f"SELECT id FROM {DB.users} WHERE username = ?", (username,))

    user_id = c.fetchone()
    conn.close()

    # TODO: Add a useful try except block in case user_id is None.
    try:
        user_id = user_id[0]
    except TypeError:
        print("Be careful, could not fetch reservation id")
        user_id = -1

    return user_id


def getUserByEmail(email: str):
    c, conn = Repo.getCursorAndConnection()

    # Check if the username exists in the database
    c.execute(
        f"SELECT * FROM {DB.users} WHERE email = ?", (email,))

    user = c.fetchone()
    conn.commit()
    conn.close()
    return user


def getUserByUsernameAndEmail(username: str, email: str):
    c, conn = Repo.getCursorAndConnection()

    c.execute(
        f"SELECT * FROM {DB.users} WHERE username = ? AND email = ?", (username, email))

    user = c.fetchone()
    conn.commit()
    conn.close()
    print(user)
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

    c, conn = Repo.getCursorAndConnection()

    # Update the password for the student with the given email
    c.execute(f"UPDATE {DB.users} SET password = ? WHERE email = ?",
              (encrypt_password(password), email))
    conn.commit()
    conn.close()


def deleteUser(username, user_email, user_role, user_priority, user_id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"DELETE FROM {DB.users} WHERE username=? AND email=? AND role=? AND priority=? AND id=?",
              (username, user_email, user_role, user_priority, user_id))


    conn.commit()
    conn.close()


def updateUserInformation(user_id, username, user_email, user_role, user_priority):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"UPDATE {DB.users} SET username=?, email=?, role=?, priority=? WHERE id=?",
              (username, user_email, user_role, user_priority, user_id))

    conn.commit()
    conn.close()


def initializeEventAnnouncementsTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute('''CREATE TABLE IF NOT EXISTS event_announcements_db
                 (attendeeUsername TEXT, attendeeRole TEXT, title TEXT, 
                 start_time TEXT, end_time TEXT, start_date TEXT, 
                 end_date TEXT, senderName TEXT, senderRole TEXT)''')


def createAttendee(attendeeUsername, attendeeRole, title, start_time, end_time, start_date, end_date, sender, role):
    c, conn = Repo.getCursorAndConnection()
    c.execute("INSERT INTO event_announcements_db VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (attendeeUsername, attendeeRole, title, start_time, end_time, start_date, end_date, sender, role))

    conn.commit()
    conn.close()
    
    
def checkPreviousEventAttendance(username: str, event_title: str):
    cursor, connection = Repo.getCursorAndConnection()
    cursor.execute("SELECT COUNT(*) FROM event_announcements_db WHERE title = ? AND attendeeUsername = ?",
                   (event_title, username))
    result = cursor.fetchone()
    connection.close()

    if result and result[0] > 0:
        return True

    return False




    
   
