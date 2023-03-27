from flask import render_template, redirect, session,  flash, request, sqlite3, Flask

import repository.UserRepository as UR

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

        suffix_ku = '@ku.edu.tr'
        upper_suffix_ku = suffix_ku.upper()
        ku_email_detected = email.endswith(suffix_ku) or email.endswith(upper_suffix_ku)

        if not ku_email_detected:
            return """
            <script>
                alert('This email address is not from the KU Domain');
                window.location.href = '/student_signup';
            </script>
            """

        UR.initializeUserTable()
        existing_student = UR.getUserByUsername(username=username)
        if existing_student:
            # Display error message if student already exists
            error_message = "You have already signed up. Please go to the login screen by clicking below button."
            return render_template('student_signup.html', error_message=error_message)
        else:
            # Insert the new student into the database
            UR.createUser(username=username,password=password,email=email)
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

        if not email.endswith('@ku.edu.tr') and not email.endswith('@KU.EDU.TR'):
            flash("This email address is not from the KU Domain")
            return redirect('/student_login')

        conn = sqlite3.connect('students_signup_db.db')
        c = conn.cursor()

        # Check if the username-password pair already exists in the database
        c.execute(
            f"SELECT * FROM students_signup_db WHERE username = '{username}' AND password = '{password}' AND email = '{email}'")
        existing_student = c.fetchone()
        if existing_student:
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