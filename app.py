from flask import Flask, request, session

import setup
from rbac import allow_roles
from service.UserService import password_change_success, go_to_opening_screen
from service.UserService import select_role, showTheClassroomAndInfo, chat_action, report_chat, report_it
import service.UserService as US
import service.ClassroomService as CS
import service.PlottingService as PS
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'
socketio = SocketIO(app)

app.route("/reservation_code")(US.generate_classroom_reservation_code)

app.route('/class_schedules')(US.course_schedules)
app.route('/exam_schedules')(US.exam_schedules)
app.route('/myExamsOnly')(US.myExamsOnly)
app.route('/allExams')(US.allExams)
app.route('/myClassesOnly')(US.myClassesOnly)
app.route('/allClasses')(US.allClasses)
app.route("/get_news_count")(US.get_news_count)
app.route("/open_news")(US.open_news_screen)
app.route("/get_teacher_signup_guide")(US.get_teacher_signup_guide)
app.route("/get_admin_signup_guide")(US.get_admin_signup_guide)
app.route("/get_student_signup_help")(US.get_student_signup_help)
app.route("/get_student_login_help")(US.get_student_login_help)
app.route("/get_teacher_signup_help")(US.get_teacher_signup_help)
app.route("/get_teacher_login_help")(US.get_teacher_login_help)
app.route("/get_it_staff_signup_help")(US.get_it_staff_signup_help)
app.route("/get_it_staff_login_help")(US.get_it_staff_login_help)
app.route("/open_description_text")(US.get_description_text)
app.route("/get_opening_help")(US.get_opening_help)
app.route("/goToOpeningScreen")(US.goToOpeningScreen)


app.route('/get_password_change_screen',
          methods=['GET'])(US.get_password_change_screen)
app.route('/change_user_password',
          methods=['GET', 'POST'])(US.change_user_password)
app.route('/password_change_success')(password_change_success)

app.route('/select_role', methods=['POST'])(select_role)
app.route('/showTheClassroomAndInfo', methods=['GET'])(showTheClassroomAndInfo)
app.route('/chat_action')(chat_action)
# @socketio.on('connect')
# @socketio.on('message')

app.route('/reportingChat', methods=['POST'])(report_chat)
app.route('/reportingIT', methods=['POST'])(report_it)

app.route('/logout')(go_to_opening_screen)
app.route('/', methods=['GET', 'POST'])(US.opening_screen)
app.route('/editReserved', methods=['GET'])(US.editReserved)
app.route('/editITReport', methods=['GET'])(US.editITReport)
app.route('/deleteReservation', methods=['POST'])(US.deleteReservation)
app.route('/deleteITReport', methods=['POST'])(US.deleteITReport)
app.route('/seeOnlyMyReserves', methods=['GET'])(US.seeOnlyMyReserves)
app.route('/createNews', methods=['GET'])(US.createNews)


@app.route('/<role>/screen', methods=['GET'])
def screen(role):
    return US.user_screen(role)


@app.route('/admin/import-classrooms', methods=['POST'])
@allow_roles([], session, request)
def import_classrooms():
    file_path = request.form.get('file_path', '')
    return CS.createClassrooms(file_path)


@app.route('/classrooms', methods=['GET'])
@allow_roles([], session, request)
def get_all_classrooms():
    return CS.getAllClassrooms()


@app.route('/classrooms/filter', methods=['GET'])
@allow_roles(['student', 'teacher', 'it_staff'], session, request)
def get_classrooms_where():
    return CS.getClassroomsWhere(request.form)


@app.route('/<role>/dashboard', methods=['GET', 'POST'])
@allow_roles(['student', 'teacher', 'it_staff'], session, request)
def dashboard(role):
    return US.user_dashboard(role)


app.route('/reserve_class', methods=['POST'])(US.reserve_class)
app.route('/already_reserved_classes',
          methods=['POST'])(US.see_already_reserved_classes)
app.route('/OpenReserveScreen', methods=['POST'])(US.OpenReserveScreen)
###########################################################################################################

app.route('/enterChat',
          methods=['GET'])(US.enterChat)


app.route('/openITReportScreen',
          methods=['GET'])(US.openITReportScreen)


app.route('/openStudentReservationScreen',
          methods=['GET'])(US.openStudentReservationScreen)
app.route('/openTeacherReservationScreen',
          methods=['GET'])(US.openTeacherReservationScreen)
app.route('/openItStaffReservationScreen',
          methods=['GET'])(US.open_it_staff_reservation_screen)


app.route('/seeITReport',
          methods=['POST'])(US.seeITReport)
app.route('/seeTheUsers',
          methods=['GET'])(US.seeTheUsers)


@app.route('/editUser', methods=['GET'])
def editUser():
    username = request.args.get('username')
    return US.editUser(username=username)


app.route('/seeTheReservations',
          methods=['GET'])(US.seeTheReservations)


app.route('/seeITReports',
          methods=['GET'])(US.seeITReports)


app.route('/AdminUserStats', methods=['GET'])(US.seeUserStats)

app.route('/AdminReservationStats', methods=['GET'])(US.seeReserveStats)
app.route('/createNewsElement', methods=['GET', "POST"])(US.createNewsElement)
app.route('/AdminITStats', methods=['GET'])(US.AdminITStats)
###########################################################################################################
# For Admin
###########################################################################################################
# Testing out role-based signup request


@socketio.on('message')
def handle_message(message):
    import clientSide as cs
    isLegitToSend = cs.isLegitToSend(message)
    if isLegitToSend:
        emit('response', message)
    else:
        # report IT
        return


@app.route('/<role>/signup', methods=['GET', 'POST'])
def signup(role):
    return US.user_signup(request, role)


@app.route('/<role>/login', methods=['GET', 'POST'])
def login(role):
    return US.user_login(request, role)


# socket_chat.on("connect")(US.user_connected)
# socket_chat.on("disconnect")(US.user_disconnected)
app.route('/send_chat_message_student')(US.send_chat_message_student)


app.route('/see_plot_of_reservation_num_per_role')(PS.plot_reservations_per_role)
app.route('/see_plot_of_reservation_num_per_class')(PS.plot_reservations_per_class)
app.route('/see_plot_of_reservation_num_per_purpose')(PS.plot_reservations_per_purpose)
app.route("/seeReservationStatistics")(US.get_reservation_statistics_screen)


if __name__ == '__main__':

    setup
    app.run(debug=True, port=499)
    app.debug = True
