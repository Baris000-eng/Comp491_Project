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

def getAllClassrooms():
    return CR.getAllClassrooms()

def getClassroomsWhere(criteria: dict):
    if request.method == "POST":
        filtered_criterias = filter_criterias(criteria=criteria)
        print("Before: "+str(filtered_criterias))
    

        # Turn each comma-seperated dictionary value to a list of string
        for k,v in filtered_criterias.items():
            filtered_criterias[k] = v.split(",")

        print("After: "+str(filtered_criterias))
    
        return CR.getClassroomsWhere(filtered_criterias)
    else:
        return render_template("Classroom_reservation_students_view.html")


def read_classrooms_and_put_to_html():
    classrooms = CR.getAllClassrooms()
    departments = CR.getAllDepartmentNames()
    return render_template("Classroom_reservation_students_view.html", classrooms = classrooms, departments = departments)

def filter_criterias(criteria: dict):
    my_dict = {}
    for key, value in criteria.items():
        if "checkbox" in key:
            my_dict[key[9:]] = criteria[key[9:]]

        if "operation" in key and key[10:] in my_dict:
            my_dict[key] = criteria[key[10:]]

    return my_dict


   


   





    
    
