import repository.ClassroomRepository as CR
from flask import render_template
from collections import defaultdict
from flask import request

def showTheClassroomAndInfo():
    return render_template("Classroom_reservation_students_view.html")

def createClassrooms(csv_source: str):
    """
    Given a path to csv file import data to classroom repository
    """
    return CR.createClassrooms(csv_source)

# def getAllClassrooms():
#     return CR.getAllClassrooms()

def getClassroomsWhere(criteria: dict={}):
        filtered_criteria, operations = filter_criteria(criteria=criteria)
        print("Before: " + str(filtered_criteria))
    

        # Turn each comma-seperated dictionary value to a list of string
        for k,v in filtered_criteria.items():
            filtered_criteria[k] = v.split(",")

        print("After: "+str(filtered_criteria))

        if not filtered_criteria:
            return CR.getAllClassrooms()
        

    
        return CR.getClassroomsWhere(filtered_criteria, operations)

def getAllDepartments():
    return CR.getAllDepartmentNames()


def filter_criteria(criteria: dict):
    filtered_criteria = {}
    operations = {}
    for key, value in criteria.items():
        # Ensure field is checked and its value is not empty
        if f'checkbox_{key}' in criteria and value:
                filtered_criteria[key] = value

        if "operation" in key:
            operations[key[10:]] = value

    return filtered_criteria, operations




   


   





    
    
