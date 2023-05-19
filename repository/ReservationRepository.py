import sqlite3

def initializeReservationsTable():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS reservations_db (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              role TEXT NOT NULL,
              date DATE NOT NULL, 
              start_time TIME NOT NULL, 
              end_time TIME NOT NULL,
              username TEXT DEFAULT "NO_NAME_GIVEN", 
              public_or_private TEXT,
              classroom TEXT,
              priority_reserved INTEGER)''')
    
def getAllReservations():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reservations_db')
    data = c.fetchall()
    conn.close()
    return data

def updateReservation(role, date, start_time, end_time, username, reservation_purpose, reserved_classroom, priority_reserved, id):
    conn = sqlite3.connect("reservations_db.db")
    c = conn.cursor()

    c.execute("UPDATE reservations_db SET role=?, date=?, start_time=?, end_time=?, username=?, public_or_private=?, classroom = ?, priority_reserved=? WHERE id=?", 
                (role, date, start_time, end_time, username, reservation_purpose, reserved_classroom, priority_reserved, id))

    conn.commit()
    conn.close()

def delete_reservation_from_db(role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved):
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    c.execute('''DELETE FROM reservations_db WHERE
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