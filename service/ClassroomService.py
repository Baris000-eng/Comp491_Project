import repository.ClassroomRepository as CR

def createClassrooms(csv_source: str):
    """
    Given a path to csv file import data to classroom repository
    """
    return CR.createClassrooms(csv_source)

def getAllClassrooms():
    return CR.getAllClassrooms()

def getClassroomsWhere(criteria: dict):
    mutable_criteria = {} 

    # Turn each comma-seperated dictionary value to a list of string
    for k,v in criteria.items():
        mutable_criteria[k] = v.split(",")

    return CR.getClassroomsWhere(mutable_criteria)