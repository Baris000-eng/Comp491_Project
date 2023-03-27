from flask import render_template, redirect, session

import repository.UserRepository as UR

def student_signup(request):

    # Get the username and password from the form data
    username = request.form['username']
    password = request.form['password']
 
    existing_student = UR.getUserByUsername(username)

    if existing_student:
        # Display error message if student already exists
        error_message = "This username is already taken."
        return render_template('student_signup.html', error_message=error_message)
    else:
        # Insert the new student into the database
        UR.createUser(username, password)

        # Store the username in a session variable
        # session['username'] = username


        success_message = "You have successfully signed up. Please press the below button to go to the student dashboard."
        button_text = "Go To Student Dashboard"
        button_url = "/student_dashboard"
        return render_template('student_signup.html', success_message=success_message, button_text=button_text, button_url=button_url)
    
def student_login(request):
    # Get the username and password from the form data
    username = request.form['username']
    password = request.form['password']

    existing_student = UR.getUserByUsername(username)

    if not existing_student:
        message = "Can't find your account."
        button_text = "Go To Student Signup Screen"
        button_url = "/student_signup"
        return render_template('student_login.html', message=message, button_text=button_text, button_url=button_url)
    
    if UR.check_password(existing_student, password):
        session['username'] = username
        return redirect('/student_dashboard')
    
    message = "Incorrect password."
    button_text = "Login again"
    button_url = "/student_login"
    return render_template('student_login.html', message=message, button_text=button_text, button_url=button_url)

