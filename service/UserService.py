from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import repository.UserRepository as UR
from flask import flash
from flask import flash

app = Flask(__name__)
app.secret_key = '491'
app.config['SECRET_KEY'] = '491'

###############STUDENT #####################################################################################

def student_signup():
    if request.method == 'POST':
        # Get the username, password, and email from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        is_ku_email = email.endswith('@ku.edu.tr'.casefold())

        # Check if the email belongs to the KU domain
        if not is_ku_email:
            return """
            <script>
                alert('This email address is not from the KU Domain');
                window.location.href = '/student_signup';
            </script>
            """

        # Check if a user with the same username already exists in the database
        existing_user = UR.getUserByUsername(username)
        if existing_user is not None:
             username_taken_error = "This username is already taken. Please choose a different one."
             return render_template('student_signup.html', username_taken_error=username_taken_error)

        # Check if a user with the same email already exists in the database
        existing_user = UR.getUserByEmail(email)
        if existing_user is not None:
            email_taken_error = "An account with this email already exists. Please choose a different email or try logging in."
            return render_template('student_signup.html', email_taken_error=email_taken_error)

        # Insert the new user into the database
        UR.createUser(username=username, password=password, email=email)
        success_message = "You have successfully signed up. Please press the below button to go to the student dashboard."
        button_text = "Go To Student Dashboard"
        button_url = "/student_dashboard"
        return render_template('student_signup.html', success_message=success_message, button_text=button_text, button_url=button_url)

    # Render the student signup form
    return render_template('student_signup.html')



def student_login():
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        email_suffix = '@ku.edu.tr'
        casefold_suffix = email_suffix.casefold()
        bigger_suffix = email_suffix.upper()
        ku_domain_email = email_suffix or casefold_suffix or bigger_suffix

        if not ku_domain_email:
            flash("This email address is not from the KU Domain")
            return redirect('/student_login')

        conn = sqlite3.connect('students_signup_db.db')
        c = conn.cursor()

        c.execute(
            f"SELECT * FROM students_signup_db WHERE username = '{username}' AND email = '{email}'")

        existing_student = c.fetchone()

        if not existing_student:
            notExistMessage = "Username does not exist."
            return render_template('student_login.html',notExistMessage=notExistMessage)
        password_check = UR.check_password(existing_student, password)
     
        if existing_student and password_check:
            # Redirect to dashboard if student already exists
            return redirect('/student_dashboard')
        
        else:
            # Render template with message and button to go to signup screen
            message = "You haven't signed up yet. Please go to student signup screen by clicking below button."
            button_text = "Go To Student Signup Screen"
            button_url = "/student_signup"
            return render_template('student_login.html', message=message, button_text=button_text, button_url=button_url)

    # Render the student login form
    return render_template('student_login.html')

def password_change():
    email = request.form.get('email')

    ku_suffix = '@ku.edu.tr'
    upper_ku_suffix = ku_suffix.upper()

    belong_to_KU = (email.endswith(upper_ku_suffix) or email.endswith(ku_suffix))

    # Check if the email has a valid domain
    if not belong_to_KU:
        return jsonify({'error': 'This email address does not belong to the KU domain'})

    # Redirect the user to the password change screen
    return redirect(url_for('password_change_screen', email=email))


def password_change_screen():
    email = request.args.get('email')

    # Render the password change screen with email as parameter
    return render_template('password_change_screen.html', email=email)



def student_password_change():
    if request.method == 'POST':
        # Get the email, new password, and confirm password from the request body
        email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if email is a KU domain email
        suffix_ku = '@ku.edu.tr'
        upper_suffix_ku = suffix_ku.upper()
        casefold_suffix = suffix_ku.casefold()
        ku_email_detected = email.endswith(suffix_ku) or email.endswith(upper_suffix_ku) or email.endswith(casefold_suffix)

        if not ku_email_detected:
            flash('Please enter a valid KU domain email.', 'error')
            return redirect(url_for('student_password_change'))

        if new_password != confirm_password or new_password == '' or confirm_password == '':
            flash('New password and confirm password must match and be non-empty.', 'error')
            return redirect(url_for('student_password_change'))

        conn = sqlite3.connect('students_signup_db.db')
        c = conn.cursor()

        # Update the password for the student with the given email
        c.execute("UPDATE students_signup_db SET password = ? WHERE email = ?", (UR.encrypt_password(new_password), email))
        conn.commit()
        conn.close()

        # Redirect to the password_change_success screen
        flash('Password changed successfully!', 'success')
        return redirect(url_for('password_change_success', email=email))

    # Render the password change form
    email = session.get('email', '')
    return render_template('student_password_change.html', email=email)

###############STUDENT #####################################################################################


def password_change_success():
    return render_template('password_change_success.html')

def go_to_opening_screen():
    return render_template('opening_screen.html')


################TEACHER##############################################################################
def teacher_signup():
    if request.method == 'POST':
        # Get the username, password, and email from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        is_ku_email = email.endswith('@ku.edu.tr'.casefold())

        # Check if the email belongs to the KU domain
        if not is_ku_email:
            return """
            <script>
                alert('This email address is not from the KU Domain');
                window.location.href = '/teacher_signup';
            </script>
            """

        # Check if a user with the same username already exists in the database
        existing_user = UR.getUserByUsername(username)
        if existing_user is not None:
             username_taken_error = "This username is already taken. Please choose a different one."
             return render_template('teacher_signup.html', username_taken_error=username_taken_error)

        # Check if a user with the same email already exists in the database
        existing_user = UR.getUserByEmail(email)
        if existing_user is not None:
            email_taken_error = "An account with this email already exists. Please choose a different email or try logging in."
            return render_template('teacher_signup.html', email_taken_error=email_taken_error)

        # Insert the new user into the database
        UR.createUser(username=username, password=password, email=email)
        success_message = "You have successfully signed up. Please press the below button to go to the teacher dashboard."
        button_text = "Go To Teacher Dashboard"
        button_url = "/teacher_dashboard"
        return render_template('teacher_signup.html', success_message=success_message, button_text=button_text, button_url=button_url)

    # Render the student signup form
    return render_template('teacher_signup.html')


def teacher_login():
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        email_suffix = '@ku.edu.tr'
        casefold_suffix = email_suffix.casefold()
        bigger_suffix = email_suffix.upper()
        ku_domain_email = email_suffix or casefold_suffix or bigger_suffix

        if not ku_domain_email:
            flash("This email address is not from the KU Domain")
            return redirect('/teacher_login')

        conn = sqlite3.connect('teachers_signup_db.db')
        c = conn.cursor()

        c.execute(
            f"SELECT * FROM teachers_signup_db WHERE username = '{username}' AND email = '{email}'")
        
        existing_student = c.fetchone()

        if not existing_student:
            notExistMessage = "Username does not exist."
            return render_template('teacher_login.html',notExistMessage=notExistMessage)
        
        password_check = UR.check_password(existing_student, password)

        if existing_student and password_check:
            # Redirect to dashboard if student already exists
            return redirect('/teacher_dashboard')
        else:
            # Render template with message and button to go to signup screen
            message = "You haven't signed up yet. Please go to teacher signup screen by clicking below button."
            button_text = "Go To Teacher Signup Screen"
            button_url = "/teacher_signup"
            return render_template('teacher_login.html', message=message, button_text=button_text, button_url=button_url)

    # Render the student login form
    return render_template('teacher_login.html')

################TEACHER##############################################################################





###################IT STAFF######################################################################
def it_staff_signup():
    if request.method == 'POST':
        # Get the username, password, and email from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        is_ku_email = email.endswith('@ku.edu.tr'.casefold())

        # Check if the email belongs to the KU domain
        if not is_ku_email:
            return """
            <script>
                alert('This email address is not from the KU Domain');
                window.location.href = '/it_staff_signup';
            </script>
            """

        # Check if a user with the same username already exists in the database
        existing_user = UR.getUserByUsername(username)
        if existing_user is not None:
             username_taken_error = "This username is already taken. Please choose a different one."
             return render_template('it_staff_signup.html', username_taken_error=username_taken_error)

        # Check if a user with the same email already exists in the database
        existing_user = UR.getUserByEmail(email)
        if existing_user is not None:
            email_taken_error = "An account with this email already exists. Please choose a different email or try logging in."
            return render_template('it_staff_signup.html', email_taken_error=email_taken_error)

        # Insert the new user into the database
        UR.createUser(username=username, password=password, email=email)
        success_message = "You have successfully signed up. Please press the below button to go to the it staff dashboard."
        button_text = "Go To It Staff Dashboard"
        button_url = "/it_staff_dashboard"
        return render_template('it_staff_signup.html', success_message=success_message, button_text=button_text, button_url=button_url)

    # Render the student signup form
    return render_template('it_staff_signup.html')

def it_staff_login():
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        email_suffix = '@ku.edu.tr'
        casefold_suffix = email_suffix.casefold()
        bigger_suffix = email_suffix.upper()
        ku_domain_email = email_suffix or casefold_suffix or bigger_suffix

        if not ku_domain_email:
            flash("This email address is not from the KU Domain")
            return redirect('/it_staff_login')

        conn = sqlite3.connect('it_staff_signup_db.db')
        c = conn.cursor()

        c.execute(
            f"SELECT * FROM it_staff_signup_db WHERE username = '{username}' AND email = '{email}'")
        
        existing_student = c.fetchone()

        if not existing_student:
            notExistMessage = "Username does not exist."
            return render_template('it_staff_login.html',notExistMessage=notExistMessage)
        
        password_check = UR.check_password(existing_student, password)

       
        if existing_student and password_check:
            # Redirect to dashboard if student already exists
            return redirect('/it_staff_dashboard')
        else:
            # Render template with message and button to go to signup screen
            message = "You haven't signed up yet. Please go to it staff signup screen by clicking below button."
            button_text = "Go To It Staff Signup Screen"
            button_url = "/it_staff_signup"
            return render_template('it_staff_login.html', message=message, button_text=button_text, button_url=button_url)

    # Render the student login form
    return render_template('it_staff_login.html')




###################IT STAFF######################################################################



#########OTHER SCREENS #######################################################
def select_role():
    role = request.form.get('roles')
    if role == 'teacher':
        return redirect(url_for('teacher_screen'))
    elif role == 'student':
        return redirect(url_for('student_screen'))
    elif role == 'it_staff':
        return redirect(url_for('it_staff_screen'))
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
            file = open("templates/classrooms_and_info.html", "w")
            file.write(txt_string)
            file.close()
        beginning = '<!DOCTYPE html> <html> <head> <title>Student Dashboard</title> <link rel="stylesheet" type="text/css" href="../static/styles.css"> </head><body>'
        html = ""
        html += beginning
        html += "<table>\n<thead>\n<tr>\n"
        html += "".join([f"<th>{header}</th>\n" for header in heads])
        html += "</tr>\n</thead>\n<tbody>\n"
        html += "".join(
            [f"<tr>{''.join([f'<td>{cell}</td>' for cell in row])}</tr>\n" for row in info])
        html += "</tbody>\n</table>"
        html += "</body></html>"
        create_html_file(html)
        return html
    html = load_classes_with_info('KU_Classrooms.xlsx')
    return render_template("classrooms_and_info.html")


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

    return 'Thank you for reporting the problem to IT!'


def report_chat():

    problem_description = request.form['problem_description']

    with open('IT_Problems.txt', 'a') as f:
        #f.write(f'chatUser: {chatUser}\n')
        f.write(f'Problem Description: {problem_description}\n\n')

    return 'Thank you for reporting the problem to IT!'

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


def getIT():
    with open("classes_teacher.txt", "r") as f:
        content = f.read()
        content = content.replace('\n', '<br>')

    # Return a response to the user
    return render_template("student_dashboard.html", content=content)


def chat_action():
    class_no = request.args.get("classroom")
    session['classroom'] = class_no
    return render_template("chat_room.html", class_no=class_no)


def user_connected(info):
    # send
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

def opening_screen():
    return render_template("opening_screen.html")

def teacher_screen():
    return render_template('teacher_screen.html')

def student_screen():
    return render_template('student_screen.html')

def it_staff_screen():
    return render_template('it_staff_screen.html')

def student_dashboard():
    return render_template('student_dashboard.html')

def teacher_dashboard():
    return render_template('teacher_dashboard.html')

def it_staff_dashboard():
    return render_template('it_staff_dashboard.html')

#########OTHER SCREENS #######################################################