-- Define the schema for HostelDays database
DROP TABLE IF EXISTS hostels;
DROP TABLE IF EXISTS wardens;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS approval_requests;
DROP TABLE IF EXISTS announcements;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS maintenance;
DROP TABLE IF EXISTS attendance_register;
DROP TABLE IF EXISTS student_fees;


-- Table for hostels
CREATE TABLE hostels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unique_key TEXT NOT NULL UNIQUE,
    room_rent INTEGER,
    max_mess_fees INTEGER
);


-- Table for wardens
CREATE TABLE wardens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    hostel_key TEXT NOT NULL,
    FOREIGN KEY (hostel_key) REFERENCES hostels (unique_key)
);


-- Table for students
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    admission_number TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL,
    hostel_key TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending_approval',
    warden_id INTEGER,
    FOREIGN KEY (hostel_key) REFERENCES hostels (unique_key),
    FOREIGN KEY (warden_id) REFERENCES wardens (id)
);


-- Table for student attendance register
CREATE TABLE attendance_register(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostel_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    attendance TEXT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (hostel_id) REFERENCES hostels (unique_key)
    FOREIGN KEY (student_id) REFERENCES students (id)
);

-- Table for announcements
CREATE TABLE announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    warden_id INTEGER NOT NULL,
    announcement_text TEXT NOT NULL,
    FOREIGN KEY (warden_id) REFERENCES wardens (id)
);

-- Table for complaints
CREATE TABLE complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostel_key TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    complaint_text TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
    FOREIGN KEY (hostel_key) REFERENCES hostels(unique_key)
);

-- Table for maintenance costs
CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostel_id INTEGER NOT NULL,
    maintenance_cost INTEGER NOT NULL,
    FOREIGN KEY (hostel_id) REFERENCES hostels (id)
);

-- Table for storing calculated student fees
CREATE TABLE student_fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    room_rent INTEGER NOT NULL,
    mess_fee INTEGER NOT NULL,
    maintenance_fee INTEGER NOT NULL,
    total_fee INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
);
