from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .db import get_db
from datetime import datetime,timedelta

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
def student_dashboard():
    student_id = session.get('user_id')
    if not student_id:
        flash('You must be logged in as a student to access the dashboard.', 'warning')
        return redirect(url_for('user.login'))
    
    return render_template('student/student_dashboard.html')


@student_bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    db_conn = get_db()
    student_id = session.get('user_id')
    hostel_key = session.get('hostel_key')

    now = datetime.now()
    start_time = now.replace(hour  = 17, minute = 0, second = 0, microsecond = 0)
    end_time = now.replace(hour = 21, minute = 0, second = 0, microsecond = 0)

    if not (start_time <= now <= end_time):
        flash('Attendance can only be marked between 5 PM and 9 PM.')
        return render_template('student/attendance_error.html')

    next_day = (now + timedelta(days=1)).date()

    if request.method == 'POST':
        attendance_status = request.form.get('attendance_status')

        check = db_conn.execute(
            "SELECT * FROM attendance_register WHERE student_id = ? AND date = ?", 
            (student_id, next_day)
        ).fetchone()

        if check:
            flash("You have already registered the attendance for tomorrow.")
            return render_template('student/attendance_error.html')

        if attendance_status in ["Present", "Absent"]:
            db_conn.execute(
                "INSERT INTO attendance_register (hostel_id, student_id, attendance, date) VALUES (?, ?, ?, ?)",
                (hostel_key, student_id, attendance_status, next_day)
            )
            db_conn.commit()
            flash('Attendance marked successfully!')
            return redirect(url_for('student.attendance'))

    return render_template('student/mark_attendance.html')


@student_bp.route('/register_complaint', methods=['GET', 'POST'])
def register_complaint():
    student_id = session.get('user_id')
    hostel_id = session.get('hostel_key')
    if request.method == 'POST':
        complaint = request.form['complaint']
        date = datetime.today().date()

        db_conn = get_db()

        db_conn.execute(
            "INSERT INTO complaints (hostel_key, student_id, complaint_text, date) VALUES (?, ?, ?, ?)",
            (hostel_id, student_id, complaint, date)
        )
        db_conn.commit()

        flash("Complaint registered")
        return redirect(url_for('student.register_complaint'))

    return render_template('student/register_complaint.html')



def days_in_previous_month():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.day


@student_bp.route('/view_fees', methods=['GET'])
def view_fees():
    db_conn = get_db()
    student_id = session.get('user_id')

    # Ensure that the student's fees are fetched correctly
    student_fees = db_conn.execute(
        "SELECT room_rent, mess_fee, maintenance_fee, total_fee FROM student_fees WHERE student_id = ? ORDER BY id DESC LIMIT 1",
        (student_id,)
    ).fetchone()

    if not student_fees:
        flash('Fee information not found.')
        return redirect(url_for('student.student_dashboard'))

    room_rent = student_fees['room_rent']
    mess_fee = student_fees['mess_fee']
    maintenance_fee = student_fees['maintenance_fee']
    total_fee_due = student_fees['total_fee']

    return render_template('student/view_fees.html', total_fee_due=total_fee_due, room_rent=room_rent, mess_fee=mess_fee, maintenance_fee=maintenance_fee)


@student_bp.route('/view_announcements')
def view_announcements():
    db_conn = get_db()
    hostel_key = session.get('hostel_key')

    announcements = db_conn.execute(
        'SELECT announcement_text FROM announcements WHERE warden_id = (SELECT id FROM wardens WHERE hostel_key = ?)',
        (hostel_key,)
    ).fetchall()

    return render_template('student/view_announcement.html', announcements=announcements)
