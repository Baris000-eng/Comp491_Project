import sqlite3
import csv
from typing import List

from constants import DB
from constants import FilterOperations as FO

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

def getClassroomsWhere(criteria: dict):
    """
    Given filtering opitons as a dictionary, return the classrooms that fit the filtering 
    """
    print(f'criteria: {criteria}')

    query, parameters = getQuery(criteria)
    

    print(f'query: {query}')
    print(f'parameters: {parameters}')

    conn = sqlite3.connect(f"{DB.classrooms}.db")
    c = conn.cursor()
    c.execute(query, parameters)

    classrooms = c.fetchall()
    conn.commit()
    conn.close()

    return classrooms
    

def getQuery(criteria: dict):
    """
    Given a dictionary of filtering criteria and values, construct corresponding query string and parameter list
    Example: 
        criteria: {'department': ['SOS', 'ENG'], 'panopto_capture': ['available'], 'projector_num': ['1', '2']}
        query: "SELECT * FROM classrooms_db WHERE ( department = ? or department = ? ) and ( panopto_capture like ? ) and ( projector_num = ? or projector_num = ? )"
        parameters: ['SOS', 'ENG', 'available', '1', '2']
    """
    parameter_list = []
    where_clauses = []
    
    for criterion, values in criteria.items():
        where_clause, param_list = getWhereClauseAndParamList(criterion, values)
        
        if param_list: # is empty check
            where_clauses.append(where_clause)
            parameter_list += param_list


    where_clause = f'{" and ".join(where_clauses)}'
    query = f"SELECT * FROM {DB.classrooms} WHERE {where_clause}"
    return query, parameter_list

def getWhereClauseAndParamList(criterion: str, values: List):
    """
    Given a filter criterion and filter values, return the corresponding where clause and the parameter binding list
    If given criterion is invalid, return empty string and an empty list.
    Example:
        criterion: "code"
        values: ["SOS B08", "ENG Z15"]
        where_clause: '( code = ? or code = ? )'
        parameter_list: ['SOS B08', 'ENG Z15']
    """
    if criterion not in FO:
        return "", []
    
    where_clauses = []
    parameter_list = []
    
    for value in values:
        where_clauses.append(f"{criterion} {FO.get(criterion)} ?")
        parameter_list.append(value)
    
    where_clause = f'( {" or ".join(where_clauses)} )'

    return where_clause, parameter_list
