from flask import session
from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import openpyxl
import secrets
import random
import matplotlib.pyplot as plt
import string
import io
import base64
from constants import ROLES
import pandas as pd
import repository.UserRepository as UR
import deprecation
import datetime
import html

DEBUG = True
app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'
app.debug = True


def getClassroomView():
    return render_template("viewSchoolMap.html")


def getClassroomView2():
    return render_template("view_inside_of_classroom.html")


def generate_classroom_reservation_code():
    alphabet = string.ascii_letters + string.digits
    if 'reservation_code' in session:
        reservation_code = session['reservation_code']
    else:
        reservation_code = ''.join(random.choice(alphabet) for i in range(8))
        session['reservation_code'] = reservation_code
    print(reservation_code)
    return render_template("reservation_code.html", reservation_code=reservation_code)


def get_news_count():
    return UR.getNewsCount()


def open_news_screen():
    return render_template("incoming_news.html", news_data=UR.getNews(), newsCount=UR.getNewsCount())


def redirect_Student_dashboard_From_news():
    newsCount = 0
    role = "student"
    return redirect(f'/{role}/dashboard?newsCount={newsCount}')


def exam_schedules():
    df = pd.read_excel('FALL_22_EXAMS.xlsx')

    # Replace missing values with an empty string #
    df.fillna("", inplace=True)

    # Escape special characters #
    df = df.applymap(lambda x: html.escape(str(x))
                     if isinstance(x, str) else x)

    html_table = df.to_html(index=False, header=False)
    header_fields = df.columns.tolist()
    return render_template("exam_schedules.html", html_table=html_table, header_fields=header_fields)


def course_schedules():
    df = pd.read_excel('SPR_23_COURSES.xlsx')

    # Replace missing values with an empty string #
    df.fillna("", inplace=True)

    # Escape special characters #
    df = df.applymap(lambda x: html.escape(str(x))
                     if isinstance(x, str) else x)

    html_table = df.to_html(index=False, header=False)
    header_fields = df.columns.tolist()
    return render_template("course_schedules.html", html_table=html_table, header_fields=header_fields)


def get_it_signup_guide():
    return render_template("it_signup_guide.html")


def get_teacher_signup_guide():
    return render_template("teacher_signup_guide.html")


def get_admin_signup_guide():
    return render_template("admin_signup_guide.html")


def get_student_signup_help():
    return render_template("student_signup_guide.html")


def get_student_login_help():
    return render_template("student_login_guide.html")


def get_teacher_signup_help():
    return render_template("teacher_signup_guide.html")


def get_teacher_login_help():
    return render_template("teacher_login_guide.html")


def get_it_staff_signup_help():
    return render_template("it_staff_signup_guide.html")


def get_it_staff_login_help():
    return render_template("it_staff_login_guide.html")


def get_description_text():
    return render_template("description_text.html")


def get_opening_help():
    return render_template("opening_screen_help.html")


def goToOpeningScreen():
    return render_template("opening_screen.html")


def includes_ignore_case(s1: str, s2: str) -> bool:
    return (s1.lower() in s2.lower())


def check_includes(credentials: List[str]):
    for i, cred1 in enumerate(credentials):
        for j, cred2 in enumerate(credentials):
            if i != j and includes_ignore_case(cred1, cred2):
                return True
    return False


def user_signup(request, role: str):
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
        session["role"] = role
        session["priority"] = ROLES[role].priority
        newsCount = UR.getNewsCount()
        return redirect(f'/{role}/dashboard?newsCount={newsCount}')

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
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        page_to_be_displayed = str()

        existing_user = UR.getUserByUsernameAndEmail(username, email)

        if not existing_user or not UR.checkUserRole(existing_user, role):
            notExistMessage = f"There is no {ROLES[role].name} with this Username & Email pair."
            folder_directory = concat_folder_dir_based_on_role(role=role)
            page_to_be_displayed += folder_directory
            page_to_be_displayed += f'{role}_login.html'
            return render_template(page_to_be_displayed, notExistMessage=notExistMessage)

        password_check = UR.check_password(existing_user, password)

        if password_check:
            # Redirect to dashboard if user already exists
            session["username"] = username
            session["priority"] = ROLES[role].priority
            session["role"] = role
            newsCount = UR.getNewsCount()
            return redirect(f'/{role}/dashboard?newsCount={newsCount}')
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
    elif UR.userExistsByUsernameAndEmail(username, email) and UR.checkUserRole(UR.getUserByUsernameAndEmail):
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


def extract_first_column_of_ku_class_data():
    df = pd.read_excel('KU_Classrooms.xlsx')
    options = [x for x in df.iloc[:, 0].dropna().tolist() if x not in [
        'CASE', 'SOS', 'SNA', 'ENG', 'SCI']]
    return options
############################################################################################################################################################################################################


def reserve_class():
    role = session["role"]
    class_code = request.form['class-code']
    start_time = request.form['start-time']
    end_time = request.form['end-time']
    date = request.form['date']
    option = request.form['option']
    classroom_code_options = extract_first_column_of_ku_class_data()

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
    rows = UR.getAllITReports()
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
    rows = UR.getAllReservations()
    return render_template('classroom_inside_reservation.html', rows=rows)
#########################################################################################################################################################################


def openStudentReservationScreen():
    options = extract_first_column_of_ku_class_data()
    selected_class_code = request.form.get('class_code')
    value = request.args.get('value')
    if selected_class_code is not None:
        return render_template('student_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('student_reservation_screen.html', options=options, selected=value)


def openTeacherReservationScreen():
    options = extract_first_column_of_ku_class_data()
    selected_class_code = request.form.get('class_code')
    if selected_class_code is not None:
        return render_template('teacher_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('teacher_reservation_screen.html', options=options)


def openITStaffReservationScreen():
    options = extract_first_column_of_ku_class_data()
    selected_class_code = request.form.get('class_code')
    if selected_class_code is not None:
        selected_class_code = options[int(selected_class_code)]
        return render_template('it_staff_reservation_screen.html', options=options, class_code=selected_class_code)
    return render_template('it_staff_reservation_screen.html', options=options)


def opening_screen():
    return render_template("opening_screen.html")


def user_screen(role: str):
    return render_template(f'{role}_pages/{role}_screen.html')


def user_dashboard(role: str):
    return render_template(f'{role}_pages/{role}_dashboard.html', news_data=UR.getNews(), newsCount=UR.getNewsCount())


def go_to_opening_screen():
    return render_template('opening_screen.html')


def OpenReserveScreen():
    class_code = request.args.get('class_code')
    return render_template("student_reservation_screen.html")


def updateITReport():
    if request.method == 'POST':
        report_no = request.form['report_no']
        room_name = request.form['room_name']
        faculty_name = request.form['faculty_name']
        problem_description = request.form['problem_description']
        date = request.form['date']
        time = request.form['time']
        UR.updateITReport(
            report_no=report_no,
            room_name=room_name,
            faculty_name=faculty_name,
            problem_description=problem_description,
            date=date,
            time=time
        )
        return redirect(url_for('successfulUpdateOfITReport'))
    else:
        return render_template('editITReport.html')


def updateReservation():
    if request.method == 'POST':
        current_reservation_id = request.form['reservation_id']
        user_role = request.form['role']
        reservation_date = request.form['date']
        reservation_time = request.form['time']
        reserver_username = request.form['username_of_reserver']
        reservation_purpose = request.form['reservation_purpose']
        reserved_classroom = request.form['classroom_name']
        priority_reserved = request.form['priority_reserved']
        UR.updateReservation(
            role=user_role,
            date=reservation_date,
            time=reservation_time,
            username=reserver_username,
            reservation_purpose=reservation_purpose,
            reserved_classroom=reserved_classroom,
            priority_reserved=priority_reserved,
            id=current_reservation_id
        )
        return redirect(url_for('successfulUpdateOfReservation'))
    else:
        return render_template('editReservations.html')


def seeTheUsers():
    usernames = UR.getAllUsernames()
    return render_template('admin_pages/admin_see_users.html', usernames=usernames)


def seeTheReservations():
    data = UR.getAllReservations()
    return render_template('admin_pages/see_the_reservations.html', reservations=data)


def editUser(username):
    return render_template('edit_users.html', username=username)


def editITReport():
    row = request.args.get('row_data').split(',')
    return render_template("editITReport.html", row=row)


def editClassroomReservations():
    row = request.args.get('row_data').split(',')
    return render_template("editReservations.html", row=row)


def deleteReservation():
    if request.method == "POST":
        role = request.form['role']
        date = request.form['date']
        time = request.form['time']
        username = request.form['username_of_reserver']
        public_or_private = request.form['reservation_purpose']
        classroom = request.form['classroom_name']
        priority_reserved = request.form['priority_reserved']
        UR.delete_reservation_from_db(
            role=role,
            date=date,
            time=time,
            username=username,
            public_or_private=public_or_private,
            classroom=classroom,
            priority_reserved=priority_reserved
        )
        return render_template("successfulDeletionOfClassReservation.html")
    else:
        return render_template("editReservations.html")


def deleteITReport():
    report_no = request.form['report_no']
    room_name = request.form['room_name']
    faculty_name = request.form['faculty_name']
    problem_description = request.form['problem_description']
    date = request.form['date']
    time = request.form['time']
    UR.delete_it_report_from_db(
        report_no=report_no,
        room_name=room_name,
        faculty_name=faculty_name,
        problem_description=problem_description,
        date=date,
        time=time
    )
    return render_template("successfulDeletionOfITReport.html")


def seeITReports():
    data = UR.getAllITReports()
    return render_template('admin_pages/admin_see_IT_reports.html', IT_Reports=data)


def it_report_statistics_for_admin():
    return render_template("it_report_statistics_for_admin.html")


def enterChat():
    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()
    # Retrieve all the rows from the reservations_db table
    # where classroom = "' + \    session["classroom"] + '"'
    query1 = 'SELECT * FROM chat_db'
    c.execute(query1)
    data = c.fetchall()
    # Close the database connection
    conn.close()
    # Retrieve the classroom parameter
    session["classroom"] = request.args.get('classroom')

    return render_template('chat_class_generic.html', rows=data)


def seeOnlyMyReserves():
    incoming_arg = request.args.get('reservationType')
    if incoming_arg == "myReservations":
        conn = sqlite3.connect('reservations_db.db')
        c = conn.cursor()
        query1 = 'SELECT * FROM reservations_db where username = "' + \
            session["username"] + '"'
        c.execute(query1)
        data = c.fetchall()
        conn.close()
        return render_template('classroom_inside_reservation.html', rows=data)
    else:
        data = UR.getAllReservations()
        return render_template('classroom_inside_reservation.html', rows=data)


def delete_old_chat_messages():
    UR.delete_chat_messages()


def send_chat_message_student():

    classroom = session['classroom']
    time = str(datetime.datetime.now().time())
    date = str(datetime.date.today())
    sender = session['username']
    role = session['role']
    flagged = False
    message = request.args.get('message')
    session['message'] = message
    message = request.args.get('message')
    classroom = message
    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()

    c.execute("INSERT INTO chat_db (classroom, time, date, sender, role, flagged) VALUES (?, ?, ?, ?, ?, ?)",
              (classroom, time, date, sender, role, flagged))

    conn.commit()
    conn.close()

    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()
    query1 = 'SELECT * FROM chat_db'
    c.execute(query1)
    data = c.fetchall()
    data.append(('classroom', session["classroom"]))

    conn.close()
    return render_template('chat_class_generic.html', rows=data, class_data=classroom, user_name=session["username"], message=message)


def myExamsOnly():
    df = pd.read_excel('FALL_22_EXAMS.xlsx')
    df.fillna("", inplace=True)
    df = df.applymap(lambda x: html.escape(str(x))
                     if isinstance(x, str) else x)

    args_array = []

    class_name = request.args.get('class_name')
    class_code = request.args.get('class_code')
    subject = request.args.get('subject')
    catalog = request.args.get('catalog')
    description = request.args.get('description')
    section = request.args.get('section')
    courseid = request.args.get('courseid')
    examdate = request.args.get('examdate')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    facilid = request.args.get('facilid')
    examtype = request.args.get('examtype')
    instructorname = request.args.get('instructorname')
    totalenr = request.args.get('totalenr')
    acadorg = request.args.get('acadorg')

    args_array.append(("class_name", class_name))
    args_array.append(("class_code", class_code))
    args_array.append(("subject", subject))
    args_array.append(("catalog", catalog))
    args_array.append(("description", description))
    args_array.append(("section", section))
    args_array.append(("courseid", courseid))
    args_array.append(("examdate", examdate))
    args_array.append(("starttime", starttime))
    args_array.append(("endtime", endtime))
    args_array.append(("facilid", facilid))
    args_array.append(("examtype", examtype))
    args_array.append(("instructorname", instructorname))
    args_array.append(("totalenr", totalenr))
    args_array.append(("acadorg", acadorg))

    search_args = ["|".join([x[1] for x in args_array if x[1]])]
    search_args.extend([f"{key}={value}" for key, value in request.args.items(
    ) if value and key != "class_code"])

    df = df[df.apply(lambda row: row.astype(str).str.startswith(tuple(search_args)).any() or
                     row.astype(str).str.startswith(class_code).any(), axis=1)]

    html_table = df.to_html(index=False, header=False)
    header_fields = df.columns.tolist()
    return render_template("exam_schedules.html", html_table=html_table, header_fields=header_fields)


def allExams():
    return exam_schedules()


def createNews():
    return render_template("admin_create_news.html")


def createNewsElement():
    news_message = request.form.get('news_message')
    date = request.form.get('date')
    time = request.form.get('time')
    date_end = request.form.get('date_end')
    time_end = request.form.get('time_end')
    sender = session["username"]
    role = session["role"]
    UR.insert_news_to_newsdb(
        news_message=news_message,
        time=time,
        date=date,
        time_end=time_end,
        date_end=date_end,
        sender=sender,
        role=role
    )
    return render_template("admin_create_news.html")


def get_reservation_statistics_screen():
    return render_template("reservation_statistics.html")


def open_user_statistics_screen():
    return render_template("user_statistics.html")


def successfulUpdateOfITReport():
    return render_template('successfulUpdateOfITReport.html')


def successfulUpdateOfReservation():
    return render_template('successfulUpdateOfClassReservation.html')


def clearMessages():
    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()

    c.execute("DELETE FROM chat_db")

    conn.commit()
    conn.close()

    conn = sqlite3.connect('chat_db.db')
    c = conn.cursor()
    query1 = 'SELECT * FROM chat_db'
    c.execute(query1)
    data = c.fetchall()
    data.append(('classroom', session["classroom"]))

    conn.close()
    return render_template('chat_class_generic.html', rows=data, user_name=session["username"], message="No Messages Recieved Yet")


def makeAnnouncment():
    news_message = request.form.get('news_message')
    date = request.form.get('date')
    time = request.form.get('time')
    date_end = request.form.get('date_end')
    time_end = request.form.get('time_end')
    sender = session["username"]
    role = session["role"]
    UR.insert_news_to_newsdb(
        news_message=news_message,
        time=time,
        date=date,
        time_end=time_end,
        date_end=date_end,
        sender=sender,
        role=role
    )
    return render_template("teacher_announcement.html")
