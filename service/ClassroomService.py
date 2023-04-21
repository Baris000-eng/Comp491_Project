import repository.ClassroomRepository as CR

def createClassrooms(csv_source: str):
    """
    Given a path to csv file import data to classroom repository
    """
    return CR.createClassrooms(csv_source)