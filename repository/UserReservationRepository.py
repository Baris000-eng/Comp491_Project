import sqlite3
from constants import DB
import repository.Repository as Repo

def initializeUserReservationsTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.user_reservation} (
                    reservation_id INTEGER,
                    user_id INTEGER,
                    is_owner BOOLEAN,
                    PRIMARY KEY (reservation_id, user_id),
                    FOREIGN KEY (reservation_id) REFERENCES {DB.reservations}(id),
                    FOREIGN KEY (user_id) REFERENCES {DB.users}(id) )''')
    
    conn.commit()
    conn.close()


def createUserReservation(reservation_id, user_id, is_owner):
    c, conn = Repo.getCursorAndConnection()
    c.execute(f'''INSERT INTO {DB.user_reservation} (reservation_id, user_id, is_owner)
    VALUES (?, ?, ?)''', (reservation_id, user_id, is_owner))

    conn.commit()
    conn.close()    
    


    