from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():
    return render_template('index.html')

@user_bp.route('/register_hostel', methods=['GET', 'POST'])
def register_hostel():
    if request.method == 'POST':
        hostel_name = request.form['hostel_name']
        unique_key = request.form['unique_id']
        
        db = get_db()
        db.execute(
            'INSERT INTO hostels (name, unique_key) VALUES (?, ?)',
            (hostel_name, unique_key)
        )
        db.commit()
        
        flash('Hostel registered successfully! Please register the warden.')
        return redirect(url_for('user.register_warden'))
    
    return render_template('register_hostel.html')

@user_bp.route('/register_warden', methods=['GET', 'POST'])
def register_warden():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        unique_id = request.form['unique_id']
        
        db = get_db()
        host = db.execute(
            'SELECT * FROM hostels WHERE unique_key=?',
            (unique_id,)
        ).fetchone()

        if host is not None:
            db.execute(
                'INSERT INTO wardens (username, password, hostel_key) VALUES (?, ?, ?)',
                (username, password, unique_id)
            )
            db.commit()
        
            flash('Warden registered successfully!')
            return redirect(url_for('user.login'))
        
        flash("No such hostel")
    
    return render_template('register_warden.html')

@user_bp.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        admission_number = request.form['admission_number']
        hostel_key = request.form['hostel_key']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        age = request.form['age']
        course = request.form['course']
        status = 'pending_approval'  # Initial status
        
        db = get_db()
        db.execute(
            'INSERT INTO students (name, age, course, admission_number, hostel_key, username, password, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, age, course, admission_number, hostel_key, username, password, status)
        )
        db.commit()
        
        flash('Student registered successfully! Please wait for warden approval.')
        return redirect(url_for('user.login'))
    
    return render_template('register_student.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        
        # Check if the user is a warden
        warden = db.execute(
            'SELECT * FROM wardens WHERE username = ?', (username,)
        ).fetchone()
        
        if warden and check_password_hash(warden['password'], password):
            session.clear()
            session['user_id'] = warden['id']
            session['hostel_key'] = warden['hostel_key']
            return redirect(url_for('warden.dashboard'))  # Redirect to warden's dashboard
        
        # Check if the user is a student
        student = db.execute(
            'SELECT * FROM students WHERE username = ?', (username,)
        ).fetchone()
        
        if student and check_password_hash(student['password'], password):
            if student['status'] == 'approved':  # Ensure student is approved by warden
                session.clear()
                session['user_id'] = student['id']
                session['hostel_key'] = student['hostel_key']
                return redirect(url_for('student.student_dashboard'))  # Redirect to student's dashboard
            else:
                flash('Your registration is pending approval.')
        
        flash('Incorrect username or password.')
    
    return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('user.login'))