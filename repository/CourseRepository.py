from flask import session
from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import openpyxl
from constants import ROLES
import pandas as pd
import repository.UserRepository as UR
import deprecation
import datetime
import html
import random
import string
from constants import DB
import csv
from typing import List


def initializeCourseTable():
    courses_excel = 'SPR_23_COURSES.xlsx'
    df = pd.read_excel(courses_excel)
    conn = sqlite3.connect(DB.kuclass_db)

    table_name = 'courses'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

"""
def initializeCourseTables():
    conn = sqlite3.connect(DB.kuclass_db)
    c = conn.cursor()

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
    conn = sqlite3.connect(DB.kuclass_db)
    c = conn.cursor()

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
    conn = sqlite3.connect(DB.kuclass_db)
    c = conn.cursor()

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