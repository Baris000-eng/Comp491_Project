from flask import render_template, session, request, redirect, url_for
import sqlite3
import random
import string
import pandas as pd
import datetime
import pytz
import repository.ReservationRepository as RR
import service.UserService as US
import service.ClassroomService as CS
import service.MailSendingService as MSS
from constants import ReservationConstants as RC

DEBUG = True

reservation_information = list()

def view_reservation_code_viewing_screen():
    reservation_code = generate_classroom_reservation_code()
    return render_template("reservation_code.html", reservation_code=reservation_code)

def getReservationInformation():
    return reservation_information
    
def check_course_or_exam_conflict():
    return "Hello World"

def reserve_class():
    role = session["role"]
    class_code = request.form['class-code']
    start_time = request.form['start-time']
    end_time = request.form['end-time']
    date = request.form['date']
    option = request.form['option']
    classroom_code_options = CS.getAllClassroomCodes()

    preference = str()
    if option == "exam":
        preference = "Exam"
    elif option == "lecture":
        preference = "Lecture"
    elif option == "ps":
        preference = "PS"
    elif option == "private":
        preference = "Private Study"
    elif option == "public":
        preference = "Public Study"
    elif option == "maintenance":
        preference = "Maintenance"
    elif option == "repair":
        preference = "Repair"

    username = session.get("username")
    priority = US.getPriorityByUsername(username)

    global reservation_information
    reservation_information.append(username)
    reservation_information.append(role)
    reservation_information.append(priority)
    reservation_information.append(class_code)
    reservation_information.append(start_time)
    reservation_information.append(end_time)
    reservation_information.append(date)
    reservation_information.append(preference)

    is_valid, error_string = validateReservation(role, date, start_time, end_time, class_code)

    if is_valid:
        # Reserv is valid, create reservation
        RR.createReservation(role, date, start_time, end_time, username, preference, class_code, priority)
        return render_template("return_success_message_classroom_reserved.html")
    
    else:
        if error_string != RC.reservation_conflicting_error:
            # Reserv is not valid, throw error message
            if DEBUG:
                print(f"Reserv is not valid, throw error message")
            return render_template(role + "_reservation_screen.html",
                                error_msg=error_string,
                                options=classroom_code_options)
        
        else:
            conflicting_ids = getConflictingIds(date, start_time, calculateDuration(start_time, end_time), class_code)
            isOverrideable = isConflictOverrideable(conflicting_ids, priority)
            if not isOverrideable:
                # Reserv is neither valid nor overrideable, throw error message
                if DEBUG:
                    print(f"Reserv is neither valid nor overrideable, throw error message")
                return render_template(role + "_reservation_screen.html",
                    error_msg=error_string,
                    options=classroom_code_options)
            else:
                # Reserv is not valid, but overrideable, remove conflicting reservations, create this reservation
                if DEBUG:
                    print(f"Reserv is not valid, but overrideable, remove conflicting reservations, create this reservation")
                
                usernames = getUsernameByReservationId(conflicting_ids)
                MSS.sendReservationOverrideMail(usernames)

                for conflicting_id in conflicting_ids:
                    RR.deleteReservationById(conflicting_id)
                

                RR.createReservation(role, date, start_time, end_time, username, preference, class_code, priority)
                return render_template("return_success_message_classroom_reserved.html")


def seeTheReservations():
    data = RR.getAllReservations()
    return render_template('admin_pages/see_the_reservations.html', reservations=data)

def getUsernameByReservationId(ids):
    usernames = RR.getUsernameByReservationId(ids)
    if DEBUG:
        print(usernames)
    return usernames


def see_already_reserved_classes():
    rows = RR.getAllReservations()
    return render_template('classroom_inside_reservation.html', rows=rows)

def getReservations(reservationType):
    if reservationType == "myReservations":
        reservations = RR.getReservationsByUsername(session.get("username"))
        return render_template('classroom_inside_reservation.html', rows=reservations, reservation_type = reservationType)
    else:
        reservations = RR.getAllReservations()
        return render_template('classroom_inside_reservation.html', rows=reservations)


def reservedClassroomsByInterval(start_date, start_time, duration):
    """
    Finds the classrooms that are occupied by a reservation between start_date,start_time to start_date,start_time + duration
    There is an occupation for a classroom if there exists a reservation at that classroom that satisfies all rules:
    1. Starts before the end of the specified datetime: (start_date,start_time + duration)
    2. Ends after the start of the specified datetime:  (start_date,start_time)

    :param start_date: String in the form of "YYYY-MM-DD" that specifies the date of interest, ex: "2023-06-24"
    :param start_time: String in the form of "HH:MM" that specifies the time of interest, ex: "18:45"
    :param duration: Integer that specifies the duration of interest IN MINUTES
    """

    info_tuples = RR.reservedClassroomsByInterval(start_date, start_time, duration)
    ids_list = [code[0] for code in info_tuples]
    codes_list = [code[1] for code in info_tuples]

    if DEBUG:
        print(f"ids_list: {ids_list}")

    return ids_list, codes_list

def check_time_interval_conflict(date, start_time, duration_in_minutes, class_code):
    # Call reservedClassroomsByInterval
    _, occupied_classcodes = reservedClassroomsByInterval(date, start_time, duration_in_minutes)

    if class_code in occupied_classcodes:
        return True
    else:
        return False
    

def getConflictingIds(date, start_time, duration_in_minutes, class_code):
    reservation_ids, occupied_classcodes = reservedClassroomsByInterval(date, start_time, duration_in_minutes)
    conflicting_ids = [res_id for i, res_id in enumerate(reservation_ids) if occupied_classcodes[i] == class_code]

    return conflicting_ids

def isConflictOverrideable(conflicting_ids, priority):
    if not conflicting_ids:
        return False
    
    conflicting_priorities = [RR.getPriorityById(id)[0] for id in conflicting_ids]
    max_priority = max(conflicting_priorities)
    if DEBUG:
        print(f'conflicting_ids: {conflicting_ids}')
        print(f'conflicting_priorities: {conflicting_priorities}')
        print(f'max_priority: {max_priority}')
        print(f'priority: {priority}')
    if max_priority >= priority:
        return False
    
    return True


def calculateDuration(start_time, end_time):
    # Calculate duration in minutes
    start_datetime = datetime.datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.datetime.strptime(end_time, "%H:%M")
    duration = end_datetime - start_datetime
    duration_in_minutes = duration.total_seconds() // 60
    if duration_in_minutes < 0:
        duration_in_minutes += 1440

    return duration_in_minutes


def validateReservation(role, date, start_time, end_time, class_code):
    duration = calculateDuration(start_time, end_time)
    timezone = pytz.timezone("Turkey")
    current_datetime = datetime.datetime.now(timezone)
    start_datetime_obj = datetime.datetime.strptime(f'{date} {start_time}', ("%Y-%m-%d %H:%M"))
    start_datetime_obj = timezone.localize(start_datetime_obj)

    if start_datetime_obj < current_datetime:
        if DEBUG:
            print("DEBUG MODE: This is not a valid time. It is in past")
        return False, RC.reservation_in_past_error
    
    if duration > RC.RESERVATION_UPPER_LIMIT:
        return False, RC.reservation_too_long_error
    
    if check_time_interval_conflict(date, start_time, duration, class_code):
        return False, RC.reservation_conflicting_error
    
    return True, ""

def editClassroomReservations():
    row = request.args.get('row_data').split(',')
    return render_template("editReservations.html", row=row)


def deleteReservation():
    if request.method == "POST":
        role = request.form['role']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        username = request.form['username_of_reserver']
        public_or_private = request.form['reservation_purpose']
        classroom = request.form['classroom_name']
        priority_reserved = request.form['priority_reserved']
        RR.delete_reservation_from_db(
            role=role,
            date=date,
            start_time=start_time,
            end_time=end_time,
            username=username,
            public_or_private=public_or_private,
            classroom=classroom,
            priority_reserved=priority_reserved
        )
        return render_template("successfulDeletionOfClassReservation.html")
    else:
        return render_template("editReservations.html")


def updateReservation():
    if request.method == 'POST':
        current_reservation_id = request.form['reservation_id']
        user_role = request.form['role']
        reservation_date = request.form['date']
        reservation_start_time = request.form['start_time']
        reservation_end_time = request.form['end_time']
        reserver_username = request.form['username_of_reserver']
        reservation_purpose = request.form['reservation_purpose']
        reserved_classroom = request.form['classroom_name']
        priority_reserved = request.form['priority_reserved']
        RR.updateReservation(
            role=user_role,
            date=reservation_date,
            start_time=reservation_start_time,
            end_time=reservation_end_time,
            username=reserver_username,
            reservation_purpose=reservation_purpose,
            reserved_classroom=reserved_classroom,
            priority_reserved=priority_reserved,
            id=current_reservation_id
        )
        return redirect(url_for('successfulUpdateOfReservation'))
    else:
        return render_template('editReservations.html')
    
def generate_classroom_reservation_code():
    alphabet = string.ascii_letters + string.digits
    if 'reservation_code' in session:
        reservation_code = session['reservation_code']
    else:
        reservation_code = ''.join(random.choice(alphabet) for i in range(8))
        session['reservation_code'] = reservation_code
    return reservation_code

def openStudentReservationScreen():
    options = CS.getAllClassroomCodes()
    selected_class_code = request.form.get('class_code')
    value = request.args.get('value')
    if selected_class_code is not None:
        return render_template('student_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('student_reservation_screen.html', options=options, selected=value)


def openTeacherReservationScreen():
    options = CS.getAllClassroomCodes()
    selected_class_code = request.form.get('class_code')
    if selected_class_code is not None:
        return render_template('teacher_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('teacher_reservation_screen.html', options=options)


def openITStaffReservationScreen():
    options = CS.getAllClassroomCodes()
    selected_class_code = request.form.get('class_code')
    if selected_class_code is not None:
        selected_class_code = options[int(selected_class_code)]
        return render_template('it_staff_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('it_staff_reservation_screen.html', options=options)


def OpenReserveScreen():
    class_code = request.args.get('class_code')
    return render_template("student_reservation_screen.html")


def get_reservation_statistics_screen():
    return render_template("reservation_statistics.html")


def successfulUpdateOfReservation():
    return render_template('successfulUpdateOfClassReservation.html')

