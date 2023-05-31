from flask import Flask, request, session
import setup
import socket
from rbac import allow_roles
from service.UserService import password_change_success, go_to_opening_screen
from service.UserService import select_role, chat_action, report_it
import service.UserService as US
import service.ClassroomService as CS
import service.CourseService as COS
import service.PiechartPlottingService as PPS
import service.HistogramPlottingService as HPS
import service.ReservationService as RS
from flask_socketio import SocketIO, emit
from flask import render_template
import service.MailSendingService as MSS

app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'
socketio = SocketIO(app)
DEBUG = True

app.route("/get_news_attendance")(US.get_news_attendance)
app.route("/already_attended_event")(US.already_attended_event)

app.route("/news_attendance")(US.news_attendance)
app.route("/drop")(US.drop)

app.route("/viewInsidesOfClassrooms")(US.getClassroomView)
app.route('/viewFloors')(US.viewFloors)
app.route(
    "/getFilterAndSearchClassroomsScreen")(CS.showClassroomSearchAndFilterScreen)

app.route("/openMap")(US.openMap)

app.route(
    "/get_reservation_code_viewing_screen")(RS.view_reservation_code_viewing_screen)

app.route('/class_schedules')(COS.course_schedules)
app.route('/exam_schedules')(US.exam_schedules)
app.route('/allExams')(US.allExams)


@app.route('/courses', methods=['GET'])
def getCoursesWithPagination():
    if DEBUG:
        print(f"request.args: {request.args}")
    pageNumber = request.args.get('pageNumber')
    return COS.getCoursesWithPagination(pageNumber)


app.route("/getAnnouncementScreen")(US.getAnnouncementScreen)
app.route("/successMessageAttendance")(US.success_message_attendance)

app.route("/open_news")(US.open_news_screen)
app.route("/redirect_student_dashboard")(US.redirect_student_dashboard_from_news)
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
app.route("/openFeatures")(US.openFeatures)

# classrooms
app.route("/openSCI")(US.openSCI)
app.route("/openSNAA")(US.openSNAA)
app.route("/openSNAB")(US.openSNAB)
app.route("/openENG")(US.openENG)
app.route("/openLIB")(US.openLIB)
app.route("/openELC")(US.openELC)
app.route("/openSOS")(US.openSOS)
app.route("/openCASE")(US.openCASE)
app.route("/openSTD")(US.openSTD)


app.route('/get_password_change_screen',
          methods=['GET'])(US.get_password_change_screen)
app.route('/change_user_password',
          methods=['GET', 'POST'])(US.change_user_password)
app.route('/password_change_success')(password_change_success)

app.route('/select_role', methods=['POST'])(select_role)
app.route('/chat_action')(chat_action)
app.route('/reportingIT', methods=['POST'])(report_it)

app.route("/makeAnnouncement", methods=['GET', 'POST'])(US.makeAnnouncement)

app.route('/logout')(go_to_opening_screen)
app.route('/', methods=['GET', 'POST'])(US.opening_screen)
app.route('/editReservedClassroom',
          methods=['GET'])(RS.editClassroomReservations)
app.route('/editITReport', methods=['GET'])(US.editITReport)
app.route('/deleteReservation', methods=['POST'])(RS.deleteReservation)
app.route('/deleteITReport', methods=['POST'])(US.deleteITReport)


@app.route('/reservations', methods=['GET'])
def getReservations():
    reservationType = request.args.get('reservationType')
    return RS.getReservations(reservationType)


app.route('/getCreateNewsScreen', methods=['GET'])(US.createNews)
app.route('/updateITReport', methods=['POST', 'GET'])(US.updateITReport)
app.route('/open_it_report_success',
          methods=['GET'])(US.open_it_report_success)
app.route('/updateReservation', methods=['POST', 'GET'])(RS.updateReservation)


@app.route('/<role>/screen', methods=['GET'])
def screen(role):
    return US.user_screen(role)


@app.route('/admin/import-classrooms', methods=['POST'])
@allow_roles(['student', 'teacher', 'it_staff'], session, request)
def import_classrooms():
    file_path = request.form.get('file_path', '')
    return CS.createClassrooms(file_path)


@app.route('/classrooms', methods=["GET"])
@allow_roles(['student', 'teacher', 'it_staff'], session, request)
def get_all_classrooms():
    classrooms = CS.getAllClassrooms()
    return render_template("classroom_reservation_view.html", classrooms=classrooms)


@app.route('/filteredClassrooms', methods=['GET'])
def get_classrooms_where():
    classrooms = CS.getClassroomsWhere(request.args)
    departments = CS.getAllDepartments()
    return render_template("classroom_reservation_view.html", classrooms=classrooms, departments=departments)


@app.route('/<role>/dashboard', methods=['GET', 'POST'])
@allow_roles(['student', 'teacher', 'it_staff'], session, request)
def dashboard(role):
    return US.user_dashboard(role)


app.route('/reserve_class', methods=['POST'])(RS.reserve_class)


@app.route('/joinOrLeaveReservation', methods=['POST'])
def joinOrLeaveReservation():
    if "joinOrLeave" not in request.form:
        return getReservations()

    joinType = request.form.get("joinOrLeave")
    reserv_id = request.form.get("row_data").split(",")[0]
    username = session.get("username")

    return RS.joinOrLeaveReservation(joinType, reserv_id, username)


app.route('/already_reserved_classes',
          methods=['POST'])(RS.see_already_reserved_classes)
app.route('/open_reserve_screen', methods=['POST'])(RS.open_reserve_screen)
###########################################################################################################
app.route('/incoming_news')(US.incoming_news)
app.route('/attend_or_not', methods=['GET', 'POST'])(US.attend_or_not)
app.route('/openEventAttendanceScreen',
          methods=['GET', 'POST'])(US.openEventAttendanceScreen)

app.route('/openITReportScreen',
          methods=['GET'])(US.openITReportScreen)


app.route('/openStudentReservationScreen',
          methods=['GET'])(RS.openStudentReservationScreen)
app.route('/openTeacherReservationScreen',
          methods=['GET'])(RS.openTeacherReservationScreen)
app.route('/openITStaffReservationScreen',
          methods=['GET'])(RS.openITStaffReservationScreen)


@app.route('/reservedClassroomsByInterval', methods=['GET'])
def reservedClassroomsByInterval():
    start_date = request.args.get('start_date')
    start_time = request.args.get('start_time')
    duration = request.args.get('duration')
    return RS.reservedClassroomsByInterval(start_date, start_time, duration)


app.route('/seeITReport',
          methods=['POST'])(US.seeITReport)
app.route('/seeTheUsers',
          methods=['GET'])(US.seeTheUsers)


@app.route('/getUserEditingScreenForAdmin', methods=['GET'])
def getUserEditingScreenForAdmin():
    return US.getUserEditingScreenForAdmin()


app.route('/seeTheReservations',
          methods=['GET'])(RS.seeTheReservations)

app.route('/viewFloors')(US.viewFloors)

app.route('/seeITReports',
          methods=['GET'])(US.seeITReports)


app.route('/createNewsElement', methods=["GET", "POST"])(US.createNewsElement)
app.route('/get_it_statistics_for_admin',
          methods=['GET'])(US.it_report_statistics_for_admin)
###########################################################################################################
# For Admin
###########################################################################################################
# Testing out role-based signup request


@app.route('/<role>/signup', methods=['GET', 'POST'])
def signup(role):
    return US.user_signup(request, role)


@app.route('/<role>/login', methods=['GET', 'POST'])
def login(role):
    return US.user_login(request, role)


app.route('/send_chat_message', methods=["GET", "POST"])(US.send_chat_message)
app.route('/enterChat', methods=['GET'])(US.enterChat)
app.route('/clearMessages')(US.clearMessages)


app.route("/get_it_report_statistics_for_admin")(US.it_report_statistics_for_admin)
app.route('/see_plot_of_reservation_num_per_role')(HPS.plot_reservations_per_role)
app.route('/see_plot_of_reservation_num_per_class')(HPS.plot_reservations_per_class)
app.route(
    '/see_plot_of_reservation_num_per_purpose')(HPS.plot_reservations_per_purpose)
app.route(
    "/see_plot_of_reservation_num_per_priority")(HPS.plot_reservations_per_priority_value)

app.route(
    '/see_piechart_of_reservation_num_per_role')(PPS.piechart_of_reservations_per_role)
app.route(
    '/see_piechart_of_reservation_num_per_class')(PPS.piechart_of_reservations_per_class)
app.route('/see_piechart_of_reservation_num_per_purpose')(
    PPS.piechart_of_reservations_per_purpose)
app.route("/see_piechart_of_reservation_num_per_priority")(
    PPS.piechart_reservations_per_priority_value)


app.route("/see_plot_of_user_numbers_per_priority_value")(
    HPS.plot_user_numbers_per_priority_value)
app.route("/see_plot_of_user_numbers_per_role")(HPS.plot_user_numbers_per_role)
app.route("/see_piechart_of_user_numbers_per_priority_value")(
    PPS.plot_piechart_of_user_numbers_per_priority_value)
app.route(
    "/see_piechart_of_user_numbers_per_role")(PPS.plot_piechart_of_user_numbers_per_role)

app.route('/see_histogram_of_it_report_num_by_classroom_name')(
    HPS.plot_histogram_of_it_report_numbers_per_classroom_name)
app.route('/see_piechart_of_it_report_num_by_classroom_name')(
    PPS.plot_piechart_of_it_report_numbers_per_classroom_name)


app.route('/see_histogram_of_it_report_num_by_faculty_name')(
    HPS.plot_histogram_of_it_report_numbers_per_faculty_name)
app.route('/see_piechart_of_it_report_num_by_faculty_name')(
    PPS.plot_piechart_of_it_report_numbers_per_faculty_name)

app.route('/see_barchart_of_it_report_num_per_problem_description')(
    HPS.plot_histogram_of_it_report_numbers_per_problem_description)
app.route('/see_piechart_of_it_report_num_per_problem_description')(
    PPS.plot_piechart_of_it_report_numbers_per_problem_description)


app.route("/seeReservationStatistics")(RS.get_reservation_statistics_screen)
app.route("/seeUserStatistics")(US.open_user_statistics_screen)
app.route('/successfulUpdateOfITReport')(US.successfulUpdateOfITReport)
app.route('/successfulUpdateOfReservation')(RS.successfulUpdateOfReservation)


app.route("/deleteUser", methods=["POST"])(US.deleteUser)
app.route("/updateUserInformation", methods=["POST"])(US.updateUserInformation)

app.route("/successfulDeletionOfUser")(US.successfulDeletionOfUser)
app.route("/successfulUpdateOfUserInformation")(US.successfulUpdateOfUserInformation)

app.route("/sendReservationInformationAsEmail",
          methods=["POST"])(MSS.sendReservationInformationAsEmail)


###################### this gets ip address of the device #####################
def get_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    return ip_address
###################### this gets ip address of the device #####################


if __name__ == '__main__':
    setup
    # Setting the host to the IP address of the device #
    host_address = get_ip_address()
    app.run(host=host_address, debug=True, port=5000)
    app.debug = True
