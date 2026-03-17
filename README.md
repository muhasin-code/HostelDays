# HostelDays

Hostel Management System built with Flask and SQLite.

## How to Run

### 1. Set up Virtual Environment (if not already done)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize the Database

Before running the app for the first time, you need to initialize the database:

```bash
flask --app . init-db
```

### 3. Run the Application

You can run the application using the following command:

```bash
flask --app . run --debug
```

The application will be available at `http://127.0.0.1:5000`.

## Features

- Student Registration
- Warden Dashboard
- Room Allocation (to be implemented)
- Leave Requests (to be implemented)
