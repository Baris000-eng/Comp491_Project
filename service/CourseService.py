import repository.CourseRepository as COR
from flask import render_template
from constants import PAGE_SIZE

DEBUG = True

def getAllCourses():
    return getCoursesWithPagination(1)

def course_schedules():
    return getAllCourses()

def getCoursesWithPagination(pageNumber: int):
    limit = PAGE_SIZE
    offset = PAGE_SIZE * (int(pageNumber) - 1)
    courses = COR.getCoursesWithPagination(limit, offset)
    pageNumber = COR.getNumberOfPages(PAGE_SIZE)
    return render_template("course_schedules.html", pageNumber=pageNumber, courses=courses)