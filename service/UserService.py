from flask import render_template, redirect, session,  flash, request, Flask, url_for, jsonify
import sqlite3
import repository.UserRepository as UR
from flask import flash

app = Flask(__name__)

app.secret_key = '491'

app.config['SECRET_KEY'] = '491'

@app.route('/student_signup', methods=['GET', 'POST'])
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




@app.route('/student_login', methods=['GET', 'POST'])
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

@app.route('/password_change', methods=['POST'])
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


@app.route('/password_change_screen', methods=['GET'])
def password_change_screen():
    email = request.args.get('email')

    # Render the password change screen with email as parameter
    return render_template('password_change_screen.html', email=email)

from flask import flash

@app.route('/student_password_change', methods=['GET', 'POST'])
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
        c.execute(
            "UPDATE students_signup_db SET password = ? WHERE email = ?", (UR.encrypt_password(password=new_password), email))
        conn.commit()
        conn.close()

        # Redirect to the password_change_success screen
        flash('Password changed successfully!', 'success')
        return redirect(url_for('password_change_success'))

    # Render the password change form
    email = session.get('email', '')
    return render_template('student_password_change.html', email=email)


@app.route('/password_change_success')
def password_change_success():
    return render_template('password_change_success.html')