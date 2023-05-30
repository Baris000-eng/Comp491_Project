from flask import session
from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import openpyxl
import datetime
from constants import ROLES
import pandas as pd
import repository.UserRepository as UR
import repository.Repository as Repo
from constants import DB
import csv
from typing import List

DEBUG = True

# def initializeExamTable():
#     c, conn = Repo.getCursorAndConnection()

#     c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.exams}
#                 (subject TEXT,
#                 catalog TEXT,
#                 descr TEXT,
#                 section TEXT,
#                 course_id TEXT,
#                 exam_date TEXT,
#                 start_time TEXT,
#                 end_time TEXT,
#                 facil_id TEXT,
#                 exam_type TEXT,
#                 tot_enrl INTEGER,
#                 acad_org TEXT,
#                 term INTEGER
#                 )''')
    
#     conn.commit()
#     conn.close()

def initializeExamTable():
    if examTableExists():
        return
    populateExamTable()

def populateExamTable():
    populateWithIncrement()

def populateWithIncrement():
    exam_excel = 'FALL_22_EXAMS.xlsx'
    df = pd.read_excel(exam_excel)
    df['exam_date'] = pd.to_datetime(df['exam_date'])
    df['exam_date'] = df['exam_date'] + pd.DateOffset(years=1)
    df['exam_date'] = df['exam_date'].dt.strftime('%Y-%m-%d')
    df['start_time'] = [t.strftime('%H:%M') for t in df['start_time']]
    df['end_time'] = [t.strftime('%H:%M') for t in df['end_time']]

    _, conn = Repo.getCursorAndConnection()
    table_name = DB.exams
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def examTableExists():
    c, conn = Repo.getCursorAndConnection()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='{DB.exams}'")
    table_exists = c.fetchone()
    conn.close()

    if table_exists:
        return True
    return False


def examsByInterval(start_date, start_time, duration):
    """
    Finds the classrooms that are occupied by an exam between start_date,start_time to start_date,start_time + duration
    There is an occupation for a classroom if there exists an exam at that classroom that satisfies all rules:
    1. Starts before the end of the specified datetime: (start_date,start_time + duration)
    2. Ends after the start of the specified datetime:  (start_date,start_time)

    :param start_date: String in the form of "YYYY-MM-DD" that specifies the date of interest, ex: "2023-06-24"
    :param start_time: String in the form of "HH:MM" that specifies the time of interest, ex: "18:45"
    :param duration: Integer that specifies the duration of interest IN MINUTES
    """
    c, conn = Repo.getCursorAndConnection()

    start_datetime = f'{start_date} {start_time}'

    query = f'''SELECT id, facil_id FROM {DB.exams}
                WHERE 
                    ((exam_date || " " || start_time) < datetime("{start_datetime}", "+{duration} minutes")
                    and (exam_date || " " || end_time) > "{start_datetime}"
                    and start_time < end_time)
                or
                    ((exam_date || " " || start_time) < datetime("{start_datetime}", "+{duration} minutes")
                    and datetime(exam_date || " " || end_time, "+1 days") > "{start_datetime}"
                    and start_time > end_time)'''


    c.execute(query)    
    exam_ids = c.fetchall()
    conn.close()

    return exam_ids
"""
def read_exam_excel():
    exam_excel = 'FALL_22_EXAMS.xlsx'
    df = pd.read_excel(exam_excel)

    _, conn = Repo.getCursorAndConnection()
    table_name = 'exams'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def createExams(csv_source: str):
    c, conn = Repo.getCursorAndConnection()

    try:
        with open(csv_source, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Iterate through CSV file and insert each row
            for row in csv_reader:
                c.execute(f'''INSERT INTO {DB.exams} (subject, catalog, descr, section, course_id, exam_date, start_time, end_time, 
                                                            facil_id, exam_type, tot_enrl, acad_org, term)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (tuple(row)))
                conn.commit()

    except FileNotFoundError:
        return '', 404

    finally:
        conn.close()

    return '', 200
"""