import sqlite3
from constants import DB
import datetime
import service.UserReservationService as URS
import service.UserService as US
import repository.Repository as Repo

DEBUG = True

def sendReservationCode():
    return "Reservation Code Sent"

def initializeReservationsTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.reservations} (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              role TEXT NOT NULL,
              date DATE NOT NULL, 
              start_time TIME NOT NULL, 
              end_time TIME NOT NULL,
              public_or_private TEXT,
              classroom TEXT,
              priority_reserved INTEGER)''')
    
    conn.commit()
    conn.close()
    
def createReservation(role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved):
    c, conn = Repo.getCursorAndConnection()
    c.execute('''INSERT INTO reservations_db (role, date, start_time, end_time, public_or_private, classroom, priority_reserved)
    VALUES (?, ?, ?, ?, ?, ?, ?)''', (role, date, start_time, end_time, public_or_private, classroom, priority_reserved))
    conn.commit()
    conn.close()

    reservation_id = getReservationId(role, date, start_time, end_time, public_or_private, classroom, priority_reserved)
    
    # FIXME: Works but probably a bad practice to call service layer here
    user_id = US.getIdByUsername(username)

    # FIXME: Works but probably a bad practice to call service layer here
    URS.createUserReservation(reservation_id, user_id, True)



def getAllReservations():
    c, conn = Repo.getCursorAndConnection()

    query = f'''SELECT r.id, r.role, r.date, r.start_time, r.end_time, u.username, r.public_or_private, r.classroom, r.priority_reserved
                FROM {DB.reservations} as r
                JOIN {DB.user_reservation} AS ur ON r.id = ur.reservation_id
                JOIN {DB.users} AS u ON ur.user_id = u.id'''

    c.execute(query)
    data = c.fetchall()
    conn.close()

    return data
    

def getOwnedReservationsByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    query = f"""SELECT r.id, r.role, r.date, r.start_time, r.end_time, u.username, r.public_or_private, r.classroom, r.priority_reserved
                FROM {DB.reservations} as r
                JOIN {DB.user_reservation} AS ur ON r.id = ur.reservation_id
                JOIN {DB.users} AS u ON ur.user_id = u.id
                WHERE u.username = '{username}' and ur.is_owner = true"""

    c.execute(query)
    data = c.fetchall()
    conn.close()
    return data


def getJoinedReservationsByUsername(username: str):
    c, conn = Repo.getCursorAndConnection()

    query = f"""SELECT r.id, r.role, r.date, r.start_time, r.end_time, owner.username, r.public_or_private, r.classroom, r.priority_reserved
                FROM {DB.reservations} as r
                JOIN {DB.user_reservation} AS ur ON r.id = ur.reservation_id
                JOIN {DB.users} AS owner ON ur.user_id = owner.id
				WHERE ur.is_owner = true AND r.id IN (
				SELECT r2.id
				FROM {DB.reservations} as r2
				JOIN {DB.user_reservation} AS ur2 ON r2.id = ur2.reservation_id
				JOIN {DB.users} AS u ON ur2.user_id = u.id
				WHERE ur2.is_owner = false AND u.username = '{username}')"""

    c.execute(query)
    data = c.fetchall()
    conn.close()
    return data


def getPriorityById(id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT priority_reserved FROM {DB.reservations} WHERE id = ?", (id,))
    priority = c.fetchone()
    conn.close()
    return priority

def getPublicityById(id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT public_or_private FROM {DB.reservations} WHERE id = ?", (id,))
    priority = c.fetchone()
    conn.close()
    return priority

def getClassById(id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT classroom FROM {DB.reservations} WHERE id = ?", (id,))
    priority = c.fetchone()
    conn.close()
    return priority


def getReservationId(role, date, start_time, end_time, public_or_private, classroom, priority_reserved):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT id FROM {DB.reservations} WHERE role=? AND date=? AND start_time=? AND end_time=? AND public_or_private=? AND classroom = ? AND priority_reserved=?", 
              (role, date, start_time, end_time, public_or_private, classroom, priority_reserved))
    
    reservation_id = c.fetchone()
    conn.close()
    
    try:
        reservation_id = reservation_id[0]
    except TypeError:
        print("Be careful, could not fetch reservation id")
        reservation_id = -1

    return reservation_id   


def isUserInReservation(user_id, reservation_id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT COUNT(*) FROM {DB.user_reservation} WHERE user_id = '{user_id}' AND reservation_id = '{reservation_id}'")
    isIn = c.fetchone()[0] > 0

    conn.close()
    return isIn


def isReservationOwner(user_id, reservation_id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"SELECT COUNT(*) FROM {DB.user_reservation} WHERE user_id = '{user_id}' AND reservation_id = '{reservation_id}' AND is_owner = true")
    isOwner = c.fetchone()[0] > 0

    conn.close()
    return isOwner


def updateReservation(role, date, start_time, end_time, reservation_purpose, reserved_classroom, priority_reserved, id):
    c, conn = Repo.getCursorAndConnection()

    c.execute(f"UPDATE {DB.reservations} SET role=?, date=?, start_time=?, end_time=?, public_or_private=?, classroom = ?, priority_reserved=? WHERE id=?", 
                (role, date, start_time, end_time, reservation_purpose, reserved_classroom, priority_reserved, id))

    conn.commit()
    conn.close()

def delete_reservation_from_db(role, date, start_time, end_time, public_or_private, classroom, priority_reserved):
    reservation_id = getReservationId(role, date, start_time, end_time, public_or_private, classroom, priority_reserved)
    deleteReservationById(reservation_id)


def deleteReservationById(id):
    c, conn = Repo.getCursorAndConnection()

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
    c, conn = Repo.getCursorAndConnection()

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
    conn.close()

    return reservation_info

def getUsernameByReservationId(ids):
    c, conn = Repo.getCursorAndConnection()
    id_string = ', '.join(map(str, ids))

    query = f'''SELECT DISTINCT username
                FROM {DB.user_reservation} as UR
                JOIN {DB.users} ON UR.user_id = {DB.users}.id
                WHERE UR.reservation_id IN ({id_string})
                '''

    c.execute(query)

    users = c.fetchall()
    users = [user[0] for user in users]

    conn.close()
    return users