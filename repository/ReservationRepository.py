import sqlite3
import datetime
from constants import DB
import datetime

DEBUG = True

def initializeReservationsTable():
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.reservations} (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              role TEXT NOT NULL,
              date DATE NOT NULL, 
              start_time TIME NOT NULL, 
              end_time TIME NOT NULL,
              username TEXT DEFAULT "NO_NAME_GIVEN", 
              public_or_private TEXT,
              classroom TEXT,
              priority_reserved INTEGER)''')
    
def createReservation(role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()
    c.execute('''INSERT INTO reservations_db (role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved))

    conn.commit()
    conn.close()


def getAllReservations():
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM {DB.reservations}')
    data = c.fetchall()
    conn.close()
    return data

def getReservationsByUsername(username: str):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {DB.reservations} WHERE username = ?", (username,))
    data = c.fetchall()
    conn.close()
    return data

def getPriorityById(id):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f"SELECT priority_reserved FROM {DB.reservations} WHERE id = ?", (id,))
    priority = c.fetchone()
    conn.close()
    return priority


def updateReservation(role, date, start_time, end_time, username, reservation_purpose, reserved_classroom, priority_reserved, id):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f"UPDATE {DB.reservations} SET role=?, date=?, start_time=?, end_time=?, username=?, public_or_private=?, classroom = ?, priority_reserved=? WHERE id=?", 
                (role, date, start_time, end_time, username, reservation_purpose, reserved_classroom, priority_reserved, id))

    conn.commit()
    conn.close()

def delete_reservation_from_db(role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f'''DELETE FROM {DB.reservations} WHERE
                 role = ? AND
                 date = ? AND
                 start_time = ? AND
                 end_time = ? AND 
                 username = ? AND
                 public_or_private = ? AND
                 classroom = ? AND
                 priority_reserved = ?''',
              (role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved))

    conn.commit()
    conn.close()

def deleteReservationById(id):
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    c.execute(f'''DELETE FROM {DB.reservations} WHERE
                 id = ?''',
              (id,))
    conn.commit()
    conn.close()    

def reservedClassroomsByInterval(start_date, start_time, duration):
    """
    Finds the classrooms that are occupied by a reservation between start_date,start_time to start_date,start_time + duration
    There is an occupation for a classroom if there exists a reservation at that classroom that satisfies all rules:
    1. Starts before the end of the specified datetime: (start_date,start_time + duration)
    2. Ends after the start of the specified datetime:  (start_date,start_time)

    :param start_date: String in the form of "YYYY-MM-DD" that specifies the date of interest, ex: "2023-06-24"
    :param start_time: String in the form of "HH:MM" that specifies the time of interest, ex: "18:45"
    :param duration: Integer that specifies the duration of interest IN MINUTES
    """
    conn = sqlite3.connect(f'{DB.reservations}.db')
    c = conn.cursor()

    start_datetime = f'{start_date} {start_time}'

    query = f'''SELECT id, classroom FROM {DB.reservations}
                WHERE 
                    ((date || " " || start_time) < datetime("{start_datetime}", "+{duration} minutes")
                    and (date || " " || end_time) > "{start_datetime}"
                    and start_time < end_time)
                or
                    ((date || " " || start_time) < datetime("{start_datetime}", "+{duration} minutes")
                    and datetime(date || " " || end_time, "+1 days") > "{start_datetime}"
                    and start_time > end_time)'''

    c.execute(query)
    
    reservation_info = c.fetchall()

    if DEBUG:
        print(f'Conflicting: {reservation_info}')
        print(f'conflict check query: {query}')
    conn.close()

    return reservation_info

