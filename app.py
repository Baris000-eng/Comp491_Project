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
from service.UserService import student_signup, student_login
from repository.UserRepository import initializeItStaffTable, initializeTeachersTable, initializeStudentTable
from service.UserService import it_staff_login, it_staff_signup, teacher_login, teacher_signup, student_login, student_signup
import bcrypt
from service.UserService import password_change_success, go_to_opening_screen
from service.UserService import select_role, showTheClassroomAndInfo, chat_action, report_chat, report_it
from service.UserService import reserve, reserve_class, getIT
import service.UserService as US


app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'


app.route('/get_password_change_screen',
          methods=['GET'])(US.get_password_change_screen)
app.route('/change_student_password',
          methods=['POST'])(US.change_student_password)
app.route('/password_change_success')(password_change_success)

app.route('/it_staff_login', methods=['GET', 'POST'])(it_staff_login)
app.route('/it_staff_signup', methods=['GET', 'POST'])(it_staff_signup)
app.route('/teacher_login', methods=['GET', 'POST'])(teacher_login)
app.route('/teacher_signup', methods=['GET', 'POST'])(teacher_signup)
app.route('/student_signup', methods=['GET', 'POST'])(student_signup)
app.route('/student_login', methods=['GET', 'POST'])(student_login)
app.route('/select_role', methods=['POST'])(select_role)
app.route('/showTheClassroomAndInfo')(showTheClassroomAndInfo)
app.route('/chat_action')(chat_action)
app.route('/reserve', methods=['POST'])(reserve)
app.route('/reserve_class', methods=['POST'])(reserve_class)
app.route('/reportingChat', methods=['POST'])(report_chat)
app.route('/reportingIT', methods=['POST'])(report_it)
app.route('/getIT', methods=['POST'])(getIT)
app.route('/logout')(go_to_opening_screen)
app.route('/', methods=['GET', 'POST'])(US.opening_screen)

app.route('/teacher_screen')(US.teacher_screen)
app.route('/student_screen')(US.student_screen)
app.route('/it_staff_screen')(US.it_staff_screen)

app.route('/student_dashboard')(US.student_dashboard)
app.route('/teacher_dashboard')(US.teacher_dashboard)
app.route('/it_staff_dashboard')(US.it_staff_dashboard)
app.route('/StudentReservesAClass', methods=['POST'])(US.StudentReservesAClass)
app.route('/student_reserving_class',
          methods=['POST'])(US.student_reserving_class)

app.route('/openReserveClass',
          methods=['POST'])(US.openReserveClass)
app.route('/openITReportScreen',
          methods=['POST'])(US.openITReportScreen)


# socket_chat.on("connect")(US.user_connected)
# socket_chat.on("disconnect")(US.user_disconnected)


if __name__ == '__main__':
    initializeStudentTable()
    initializeItStaffTable()
    initializeTeachersTable()
    app.run(debug=True)
    app.debug = True
