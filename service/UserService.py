from flask import session
from typing import List
from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
from constants import ROLES, DB
import pandas as pd
import repository.UserRepository as UR
import repository.Repository as Repo
import datetime
import html

DEBUG = True
app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'
app.debug = True

def replace_dashes_with_slashes(string:str):
    string = string.replace('-', '/')
    return string

def getAnnouncementScreen():
    return render_template("teacher_announcement.html")

def getClassroomView():
    return render_template("view_inside_of_classroom.html")

def getNewsCount():
    return UR.getNewsCount()

def split_based_on_slash(string: str):
    parts = string.split("/")
    return parts

def replace_day_and_year(date_field_list: list):
    year_field = date_field_list[0]
    date_field_list[0] = date_field_list[2]
    date_field_list[2] = year_field
    return date_field_list

def open_news_screen():
    all_news = UR.getNews()
    modified_news = []
    for new in all_news:
        new_list = list(new)
        new_list[2] = replace_dashes_with_slashes(new_list[2])
        sec_date_field_list = split_based_on_slash(new_list[2])
        new_list[2] = '/'.join(replace_day_and_year(sec_date_field_list))
        
        new_list[4] = replace_dashes_with_slashes(new_list[4])
        fourth_date_field_list = split_based_on_slash(new_list[4])
        new_list[4] = '/'.join(replace_day_and_year(fourth_date_field_list))
        
        modified_news.append(new_list)
        
    return render_template("incoming_news.html", news_data=modified_news)


def redirect_student_dashboard_from_news():
    nc = getNewsCount()
    role = "student"
    return redirect(f'/{role}/dashboard?newsCount={nc}')


def exam_schedules():
    df = pd.read_excel('FALL_22_EXAMS.xlsx')
    df.fillna("", inplace=True)
    df = df.applymap(lambda x: html.escape(str(x))
                     if isinstance(x, str) else x)

    html_table = df.to_html(index=False, header=False)
    header_fields = df.columns.tolist()
    return render_template("exam_schedules.html", html_table=html_table, header_fields=header_fields)


def course_schedules():
    df = pd.read_excel('SPR_23_COURSES.xlsx')
    df.fillna("", inplace=True)
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

def openFeatures():
    return render_template("features.html")


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
        nc = getNewsCount()
        return redirect(f'/{role}/dashboard?newsCount={nc}')

    page_rendered = str()
    page_rendered += concat_folder_dir_based_on_role(role=role)
    page_rendered += f'{role}_signup.html'

    return render_template(page_rendered)


###############STUDENT #####################################################################################


###########for checking security ###########################
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

        if not existing_user or not UR.checkUserRole(existing_user, role=role):
            screen_name = beautify_role_names(role_str=role)
            message = f"There is no {ROLES[role].name} with this Username & Email pair."
            button_text = f"Go To {screen_name} Signup Screen"
            page_to_be_rendered = str()
            page_to_be_rendered += concat_folder_dir_based_on_role(role=role)
            page_to_be_rendered += f'{role}_login.html'
            button_url = f"/{role}_signup"
            return render_template(page_to_be_rendered, message=message, button_text=button_text, button_url=button_url, username=username)

        password_check = UR.check_password(existing_user, password)

        if password_check:
            # Redirect to dashboard if user already exists
            session["username"] = username
            session["priority"] = ROLES[role].priority
            session["role"] = role
            nc = getNewsCount()
            return redirect(f'/{role}/dashboard?newsCount={nc}')

        else:
            # Render template with message and button to go to signup screen
            notExistMessage = f"Invalid password"
            folder_directory = concat_folder_dir_based_on_role(role=role)
            page_to_be_displayed += folder_directory
            page_to_be_displayed += f'{role}_login.html'
            return render_template(page_to_be_displayed, notExistMessage=notExistMessage)

    rendered_page = str()
    rendered_page += concat_folder_dir_based_on_role(role=role)
    rendered_page += f'{role}_login.html'
    return render_template(rendered_page)


def getPriorityByUsername(username):
    """
    If user exists, return their priority.
    Otherwise, return 0.
    """

    priority = UR.getPriorityByUsername(username)

    if not priority:
        return 0

    return priority[0]

def getIdByUsername(username):
    user_id = UR.getIdByUsername(username)

    return user_id


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

    if not validate_role(role):
        is_valid = False
        invalid_role = "This role does not exist. Something went wrong"
        return is_valid, render_template('opening_screen.html')
    if not is_ku_email(email):
        is_valid = False
        not_ku_error = "This email address is not from the KU Domain."
        return is_valid, render_template(page_rendered, not_ku_error=not_ku_error)
    elif UR.userExistsByUsernameAndEmail(username, email) and UR.checkUserRole(UR.getUserByUsernameAndEmail(username=username, email=email), role=role):
        is_valid = False
        screen_name = beautify_role_names(role_str=role)
        signup_error_message = "This account already exists. Please go to " + \
            str(screen_name)+" Login Screen by pressing below button."
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


############################################################################################################################################################################################################
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
    newsCount = UR.getNewsCount()
    return redirect(url_for('open_it_report_success', newsCount=newsCount))

def open_it_report_success():
    newsCount = request.args.get('newsCount')
    return render_template("it_staff_pages/IT_report_success_screen.html", newsCount=newsCount)
    
def seeITReport():
    rows = UR.getAllITReports()
    return render_template('it_staff_pages/IT_report_list.html', rows=rows)


def chat_action():
    classroom = request.args.get("classroom")
    session['classroom'] = classroom
    return render_template("chat_pages/chat_room.html", classroom=classroom)
#########################################################################################################################################################################
def opening_screen():
    return render_template("opening_screen.html")


def user_screen(role: str):
    return render_template(f'{role}_pages/{role}_screen.html')


def user_dashboard(role: str):
    nc = getNewsCount()
    return render_template(f'{role}_pages/{role}_dashboard.html', news_data=UR.getNews(), newsCount=nc)


def go_to_opening_screen():
    return render_template('opening_screen.html')


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


def updateUserInformation():
    if request.method == 'POST':
        user_id = request.form['user_id']
        username = request.form['username']

        user_email = request.form['user_email']
        user_role = request.form['user_role']
        user_priority = request.form['user_priority']

        UR.updateUserInformation(
            user_id, username, user_email, user_role, user_priority)

        return redirect(url_for('successfulUpdateOfUserInformation'))
    else:
        return render_template('admin_edits_users.html')


def deleteUser():
    if request.method == 'POST':
        username = request.form["username"]

        user_email = request.form["user_email"]
        user_role = request.form["user_role"]
        user_priority = request.form["user_priority"]
        user_id = request.form["user_id"]

        UR.deleteUser(username, user_email,
                      user_role, user_priority, user_id)
        return redirect(url_for('successfulDeletionOfUser'))
    else:
        return render_template('admin_edits_users.html')


def seeTheUsers():
    users = UR.getAllUsers()
    return render_template('admin_pages/admin_see_users.html', users=users)


def getUserEditingScreenForAdmin():
    user = request.args.get('row_data').split(',')
    return render_template('admin_edits_users.html', user=user)


def editITReport():
    row = request.args.get('row_data').split(',')
    return render_template("editITReport.html", row=row)


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
    classroom = request.args.get("classroom")
    conn = sqlite3.connect(DB.kuclass_db)
    c = conn.cursor()
    chat_query = f'SELECT * FROM chat_db WHERE classroom = ?'
    
    c.execute(chat_query, (classroom,))
    data = c.fetchall()
    conn.close()

    return render_template('chat_class_generic.html', rows=data, classroom=classroom)

def send_chat_message():
    if request.method == 'POST':
        time = str(datetime.datetime.now().time())
        date = str(datetime.date.today())
        sender = session['username']

        message = request.form.get('message')
        classroom = request.form.get("classroom")
        conn = sqlite3.connect(DB.kuclass_db)
        c = conn.cursor()

        c.execute("INSERT INTO chat_db (classroom, time, date, sender, message) VALUES (?, ?, ?, ?, ?)",
                  (classroom, time, date, sender, message))

        conn.commit()
        conn.close()

        return redirect(url_for('enterChat', classroom=classroom, message = message))
    elif request.method == "GET":
        return render_template('chat_class_generic.html')
    
def allExams():
    return exam_schedules()


def createNews():
    return render_template("admin_create_news.html")


def createNewsElement():
    if request.method == "POST":
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
        return render_template("successful_news_creation_of_admin.html")


def open_user_statistics_screen():
    return render_template("user_statistics.html")


def successfulUpdateOfITReport():
    return render_template('successfulUpdateOfITReport.html')


def successfulUpdateOfUserInformation():
    return render_template("successfulUserUpdate.html")


def successfulDeletionOfUser():
    return render_template("successfulDeletionOfUser.html")


def clearMessages():
    c, conn = Repo.getCursorAndConnection()

    c.execute("DELETE FROM chat_db")

    conn.commit()
    conn.close()

    c, conn = Repo.getCursorAndConnection()
    query1 = 'SELECT * FROM chat_db'
    c.execute(query1)
    data = c.fetchall()
    data.append(('classroom', session["classroom"]))

    conn.close()
    return render_template('chat_class_generic.html', rows=data, user_name=session["username"], message="No Messages Recieved Yet")


def viewFloors():
    return render_template("select_floor.html")

    
def makeAnnouncement():
    if request.method == "POST":
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
        return render_template("successful_announcement_sending.html")


def openMap():
    return render_template("viewSchoolMap.html")

def openEventAttendanceScreen():
    if request.method == "POST":
        attendeeUsername = session["username"]
        attendeeRole = session["role"]
        title = request.form.get('title')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        sender = request.form.get('sender')
        role = request.form.get('role')
        return redirect(url_for("news_attendance",
                                attendeeUsername=attendeeUsername,
                                attendeeRole=attendeeRole,
                                title=title,
                                start_time=start_time,
                                end_time=end_time,
                                start_date=start_date,
                                end_date=end_date,
                                sender=sender,
                                role=role))
    else:
        return redirect(url_for("incoming_news"))


def incoming_news():
    return render_template("incoming_news.html")


def news_attendance():
    attendeeUsername = request.args.get("attendeeUsername")
    attendeeRole = request.args.get("attendeeRole")
    title = request.args.get("title")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sender = request.args.get("sender")
    role = request.args.get("role")
    return render_template("news_attendance.html",
                           attendeeUsername=attendeeUsername,
                           attendeeRole=attendeeRole,
                           title=title,
                           start_time=start_time,
                           end_time=end_time,
                           start_date=start_date,
                           end_date=end_date,
                           sender=sender,
                           role=role)

########################for convenience in table field updating######################
def drop():
    cursor, connection= Repo.getCursorAndConnection()
    cursor.execute("DELETE FROM event_announcements_db")
    connection.commit()
    connection.close()
    return ""
########################for convenience in table field updating######################
def attend_or_not():
    if request.method=="POST":
        attendeeUsername = session["username"]
        attendeeRole = session["role"]
        title = request.form.get('title')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        sender = request.form.get('sender')
        role = request.form.get('role')
        if UR.checkPreviousEventAttendance(username=attendeeUsername, event_title=title):
            return redirect(url_for("already_attended_event"))
        else:
            UR.createAttendee(
            attendeeUsername = attendeeUsername,
            attendeeRole = attendeeRole,
            title=title, 
            start_time=start_time, 
            end_time=end_time,
            start_date=start_date, 
            end_date=end_date, 
            sender=sender, 
            role=role
            )
            return redirect(url_for('success_message_attendance'))
    elif request.method == "GET":
        return redirect(url_for("get_news_attendance"))
            

def get_news_attendance():
    return render_template("news_attendance.html")

def already_attended_event():
    return render_template("alreadyAttendedEvent.html")

def success_message_attendance():
    return render_template("success_message_attendance.html")

def openSCI():
    return render_template("science.html")

def openSOS():
    return render_template("sos.html")

def openENG():
    return render_template("eng.html")

def openCASE():
    return render_template("case.html")

def openELC():
    return render_template("elc.html")

def openLIB():
    return render_template("lib.html")

def openSTD():
    return render_template("std.html")

def openSNAA():
    return render_template("snaa.html")

def openSNAB():
    return render_template("snab.html")
