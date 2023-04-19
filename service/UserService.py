from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
from constants import ROLES
import pandas as pd
import repository.UserRepository as UR
import deprecation


DEBUG = True
app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'
app.debug = True


def includes_ignore_case(s1: str, s2: str) -> bool:
    return (s1.lower() in s2.lower())


def check_includes(credentials: List[str]):
    for i, cred1 in enumerate(credentials):
        for j, cred2 in enumerate(credentials):
            if i != j and includes_ignore_case(cred1, cred2):
                return True
    return False


def user_signup(request, role: str):
    session["role"] = role
    session["priority"] = ROLES[role].priority

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        is_valid, error_template = validate_credentials(
            username, password, email, role
        )

        if not is_valid:
            return error_template

        UR.createUser(username=username, password=password,
                      email=email, role=role, priority=ROLES[role].priority)

        session["username"] = username
        page_rendered = f'{concat_folder_dir_based_on_role(role)}{role}_dashboard.html'
        # After sign-up is done, before the url would show role/dahsborad, now it shows role/dashboard, potential routing problem
        return render_template(page_rendered)

    page_rendered = str()
    page_rendered += concat_folder_dir_based_on_role(role=role)
    page_rendered += f'{role}_signup.html'

    return render_template(page_rendered)


###############STUDENT #####################################################################################


###########for checking security ###########################
# TO DO: Integrate this in the validate credentials function. also, check credential validity with the validate_credential function.
#####TO DO: Add a parameter of screen in validate_credentials function so that it can be used for all types of users #########
def validate_password(password):
    # Define the minimum password length
    min_length = 8

    if len(password) < min_length:
        return False

    # Check if the password contains at least one lowercase letter, one uppercase letter, one digit, and one special character
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c.isalnum() for c in password)
    if not (has_lower and has_upper and has_digit and has_special):
        return False

    # If the password passes all the checks, return True
    return True

###########for checking security ############################


def validate_role(role: str):
    """
    Return True if given role is a valid role, false otherwise.
    In other words, check if role exists in ROLES dictionary.
    """
    return role in ROLES


def user_login(request, role: str):
    session['role'] = role
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        page_to_be_displayed = str()

        existing_user = UR.getUserByUsernameAndEmail(username, email, role)

        if not existing_user:
            notExistMessage = "Username & Email pair does not exist."
            folder_directory = concat_folder_dir_based_on_role(role=role)
            page_to_be_displayed += folder_directory
            page_to_be_displayed += f'{role}_login.html'
            return render_template(page_to_be_displayed, notExistMessage=notExistMessage)

        password_check = UR.check_password(existing_user, password)

        if password_check:
            # Redirect to dashboard if student already exists
            session["username"] = username
            session["priority"] = ROLES[role].priority
            session["role"] = role
            page_to_be_shown = str()
            page_to_be_shown += concat_folder_dir_based_on_role(role=role)
            page_to_be_shown += f'{role}_dashboard.html'
            return render_template(page_to_be_shown)

        else:
            # Render template with message and button to go to signup screen
            screen_name = beautify_role_names(role_str=role)
            message = f"You haven't signed up yet. Please go to {screen_name} signup screen by clicking below button."
            button_text = f"Go To {screen_name} Signup Screen"
            page_to_be_rendered = str()
            page_to_be_rendered += concat_folder_dir_based_on_role(role=role)
            page_to_be_rendered += f'{role}_login.html'
            button_url = f"/{role}_signup"
            return render_template(page_to_be_rendered, message=message, button_text=button_text, button_url=button_url, username=username)

    rendered_page = str()
    rendered_page += concat_folder_dir_based_on_role(role=role)
    rendered_page += f'{role}_login.html'
    return render_template(rendered_page)


def get_password_change_screen():
    return render_template('password_change_screen.html')


def change_user_password():
    if request.method == 'POST':
        # Get the email, new password, and confirm password from the request body
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # FIXME
        session['role'] = 'student'

        if not UR.userExistsByEmail(email):
            email_not_found_error = "No account exists with this email."
            return render_template('password_change_screen.html', email_not_found_error=email_not_found_error)

        if not validate_password(new_password) or new_password != confirm_password:
            invalid_password_error = "Make sure new password and confirm password match and are valid."
            return render_template('password_change_screen.html', invalid_password_error=invalid_password_error)

        UR.change_user_password(email, new_password)

        # Redirect to the password_change_success screen
        return redirect(url_for('password_change_success'))

    # Render the password change form
    email = session.get('email', '')
    return render_template(f'password_change_screen.html', email=email)


def password_change_success():
    return render_template('password_change_success.html')
###############STUDENT #####################################################################################


def go_to_opening_screen():
    return render_template('opening_screen.html')


def remove_underscore_and_capitalize(input: str) -> str:
    #####For beautifying the name of screens on buttons , this function is especially for it_staff#####
    words = input.split("_")
    capitalized_words = [word.capitalize() for word in words]
    return " ".join(capitalized_words)


def capitalize(input_string: str) -> str:
    output = input_string.capitalize()
    return output


def concat_folder_dir_based_on_role(role: str):
    #### Gets user role as parameter ####
    #### concatenates the folder directory within templates folder ####
    #### returns the folder directory. ####
    page_rendered = f'{role}_pages/'
    return page_rendered


def beautify_role_names(role_str: str) -> str:
    # screen_name = str()
    # if role_str == "it_staff":
    #     screen_name = remove_underscore_and_capitalize(role_str)
    # elif role_str == "student" or role_str == "teacher":
    #     screen_name = capitalize(role_str)
    # return screen_name
    return ROLES[role_str].name


def validate_credentials(username, password, email, role):
    """
    Checks if current credentials are valid based on:
    1. KU Domain requirement
    2. Email uniqueness
    3. Username uniqueness
    :param username: Username of the user
    :param password: Password of the user
    :param email: Email of the user
    :param role: Role of the user (student/teacher/it_staff)
    """

    page_rendered = str()
    folder_directory = concat_folder_dir_based_on_role(role=role)
    page_rendered += (folder_directory + f'{role}_signup.html')

    is_valid = True

    # TODO: validate_role might be a temporary solution. May be good to add an invalid_role error to opening.screen.html
    if not validate_role(role):
        is_valid = False
        invalid_role = "This role does not exist. Something went wrong"
        return is_valid, render_template('opening_screen.html')
    if not is_ku_email(email):
        is_valid = False
        not_ku_error = "This email address is not from the KU Domain."
        return is_valid, render_template(page_rendered, not_ku_error=not_ku_error)
    elif UR.userExistsByUsernameAndEmail(username, email, role):
        is_valid = False
        screen_name = beautify_role_names(role_str=role)
        signup_error_message = "This account already exists. Please go to " + \
            str(screen_name)+" login screen by pressing below button."
        return is_valid, render_template(page_rendered, signup_error_message=signup_error_message)
    elif UR.userExistsByEmail(email):
        is_valid = False
        email_taken_error = "An account with this email already exists. Choose different email or try logging in by pressing below button."
        return is_valid, render_template(page_rendered, email_taken_error=email_taken_error)
    elif UR.userExistsByUsername(username):
        is_valid = False
        username_taken_error = "This username is already taken. Choose different username or try logging in by pressing below button."
        return is_valid, render_template(page_rendered, username_taken_error=username_taken_error)
    elif check_includes([username, password]) or check_includes([email, password]):
        is_valid = False
        credentials_coincide_error = "Make sure that your credentials do not contain each other"
        return is_valid, render_template(page_rendered, credentials_coincide_error=credentials_coincide_error)
    elif not validate_password(password):
        is_valid = False
        invalid_password_error = "Password must be at least 8 characters and must include at least:\n \
        1 lower case character\n\
        1 upper case character\n\
        1 digit\n\
        1 special character"
        return is_valid, render_template(page_rendered, invalid_password_error=invalid_password_error)

    return is_valid, ""


def is_ku_email(email: str):
    """
    Given an string, checks if it belongs to KU Domain (case insensitive)
    """
    suffix_ku = '@ku.edu.tr'
    is_ku_email = email.lower().endswith(suffix_ku)
    return is_ku_email


def openITReportScreen():
    return render_template('report_to_IT.html')


#########OTHER SCREENS #######################################################
def select_role():
    role = request.form.get('roles')
    if role in ROLES:
        return redirect(f'/{role}/screen')
    else:
        return render_template('opening_screen.html')


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
            with open("templates/Classroom_reservation_students_view.html", "w", encoding="utf-8") as file:
                file.write(txt_string)
                file.write(txt_string)
                file.close()
        beginning = '<!DOCTYPE html><html><head><title>Student Dashboard</title><link rel="stylesheet" type="text/css" href="../static/classroom_infos.css"><script> window.addEventListener("DOMContentLoaded", function() { var reserveButtons=document.querySelectorAll("button[action=\'/OpenReserveScreen\']"); reserveButtons.forEach(function(button) { button.addEventListener("click", function() {  var parentRow=button.parentElement.parentElement; parentRow.classList.add(\'reserved\'); });       });     }); </script></head><body>'

        html = ""
        html += beginning
        html += "<table>\n<thead>\n<tr>\n"
        html += "".join([f"<th>{header}</th>\n" for header in heads])
        html += "</tr>\n</thead>\n<tbody>\n"
        html += "".join([f"<tr>{''.join([f'<td>{cell}</td>' for cell in row])}<td><form action='/openStudentReservationScreen' method='GET'><button >Reserve</button></form></td></tr>\n" for row in info])
        html += "</tbody>\n</table>"
        html += "</body></html>"
        create_html_file(html)
        return html
    html = load_classes_with_info('KU_Classrooms.xlsx')
    return render_template("Classroom_reservation_students_view.html")


def extract_first_column_of_ku_class_data():
    df = pd.read_excel('KU_Classrooms.xlsx')
    options = [x for x in df.iloc[:, 0].dropna().tolist() if x not in [
        'CASE', 'SOS', 'SNA', 'ENG', 'SCI']]
    return options
############################################################################################################################################################################################################


def reserve_class():
    role = session["role"]
    class_code = request.form['class-code']
    time = request.form['time']
    date = request.form['date']
    option = request.form['option']

    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    preference = str()
    if option == "exam":
        preference = "Exam"
    elif option == "lecture":
        preference = "Lecture"
    elif option == "ps":
        preference = "PS"
    elif option == "private":
        preference = "Private"
    elif option == "public":
        preference = "Public"

    # Retrieve existing reservation
    c.execute('''SELECT * FROM reservations_db WHERE date=? AND time=? AND classroom=?''',
              (date, time, class_code))
    existing_reservation = c.fetchone()

    if existing_reservation and existing_reservation[6] < session['priority']:
        c.execute('''UPDATE reservations_db SET role=?, username=?, public_or_private=?, priority_reserved=? 
                    WHERE date=? AND time=? AND classroom=? AND priority_reserved < ?''', (role, session["username"], preference, session['priority'], date, time, class_code, session['priority']))
        conn.commit()
        conn.close()
        return render_template("return_success_message_classroom_reserved.html")
    else:
        if existing_reservation and existing_reservation[1] == date and existing_reservation[2] == time and existing_reservation[3] == class_code and existing_reservation[4] == session['username']:
            reservation_already_happened = "Reservation failed: you have already reserved this slot."
            return render_template(role + "_reservation_screen.html", reservation_already_happened=reservation_already_happened)
        elif existing_reservation:
            another_user_reserved = "Reservation failed: slot already reserved by another user."
            return render_template(role + "_reservation_screen.html", another_user_reserved=another_user_reserved)
        else:
            # Insert new reservation #
            c.execute('''INSERT INTO reservations_db (role, date, time, username, public_or_private, classroom, priority_reserved) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (role, date, time, session["username"], preference, class_code, session['priority']))
            conn.commit()
            conn.close()
            return render_template("return_success_message_classroom_reserved.html")


def report_it():
    room_number = request.form['room_number']
    faculty_name = request.form['faculty_name']
    problem_description = request.form['problem_description']
    date = request.form['date']
    time = request.form['time']
    UR.createITReport(
        room_number,
        faculty_name,
        problem_description,
        date,
        time
    )
    return render_template("it_staff_pages/IT_report_success_screen.html")


def seeITReport():
    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM IT_Report_logdb')
    rows = c.fetchall()
    return render_template('it_staff_pages/IT_Report_list.html', rows=rows)


def report_chat():
    problem_description = request.form['problem_description']
    with open('IT_Chat_Problems.txt', 'a') as f:
        f.write(f'Problem Description: {problem_description}\n\n')
    return 'Thank you for reporting the problem to IT!'


def chat_action():
    class_no = request.args.get("classroom")
    session['classroom'] = class_no
    return render_template("chat_pages/chat_room.html", class_no=class_no)


def user_connected(info):
    with open('chat_data.txt', 'a') as f:
        f.write(session['username'] + " entered the chat to room " +
                session['classroom'] + " \n")
    print(session['username'] +
          " joined the chat (room : " + session['classroom'] + ")")


def user_disconnected():
    with open('chat_data.txt', 'a') as f:
        f.write(session['username'] + " exited the chat to room " +
                session['classroom'] + " \n")
    print(session['username'] +
          " left the chat room (room : " + session['classroom'] + ")")


def see_already_reserved_classes():
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reservations_db')
    rows = c.fetchall()
    return render_template('classroom_inside_reservation.html', rows=rows)
#########################################################################################################################################################################


def openStudentReservationScreen():
    options = extract_first_column_of_ku_class_data()
    return render_template('student_reservation_screen.html', options=options)


def openTeacherReservationScreen():
    options = extract_first_column_of_ku_class_data()
    return render_template("teacher_reservation_screen.html", options=options)


def opening_screen():
    return render_template("opening_screen.html")


def user_screen(role: str):
    return render_template(f'{role}_pages/{role}_screen.html')


def user_dashboard(role: str):
    return render_template(f'{role}_pages/{role}_dashboard.html')


def go_to_opening_screen():
    return render_template('opening_screen.html')


def OpenReserveScreen():
    return render_template("student_reservation_screen.html")


def seeTheUsers():
    # Connect to the database
    print("hi")
    conn = sqlite3.connect('users_db.db')
    c = conn.cursor()

    # Retrieve the usernames from the database
    c.execute('SELECT username FROM users_db')

    usernames = [row[0] for row in c.fetchall()]

    # Close the database connection
    conn.close()

    # Render the HTML template with the usernames

    return render_template('admin_see_users.html', usernames=usernames)


def seeTheReservations():
    # Connect to the database
    # Connect to the database
    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    # Retrieve all the rows from the reservations_db table
    c.execute('SELECT * FROM reservations_db')
    data = c.fetchall()

    # Close the database connection
    conn.close()
    print(data)

    # Render the HTML template with the rows
    return render_template('see_the_reservations.html', reservations=data)


def editUser(username):
    return render_template('edit_users.html', username=username)


def editReserved():
    row = request.args.get('row_data').split(',')
    return render_template("editYourReservations.html", row=row)


def editITReport():
    row = request.args.get('row_data').split(',')
    return render_template("editITReport.html", row=row)


def deleteReservation():

    role = request.form['role']
    date = request.form['date']
    time = request.form['time']
    username = request.form['username']
    public_or_private = request.form['public_or_private']
    classroom = request.form['classroom']
    priority_reserved = request.form['priority_reserved']

    conn = sqlite3.connect('reservations_db.db')
    c = conn.cursor()

    c.execute('''DELETE FROM reservations_db WHERE
                 role = ? AND
                 date = ? AND
                 time = ? AND
                 username = ? AND
                 public_or_private = ? AND
                 classroom = ? AND
                 priority_reserved = ?''',
              (role, date, time, username, public_or_private, classroom, priority_reserved))

    conn.commit()
    conn.close()
    print("1hi")
    return render_template("successsDeletedClass.html")


def deleteITReport():
    report_no = request.form['report_no']
    room_name = request.form['room_name']
    faculty_name = request.form['faculty_name']
    problem_description = request.form['problem_description']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect('IT_Report_logdb.db')
    c = conn.cursor()
    c.execute('''DELETE FROM IT_Report_logdb WHERE
                 it_report_no = ? AND
                 room_name = ? AND
                 faculty_name = ? AND
                 problem_description = ? AND
                 date = ? AND
                 time = ?''',
              (report_no, room_name, faculty_name, problem_description, date, time))
    conn.commit()
    conn.close()
    return render_template("successDeletedITReport.html")
