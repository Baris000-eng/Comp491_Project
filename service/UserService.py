from flask import render_template, redirect, session,  flash, request, Flask
import sqlite3
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