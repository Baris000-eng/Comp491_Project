import repository.ClassroomRepository as CR
import service.ReservationService as RS
import service.ExamService as ES
from constants import VacancyCheckRequirements as VCR
from constants import ClassroomModel as CM
from flask import render_template
from flask import request


DEBUG = True

def showTheClassroomAndInfo():
    return render_template("Classroom_reservation_students_view.html")

def getAllClassrooms():
    return CR.getAllClassrooms()

def getAllClassroomCodes():
    codes_tuples = CR.getAllClassroomCodes()
    codes_list = [code[0] for code in codes_tuples] 
    return codes_list

def getSeatsByCode(class_code):
    return CR.getSeatsByCode(class_code)

def createClassrooms(csv_source: str):
    """
    Given a path to csv file import data to classroom repository
    """
    return CR.createClassrooms(csv_source)

def showClassroomSearchAndFilterScreen():
    classroom_names = CR.getAllClassroomNames()
    departments = CR.getAllDepartmentNames()
    return render_template("classroom_search_and_filtering_screen.html", classroom_names = classroom_names, departments = departments)
    

def getClassroomsWhere(criteria: dict=None):
    if criteria is None:
        return CR.getAllClassrooms()
    
    filtered_criteria, operations = filter_criteria(criteria=criteria)

    # Turn each comma-seperated dictionary value to a list of string
    for k,v in filtered_criteria.items():
        try:
            filtered_criteria[k] = v.split(",")
        except AttributeError:
            # Skip values that do not have the attribute 'split'
            continue
    
    if not filtered_criteria:
        classrooms = CR.getAllClassrooms()
    
    else:
        classrooms = CR.getClassroomsWhere(filtered_criteria, operations)

    if isVacanyCheckNeeded(criteria):
        vacancy_criteria = [criteria.get(req) for req in VCR]
        classrooms = excludeAllBusyClassrooms(vacancy_criteria, classrooms)

        
    return classrooms

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


def isVacanyCheckNeeded(criteria: dict):
    # Check for vacancy filtering
    if "checkbox_vacant" not in criteria:
        return False
    
    # Ensure neccessary fields are all non-empty
    for requirement in VCR:
        if not criteria.get(requirement):
            return False

    return True

def excludeAllBusyClassrooms(vacancy_criteria, classrooms):
    classrooms = excludeReservedClassrooms(vacancy_criteria, classrooms)
    classrooms = excludeExamClassrooms(vacancy_criteria, classrooms)

    return classrooms


def excludeReservedClassrooms(vacancy_criteria, classrooms):
    _, busy_classrooms_codes = RS.reservedClassroomsByInterval(*vacancy_criteria)
    filtered_classrooms = excludeClassrooms(classrooms, busy_classrooms_codes)
    return filtered_classrooms

def excludeExamClassrooms(vacancy_criteria, classrooms):
    _, exam_classcodes = ES.examsByInterval(*vacancy_criteria)
    filtered_classrooms = excludeClassrooms(classrooms, exam_classcodes)
    return filtered_classrooms


def excludeClassrooms(source_classrooms, exclude_codes):
    exclude_codes = [code.replace(" ", "") for code in exclude_codes]
    exclude_codes_set = set(exclude_codes) # Turn to a set for efficiency
    return [classroom for classroom in source_classrooms if classroom[CM.code].replace(" ", "") not in exclude_codes_set]
