from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from . import db

from datetime import datetime, timedelta
from calendar import monthrange

warden_bp = Blueprint('warden', __name__)

@warden_bp.route('/dashboard')
def dashboard():
    warden_id = session.get('user_id')
    if not warden_id:
        flash('You must be logged in as a warden to access the dashboard.', 'warning')
        return redirect(url_for('user.login'))

    return render_template('warden/warden_dashboard.html')

@warden_bp.route('/approval_requests', methods=['GET'])
def approval_requests():
    db_conn = db.get_db()
    status = 'pending_approval'
    hostel_id = session.get('hostel_key')
    pending_requests = db_conn.execute(
        "SELECT id, name, admission_number, age, course FROM students WHERE status = ? and hostel_key = ?", (status, hostel_id)
    ).fetchall()
    return render_template('warden/approval_requests.html', approval_requests=pending_requests)

@warden_bp.route('/approve_request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    db_conn = db.get_db()
    db_conn.execute(
        "UPDATE students SET status = 'approved' WHERE id = ?", (request_id,)
    )
    db_conn.commit()
    return redirect(url_for('warden.approval_requests'))

@warden_bp.route('/deny_request/<int:request_id>', methods=['POST'])
def deny_request(request_id):
    db_conn = db.get_db()
    db_conn.execute(
        "DELETE FROM students WHERE id = ?", (request_id,)
    )
    db_conn.commit()
    return redirect(url_for('warden.approval_requests'))



@warden_bp.route('/view_complaints')
def view_complaints():
    hostel_id = session.get('hostel_key')
    db_conn = db.get_db()

    # Fetch all complaints for the hostel
    complaints = db_conn.execute(
        "SELECT * FROM complaints WHERE hostel_key = ?", (hostel_id,)
    ).fetchall()

    # Create a list to hold complaints with student names
    complaints_with_students = []

    # Fetch student names for each complaint
    for complaint in complaints:
        student = db_conn.execute(
            "SELECT name FROM students WHERE id = ?", (complaint['student_id'],)
        ).fetchone()
        # Add student name to the complaint dictionary
        complaint_with_student = dict(complaint)
        complaint_with_student['student_name'] = student['name']
        complaints_with_students.append(complaint_with_student)
    
    return render_template('warden/view_complaints.html', complaints=complaints_with_students)



@warden_bp.route('/manage_students', methods=['GET', 'POST'])
def manage_students():
    db_conn = db.get_db()
    hostel_id = session.get('hostel_key')
    status = 'approved'

    if request.method == 'POST':
        student_id = request.form['student_id']
        
        # Remove the student from the students table
        db_conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        db_conn.commit()
        flash('Student removed successfully.')

    # Fetch the approved students
    students = db_conn.execute(
        "SELECT * FROM students WHERE hostel_key = ? AND status = ?",
        (hostel_id, status)
    ).fetchall()

    return render_template('warden/manage_students.html', approved_students=students)



@warden_bp.route('/view_fees', methods=['GET', 'POST'])
def view_fees():
    db_conn = db.get_db()
    hostel_key = session.get('hostel_key')
    
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    fifth_day_of_month = today.replace(day=5)  # Corrected the day to 5th instead of 20th
    
    show_fee_update_form = first_day_of_month <= today <= fifth_day_of_month

    if request.method == 'POST' and show_fee_update_form:
        room_rent = request.form['room_rent']
        maintenance_cost = request.form['maintenance_cost']
        max_mess_fees = request.form['max_mess_fees']

        db_conn.execute(
            'UPDATE hostels SET room_rent = ?, max_mess_fees = ? WHERE unique_key = ?',
            (room_rent, max_mess_fees, hostel_key)
        )
        db_conn.execute(
            'INSERT INTO maintenance (hostel_id, maintenance_cost) VALUES (?, ?)',
            (hostel_key, maintenance_cost)
        )
        db_conn.commit()
        flash('Fees updated successfully!')

    # Fetch room rent and max mess fees
    hostel_info = db_conn.execute(
        'SELECT room_rent, max_mess_fees FROM hostels WHERE unique_key = ?',
        (hostel_key,)
    ).fetchone()

    room_rent = hostel_info['room_rent'] if hostel_info['room_rent'] is not None else 0
    max_mess_fees = hostel_info['max_mess_fees'] if hostel_info['max_mess_fees'] is not None else 0

    maintenance_cost = db_conn.execute(
        'SELECT SUM(maintenance_cost) AS total_maintenance_cost FROM maintenance WHERE hostel_id = ?',
        (hostel_key,)
    ).fetchone()
    total_maintenance_cost = maintenance_cost['total_maintenance_cost'] if maintenance_cost['total_maintenance_cost'] is not None else 0

    # Fetch students and calculate their total fees
    students = db_conn.execute(
        'SELECT id, name, admission_number FROM students WHERE hostel_key = ?',
        (hostel_key,)
    ).fetchall()

    previous_month = today.replace(day=1) - timedelta(days=1)
    previous_month_days = monthrange(previous_month.year, previous_month.month)[1]
    maintenance_per_student = total_maintenance_cost / len(students) if students else 0
    mess_fee_per_day = max_mess_fees / previous_month_days if previous_month_days else 0

    students_fees = []

    for student in students:
        student_id = student['id']
        absents = db_conn.execute(
            'SELECT COUNT(*) AS absents FROM attendance_register WHERE student_id = ? AND attendance = "Absent" AND strftime("%Y-%m", date) = ?',
            (student_id, previous_month.strftime('%Y-%m'))
        ).fetchone()['absents']
        
        mess_fee = mess_fee_per_day * absents
        total_fee_due = room_rent + (max_mess_fees - mess_fee) + maintenance_per_student
        
        students_fees.append({
            'name': student['name'],
            'admission_number': student['admission_number'],
            'total_fee_due': total_fee_due
        })
        
        db_conn.execute(
            'INSERT INTO student_fees (student_id, room_rent, mess_fee, maintenance_fee, total_fee) VALUES (?, ?, ?, ?, ?)',
            (student_id, room_rent, max_mess_fees - mess_fee, maintenance_per_student, total_fee_due)
        )

    db_conn.commit()

    previous_month_name = previous_month.strftime('%B')

    return render_template('warden/view_fees.html', 
                           show_fee_update_form=show_fee_update_form, 
                           room_rent=room_rent, 
                           max_mess_fees=max_mess_fees, 
                           students_fees=students_fees,
                           previous_month=previous_month_name)



@warden_bp.route('/view_attendance')
def view_attendance():
    db_conn = db.get_db()
    hostel_key = session.get('hostel_key')

    attendance_records = db_conn.execute(
        "SELECT s.name, s.admission_number, ar.attendance FROM attendance_register ar "
        "JOIN students s ON ar.student_id = s.id WHERE ar.hostel_id = ?",
        (hostel_key,)
    ).fetchall()

    return render_template('warden/view_attendance.html', attendance_records=attendance_records)


@warden_bp.route('/make_announcement', methods=['GET', 'POST'])
def make_announcement():
    if request.method == 'POST':
        warden_id = session.get('user_id')
        announcement_text = request.form['announcement_text']

        db_conn = db.get_db()
        db_conn.execute(
            'INSERT INTO announcements (warden_id, announcement_text) VALUES (?, ?)',
            (warden_id, announcement_text)
        )
        db_conn.commit()

        flash('Announcement made successfully.')
        return redirect(url_for('warden.dashboard'))

    return render_template('warden/make_announcement.html')