import sqlite3
import csv

from constants import DB
from constants import ClassroomModel as CM

def initializeClassroomTables():
    conn = sqlite3.connect(f"{DB.classrooms}.db")
    c = conn.cursor()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.classrooms}
                (code TEXT PRIMARY KEY, 
                department TEXT NOT NULL, 
                room_type TEXT NOT NULL,
                seats INTEGER,
                area FLOAT,
                board_num INTEGER,
                board_type TEXT,
                board_size TEXT,
                connections TEXT,
                projector_size TEXT,
                panopto_capture TEXT,
                touch_screen TEXT,
                document_camera TEXT,
                outlets_for_students TEXT,
                projector_num INTEGER
                )''')
    
    conn.commit()
    conn.close()

def createClassrooms(csv_source: str):
    conn = sqlite3.connect(f"{DB.classrooms}.db")
    c = conn.cursor()

    try:
        with open(csv_source, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Iterate through CSV file and insert each row
            for row in csv_reader:
                c.execute(f'''INSERT INTO {DB.classrooms} (code, department, room_type, seats, area, board_num, board_type,
                                                            board_size, connections, projector_size, panopto_capture, 
                                                            touch_screen, document_camera, outlets_for_students, projector_num)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (tuple(row)))
                conn.commit()
    
    except FileNotFoundError:
        return '', 404
    
    finally:
        conn.close()

    
    
    return '', 200
    

def getAllClassrooms():
    conn = sqlite3.connect(f"{DB.classrooms}.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM {DB.classrooms}")

    classrooms = c.fetchall()
    conn.commit()
    conn.close()
    return classrooms