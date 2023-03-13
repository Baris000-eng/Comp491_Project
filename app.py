from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

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

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/student_screen')
    else:
        return render_template('student_signup.html')
    

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/student_screen')
    else:
        return render_template('student_login.html')
    
@app.route('/it_staff_signup', methods=['GET', 'POST'])
def it_staff_signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/it_staff_screen')
    else:
        return render_template('it_staff_signup.html')
    

@app.route('/it_staff_login', methods=['GET', 'POST'])
def it_staff_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/it_staff_screen')
    else:
        return render_template('it_staff_login.html')
    
@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/teacher_screen')
    else:
        return render_template('teacher_signup.html')
    

@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        # Handle form submission here
        return redirect('/teacher_screen')
    else:
        return render_template('teacher_login.html')
    
if __name__=='main':
    app.run(debug=True, host="127.0.0.1", port="5000")



