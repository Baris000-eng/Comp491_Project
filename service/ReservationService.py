from flask import render_template, session, request, redirect, url_for
import sqlite3
import random
import string
import pandas as pd

import repository.ReservationRepository as RR
import service.ClassroomService as CS

DEBUG = True

def reserve_class():
    role = session["role"]
    class_code = request.form['class-code']
    start_time = request.form['start-time']
    end_time = request.form['end-time']
    date = request.form['date']
    option = request.form['option']
    classroom_code_options = CS.getAllClassroomCodes()

    conn = sqlite3.connect(f'reservations_db.db')
    c = conn.cursor()

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

    # Retrieve existing reservation
    c.execute('''SELECT * FROM reservations_db WHERE date=? AND start_time=? AND end_time = ? AND classroom=?''',
              (date, start_time, end_time, class_code))
    existing_reservation = c.fetchone()

    if existing_reservation and existing_reservation[8] < session['priority']:
        c.execute('''UPDATE reservations_db SET role=?, username=?, public_or_private=?, priority_reserved=?
                    WHERE date=? AND start_time=? AND end_time=? AND classroom=? AND priority_reserved < ?''', (role, session["username"], preference, session['priority'], date, start_time, end_time, class_code, session['priority']))
        conn.commit()
        conn.close()
        return render_template("return_success_message_classroom_reserved.html")
    else:
        if existing_reservation and existing_reservation[2] == date and existing_reservation[3] == start_time and existing_reservation[4] == end_time and existing_reservation[5] == session['username'] and existing_reservation[7] == class_code:
            reservation_already_happened = "Reservation failed: you have already reserved this slot."
            return render_template(role + "_reservation_screen.html", reservation_already_happened=reservation_already_happened, options=classroom_code_options)
        elif existing_reservation:
            another_user_reserved = "Reservation failed: slot already reserved by another user."
            return render_template(role + "_reservation_screen.html", another_user_reserved=another_user_reserved, options=classroom_code_options)
        else:
            c.execute('''INSERT INTO reservations_db (role, date, start_time, end_time, username, public_or_private, classroom, priority_reserved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (role, date, start_time, end_time, session["username"], preference, class_code, session['priority']))
            conn.commit()
            conn.close()
            return render_template("return_success_message_classroom_reserved.html")
        

def seeTheReservations():
    data = RR.getAllReservations()
    return render_template('admin_pages/see_the_reservations.html', reservations=data)


def see_already_reserved_classes():
    rows = RR.getAllReservations()
    return render_template('classroom_inside_reservation.html', rows=rows)

def getReservations(reservationType):
    if reservationType == "myReservations":
        reservations = RR.getReservationsByUsername(session.get("username"))
        return render_template('classroom_inside_reservation.html', rows=reservations)
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
    codes_tuples = RR.reservedClassroomsByInterval(start_date, start_time, duration)
    codes_list = [code[0] for code in codes_tuples] 
    return codes_list


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
    print(reservation_code)
    return render_template("reservation_code.html", reservation_code=reservation_code)

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

