from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
    
@app.route('/signup_success')
def signup_success():
    return "Signup successful!"

@app.route('/', methods=['GET', 'POST'])
def opening_screen():
    return render_template("opening_screen.html")

@app.route('/role_selection', methods=['POST'])
def role_selection():
    role = request.form.get('roles')
    if role == 'teacher':
        return redirect(url_for('teacher_screen'))
    elif role == 'student':
        return redirect(url_for('student_screen'))
    elif role == 'it_staff':
        return redirect(url_for('it_staff_screen'))
    else:
        # Invalid role selected, render the opening screen again
        return render_template('opening_screen.html')


@app.route('/teacher_screen')
def teacher_screen():
    return render_template('teacher_screen.html')

@app.route('/student_screen')
def student_screen():
    return render_template('student_screen.html')

@app.route('/it_staff_screen')
def it_staff_screen():
    return render_template('it_staff_screen.html')

@app.route('/student_dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')



@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        # Get the username and password from the form data
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('students_signup_db.db')
        c = conn.cursor()

        # Create the students_signup_db table if it doesn't exist yet
        c.execute('''CREATE TABLE IF NOT EXISTS students_signup_db
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     username TEXT NOT NULL, 
                     password TEXT NOT NULL)''')

        # Check if the username-password pair already exists in the database
        c.execute("SELECT * FROM students_signup_db WHERE username = ? AND password = ?", (username, password))
        existing_student = c.fetchone()
        if existing_student:
            # Display error message if student already exists
            error_message = "You have already signed up. Please go to the login screen by clicking below button."
            return render_template('student_signup.html', error_message=error_message)
        else:
            # Insert the new student into the database
            c.execute("INSERT INTO students_signup_db (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()

            alert_message = "Signup successful! Now you can go to student dashboard by clicking below button."

            return render_template('student_signup.html', alert_message=alert_message)

    # Render the student signup form
    return render_template('student_signup.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/student_screen') # burdda student dashboardduna redirect etmesi gerekiyor (chat kısmı, sınıf bilgisi falan bburda olcak)
    else:
        return render_template('student_login.html')
    
@app.route('/it_staff_signup', methods=['GET', 'POST'])
def it_staff_signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/it_staff_screen') # burdda it_staff dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
    else:
        return render_template('it_staff_signup.html')
    

@app.route('/it_staff_login', methods=['GET', 'POST'])
def it_staff_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/it_staff_screen') # burdda it_staff dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
    else:
        return render_template('it_staff_login.html')
    
@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/teacher_screen') # burdda teacher dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
    else:
        return render_template('teacher_signup.html')
    

@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/teacher_screen') # burdda teacher dashboardduna redirect etmesi gerekiyor (chat kısmı, it panel, sınıf bilgisi falan bburda olcak)
    else:
        return render_template('teacher_login.html')
    
if __name__=='main':
    app.run(debug=True, host="127.0.0.1", port="5000")





