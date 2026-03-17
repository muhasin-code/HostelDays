# 🏥 HostelDays

> A Premium, Modern Hostel Management System built with Flask & SQLite.

HostelDays is a comprehensive web application designed to streamline hostel operations for both wardens and students. It features a stunning, modern user interface built on the principles of **Glassmorphism**, providing a premium experience that is as intuitive as it is beautiful.

![Modern UI Preview](https://img.shields.io/badge/UI-Modern_Glassmorphism-blueviolet?style=for-the-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.0+-blue?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Data-003B57?style=for-the-badge&logo=sqlite)

---

> 📚 **Academic Project** — Built as a minor project for the BSc Computer Science
> curriculum at the University of Kerala (2023). Demonstrates full-stack web development
> with Flask, role-based access control, and domain-driven feature design.
```

**2. Fix the `schema.sql` — it's actually a strength, highlight it.** Most student Flask projects don't include a proper SQL schema file. Add a mention of it in the project structure section:
```
├── schema.sql              # Full database schema — initialize with flask init-db

## ✨ Features

### 🛡️ Warden Management

- **Centralized Dashboard**: At-a-glance view of pending approvals and student complaints.
- **Student Onboarding**: Review and approve/deny new student registrations with a single click.
- **Attendance Monitoring**: Trace student presence records through a refined tabular interface.
- **Automated Fee Calculation**: Dynamic calculation of monthly dues based on room rent, maintenance, and actual mess usage (derived from attendance).
- **Broadcast System**: Post hostel-wide announcements that appear instantly on all student dashboards.
- **Issue Resolution**: Monitor and manage student-reported maintenance issues and complaints.

### 🎓 Student Experience

- **Personalized Dashboard**: View latest announcements and personal status immediately upon login.
- **Smart Attendance**: Mark presence for upcoming meals between 5 PM and 9 PM to minimize food waste.
- **Transparent Billing**: Detailed breakdown of monthly fees, including room rent, mess charges, and maintenance costs.
- **Digital Complaints**: Easily report maintenance issues directly to the warden's dashboard.
- **Mobile Friendly**: Fully responsive design for managing hostel life on the go.

---

## 🎨 Design Aesthetics

HostelDays isn't just a management tool; it's a visual experience:

- **Glassmorphism**: Elegant, translucent interfaces with real-time backdrop filtering.
- **Inter Typography**: Using the modern Inter font for superior clarity and a pro-tech feel.
- **Lucide Iconography**: Consistent, high-quality icons for intuitive navigation.
- **Dynamic Gradients**: Subtle, professional background gradients providing a premium depth.
- **Smooth Transitions**: Micro-animations and fade-ins for a fluid user journey.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- `pip` (Python Package Manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/muhasin-code/HostelDays.git
   cd HostelDays
   ```

2. **Set up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   flask --app . init-db
   ```

### Running the App

```bash
flask --app . run --debug
```

Access the application at `http://127.0.0.1:5000`.

---

## 📂 Project Structure

```text
HostelDays/
├── instance/               # SQLite database storage
├── static/
│   ├── css/
│   │   └── style.css       # Core design system & glassmorphism
├── templates/
│   ├── student/            # Student role templates
│   ├── warden/             # Warden role templates
│   ├── base.html           # Master layout
│   ├── dashboard_base.html # Sidebar layout for dashboard
│   └── index.html          # Modern hero landing page
├── db.py                   # Database connection logic
├── student.py              # Student-side routes & logic
└── warden.py               # Warden-side routes & logic
```

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: Vanilla CSS3, Jinja2 Templates
- **Icons**: Lucide Icons
- **Fonts**: Inter (Google Fonts)

---

## 🔄 If I Were Building This Today

- Replace SQLite with PostgreSQL for concurrent access
- Add proper session management and CSRF protection
- Deploy with Gunicorn + Nginx (as done in RoboStock)
- Add unit tests for fee calculation logic

_Created with ❤️ for better hostel management._
