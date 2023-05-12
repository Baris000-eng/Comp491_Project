from flask import session
from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import openpyxl
from constants import ROLES
import pandas as pd
import repository.UserRepository as UR
from constants import DB
import csv
from typing import List



def initializeExamTable():

    exam_excel = 'FALL_22_EXAMS.xlsx'
    df = pd.read_excel(exam_excel)

    conn = sqlite3.connect(f"{DB.exams}.db")
    table_name = 'exams'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
def increment_exams_db():
    exam_excel = 'FALL_22_EXAMS.xlsx'
    df = pd.read_excel(exam_excel)
    df['Exam Date'] = pd.to_datetime(df['Exam Date'])
    df['Exam Date'] = df['Exam Date'] + pd.DateOffset(years=1)

    conn = sqlite3.connect(f"{DB.exams}.db")
    table_name = 'exams'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
"""
def initializeExamTable():
    conn = sqlite3.connect(f"{DB.exams}.db")
    c = conn.cursor()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {DB.exams}
                (subject TEXT,
                catalog TEXT,
                descr TEXT,
                section TEXT,
                course_id TEXT,
                exam_date TEXT,
                start_time TEXT,
                end_time TEXT,
                facil_id TEXT,
                exam_type TEXT,
                tot_enrl INTEGER,
                acad_org TEXT,
                term INTEGER
                )''')
    
    conn.commit()
    conn.close()

def createExams(csv_source: str):
    conn = sqlite3.connect(f"{DB.exams}.db")
    c = conn.cursor()

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