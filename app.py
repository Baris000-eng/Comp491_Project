from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask import session, flash

import setup
from flask_socketio import send
from service.UserService import student_signup, student_login
from repository.UserRepository import initializeItStaffTable, initializeTeachersTable, initializeStudentTable, intializeITReportLog, initializeReservationsTable
from service.UserService import it_staff_login, it_staff_signup, teacher_login, teacher_signup, student_login, student_signup
from service.UserService import password_change_success, go_to_opening_screen
from service.UserService import select_role, showTheClassroomAndInfo, chat_action, report_chat, report_it
from service.UserService import reserve_class
import service.UserService as US
from service.UserService import extract_first_column_of_ku_class_data


app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'


app.route('/get_password_change_screen',
          methods=['GET'])(US.get_password_change_screen)
app.route('/change_student_password',
          methods=['POST'])(US.change_student_password)
app.route('/password_change_success')(password_change_success)

################################################################################################

app.route('/it_staff_login', methods=['GET', 'POST'])(it_staff_login)
app.route('/it_staff_signup', methods=['GET', 'POST'])(it_staff_signup)
app.route('/teacher_login', methods=['GET', 'POST'])(teacher_login)
app.route('/teacher_signup', methods=['GET', 'POST'])(teacher_signup)
app.route('/student_signup', methods=['GET', 'POST'])(student_signup)
app.route('/student_login', methods=['GET', 'POST'])(student_login)

##########################################################################################

app.route('/select_role', methods=['POST'])(select_role)
app.route('/showTheClassroomAndInfo', methods=['GET'])(showTheClassroomAndInfo)
app.route('/chat_action')(chat_action)

app.route('/reportingChat', methods=['POST'])(report_chat)
app.route('/reportingIT', methods=['POST'])(report_it)

app.route('/logout')(go_to_opening_screen)
app.route('/', methods=['GET', 'POST'])(US.opening_screen)

app.route('/teacher_screen')(US.teacher_screen)
app.route('/student_screen')(US.student_screen)
app.route('/it_staff_screen')(US.it_staff_screen)

app.route('/student_dashboard')(US.student_dashboard)
app.route('/teacher_dashboard')(US.teacher_dashboard)
app.route('/it_staff_dashboard')(US.it_staff_dashboard)


app.route('/reserve_class', methods=['POST'])(US.reserve_class)
app.route('/already_reserved_classes',
          methods=['POST'])(US.see_already_reserved_classes)
app.route('/OpenReserveScreen', methods=['POST'])(US.OpenReserveScreen)
###########################################################################################################


app.route('/openStudentReservationScreen',
          methods=['GET'])(US.openStudentReservationScreen)
app.route('/openITReportScreen',
          methods=['GET'])(US.openITReportScreen)
app.route('/openTeacherReservationScreen',
          methods=['GET'])(US.openTeacherReservationScreen)
app.route('/seeITReport',
          methods=['POST'])(US.seeITReport)


# Testing out role-based signup request
@app.route('/<role>/signup', methods=['POST'])
def signup(role):
    return US.user_signup(request, role)

# socket_chat.on("connect")(US.user_connected)
# socket_chat.on("disconnect")(US.user_disconnected)


if __name__ == '__main__':
    setup
    app.run(debug=True)
    app.debug = True
