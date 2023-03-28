import glob
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask import session, flash
from flask import session
from flask_socketio import SocketIO
import socketio
from flask_socketio import send
from service.UserService import student_signup, student_login, password_change, password_change_screen, student_password_change, password_change_success

import bcrypt

import service.UserService as US

DEBUG = True


app = Flask(__name__)
# push testf

app.secret_key = '491'

app.config['SECRET_KEY'] = '491'

socket_chat = SocketIO(app)


@app.route('/signup_success')
def signup_success():
    return "Signup successful!"


@app.route('/', methods=['GET', 'POST'])
def opening_screen():
    return render_template("opening_screen.html")


@app.route('/')
def index():
    return render_template('student_dashboard.html')


@app.route('/role_selection', methods=['POST'])
def role_selection():
    role = request.form.get('roles')
    if role == 'teacher':
        return redirect(url_for('teacher_screen'))
    elif role == 'student':
        return redirect(url_for('student_screen'))
    elif role == 'it_staff':
        return redirect(url_for('it_staff_screen'))
    else:
        # Invalid role selected, render the opening screen again
        return render_template('opening_screen.html')


@app.route('/teacher_screen')
def teacher_screen():
    return render_template('teacher_screen.html')


@app.route('/student_screen')
def student_screen():
    return render_template('student_screen.html')


@app.route('/it_staff_screen')
def it_staff_screen():
    return render_template('it_staff_screen.html')


@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')


app.route('/student_signup', methods=['GET', 'POST'])(student_signup)
app.route('/student_login', methods=['GET', 'POST'])(student_login)

# Routes for password change functionality
app.route('/password_change_screen', methods=['GET'])(password_change_screen)
app.route('/student_password_change',
          methods=['GET', 'POST'])(student_password_change)
app.route('/password_change_success')(password_change_success)
app.route('/password_change', methods=['POST'])(password_change)


@app.route('/it_staff_signup', methods=['GET', 'POST'])
def it_staff_signup():
    if request.method == 'POST':
        # Handle form submission here
        # burdda it_staff dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
        return redirect('/it_staff_screen')
    else:
        return render_template('it_staff_signup.html')


@app.route('/it_staff_login', methods=['GET', 'POST'])
def it_staff_login():
    if request.method == 'POST':
        # Handle form submission here
        # burdda it_staff dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
        return redirect('/it_staff_screen')
    else:
        return render_template('it_staff_login.html')


@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        # Handle form submission here
        # burdda teacher dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
        return redirect('/teacher_screen')
    else:
        return render_template('teacher_signup.html')


@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        # Handle form submission here
        # burdda teacher dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
        return redirect('/teacher_screen')
    else:
        return render_template('teacher_login.html')


@app.route('/reserve', methods=['POST'])
def reserve():
    class_code = request.form['class-code']
    time = request.form['time']
    date = request.form['date']
    option = request.form['option']

    with open('class_reservations.txt', 'a') as f:
        f.write(f'Class Code: {class_code}\n')
        f.write(f'Time: {time}\n')
        f.write(f'Date: {date}\n')
        f.write(f'Option: {option}\n\n')

    return 'Reservation submitted successfully!'


@app.route('/reportingIT', methods=['POST'])
def report_it():
    room_number = request.form['room_number']
    faculty_name = request.form['faculty_name']
    problem_description = request.form['problem_description']
    date = request.form['date']
    time = request.form['time']

    # Write the form data to the file
    with open('IT_Problems.txt', 'a') as f:
        f.write(f'Room Number: {room_number}\n')
        f.write(f'Faculty Name: {faculty_name}\n')
        f.write(f'Problem Description: {problem_description}\n')
        f.write(f'Date: {date}\n')
        f.write(f'Time: {time}\n\n')

    # Return a response to the user
    return 'Thank you for reporting the problem to IT!'


@app.route('/reportingChat', methods=['POST'])
def report_chat():

    problem_description = request.form['problem_description']

    # Write the form data to the file
    with open('IT_Problems.txt', 'a') as f:
        #f.write(f'chatUser: {chatUser}\n')
        f.write(f'Problem Description: {problem_description}\n\n')

    # Return a response to the user
    return 'Thank you for reporting the problem to IT!'


@app.route('/reservingClass', methods=['POST'])
def reserve_class():
    class_num = request.form['class_num']
    class_code = request.form['class-code']
    date_input = request.form['date_input']
    option = request.form['option']
    time = request.form['time']

    # Write the form data to the file
    with open('reserved_classes.txt', 'a') as f:
        f.write(f'Class Number: {class_num}\n')
        f.write(f'Class Code: {class_code}\n')
        f.write(f'Option: {option}\n')
        f.write(f'Date: {date_input}\n')
        f.write(f'Time: {time}\n\n')

    # Return a response to the user
    return 'Reservation submitted successfully'


@app.route('/getIT', methods=['POST'])
def getIT():
    with open("classes_teacher.txt", "r") as f:
        content = f.read()
        content = content.replace('\n', '<br>')

    # Return a response to the user
    return render_template("student_dashboard.html", content=content)


@app.route('/chat_action')
def chat_action():

    class_no = request.args.get("classroom")
    session['classroom'] = class_no
    return render_template("chat_room.html", class_no=class_no)


@socket_chat.on("connect")
def user_connected(info):
    # send
    with open('chat_data.txt', 'a') as f:
        f.write(session['username'] + " entered the chat to room " +
                session['classroom'] + " \n")
    print(session['username'] +
          " joined the chat (room : " + session['classroom'] + ")")


@socket_chat.on("disconnect")
def user_disconnected():
    with open('chat_data.txt', 'a') as f:
        f.write(session['username'] + " exited the chat to room " +
                session['classroom'] + " \n")
    print(session['username'] +
          " left the chat room (room : " + session['classroom'] + ")")
    # send()


@app.route('/showTheClassroomAndInfo')
def showTheClassroomAndInfo():
    import openpyxl

    def load_classes_with_info(filename):
        # Load workbook
        workBook = openpyxl.load_workbook(filename)

        # Select active worksheet
        workBookActive = workBook.active

        # Get column headers
        columns = workBookActive[1][:8]
        heads = [collumn.value for collumn in columns]

        # Get data from columns A to H
        rows = workBookActive.iter_rows(min_row=2)
        info = []
        for row in rows:
            row_values = []
            for column in row[:8]:
                row_values.append(column.value)
            info.append(row_values)

        def create_html_file(txt_string):
            file = open("templates/classrooms_and_info.html", "w")
            file.write(txt_string)
            file.close()
        beginning = '<!DOCTYPE html> <html> <head> <title>Student Dashboard</title> <link rel="stylesheet" type="text/css" href="../static/styles.css"> </head><body>'
        html = ""
        html += beginning
        html += '! <form action="/getBackFromClassroomInfo" style="padding-top: 20px; padding-bottom: 20px;> <input type="submit" value="Go Back"> </form>'
        html += "<table>\n<thead>\n<tr>\n"
        html += "".join([f"<th>{header}</th>\n" for header in heads])
        html += "</tr>\n</thead>\n<tbody>\n"
        html += "".join([f"<tr>{''.join([f'<td>{cell}</td>' for cell in row])}<td><button>Reserve</button></td></tr>\n" for row in info])

        html += "</tbody>\n</table>"
        html += '! <form action="/getBackFromClassroomInfo" > <input type="submit" value="Go Back"> </form>'
        html += "</body></html>"
        create_html_file(html)
        return html
    html = load_classes_with_info('KU_Classrooms.xlsx')
    return render_template("classrooms_and_info.html")


@app.route('/getBackFromClassroomInfo')
def getBackFromClassroomInfo():
    return render_template("student_dashboard.html")


@app.route('/StudentReservesAClass')
def StudentReservesAClass():
    


if __name__ == '__main__':
    app.run(debug=True)
    socket_chat.run(app, debug=True)
