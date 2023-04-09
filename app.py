from flask import Flask, request

import setup
from service.UserService import password_change_success, go_to_opening_screen
from service.UserService import select_role, showTheClassroomAndInfo, chat_action, report_chat, report_it
import service.UserService as US


app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'


app.route('/get_password_change_screen',
          methods=['GET'])(US.get_password_change_screen)
app.route('/change_user_password',
          methods=['GET', 'POST'])(US.change_user_password)
app.route('/password_change_success')(password_change_success)

app.route('/select_role', methods=['POST'])(select_role)
app.route('/showTheClassroomAndInfo', methods=['GET'])(showTheClassroomAndInfo)
app.route('/chat_action')(chat_action)

app.route('/reportingChat', methods=['POST'])(report_chat)
app.route('/reportingIT', methods=['POST'])(report_it)

app.route('/logout')(go_to_opening_screen)
app.route('/', methods=['GET', 'POST'])(US.opening_screen)

@app.route('/<role>/screen', methods=['GET'])
def screen(role):
    return US.user_screen(role)

@app.route('/<role>/dashboard', methods=['GET'])
def dashboard(role):
    return US.user_dashboard(role)

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
@app.route('/<role>/signup', methods=['GET', 'POST'])
def signup(role):
    return US.user_signup(request, role)

@app.route('/<role>/login', methods=['GET', 'POST'])
def login(role):
    return US.user_login(request, role)

# socket_chat.on("connect")(US.user_connected)
# socket_chat.on("disconnect")(US.user_disconnected)


if __name__ == '__main__':
    setup
    app.run(debug=True)
    app.debug = True
