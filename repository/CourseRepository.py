import pandas as pd
import math
import repository.UserRepository as UR
import repository.Repository as Repo
from constants import DB
from typing import List


def initializeCourseTable():
    if courseTableExists():
        return
        
    courses_excel = 'SPR_23_COURSES.xlsx'
    df = pd.read_excel(courses_excel)
    _, conn = Repo.getCursorAndConnection()

    table_name = 'courses'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def courseTableExists():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='{DB.courses}'")
    table_exists = c.fetchone()
    conn.close()

    if table_exists:
        return True
    return False

def getAllCourses():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT * FROM '{DB.courses}'")

    courses = c.fetchall()
    conn.close()

    return courses


def getCoursesWithPagination(limit, offset):
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT * FROM '{DB.courses}' LIMIT {limit} OFFSET {offset}")

    courses = c.fetchall()
    conn.close()

    return courses

def getNumberOfPages(pageSize):
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT COUNT(*) FROM '{DB.courses}'")

    count = c.fetchone()[0]
    conn.close()

    num_pages = math.ceil(count / pageSize)
    return num_pages

"""
def initializeCourseTables():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.courses}
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
"""
"""
def initializeCourseTable():
    c, conn = Repo.getCursorAndConnection()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.courses}
                (component TEXT,
                subject TEXT NOT NULL,
                catalog TEXT NOT NULL,
                section TEXT NOT NULL,
                course_id TEXT,
                descr TEXT,
                tot_enrl INTEGER,
                career TEXT,
                acad_org TEXT,
                mon TEXT,
                tues TEXT,
                wed TEXT,
                thurs TEXT,
                fri TEXT,
                sat TEXT,
                sun TEXT,
                facil_id TEXT,
                type TEXT,
                capacity INTEGER,
                mtg_start TEXT,
                mtg_end TEXT,
                start_date TEXT,
                end_date TEXT,
                term INTEGER,
                class_nbr INTEGER PRIMARY KEY,
                mode TEXT
                )''')
    
    conn.commit()
    conn.close()

def createCourses(csv_source: str):
    c, conn = Repo.getCursorAndConnection()

    try:
        with open(csv_source, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Iterate through CSV file and insert each row
            for row in csv_reader:
                c.execute(f'''INSERT INTO {DB.courses} (component, subject, catalog, section, course_id, descr, tot_enrl,
                                                            career, acad_org, mon, tues, wed, thurs, fri, sat, sun, facil_id,
                                                            type, capacity, mtg_start, mtg_end, start_date, end_date, term, class_nbr, mode)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (tuple(row)))
                conn.commit()

    except FileNotFoundError:
        return '', 404

    finally:
        conn.close()

    return '', 200

"""