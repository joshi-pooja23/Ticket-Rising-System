# 🎫 Ticket Raising System (Flask & MongoDB)

A full-stack web-based **Ticket Raising & Help Desk Management System** built with **Python (Flask)** and **MongoDB**. It allows users to register, raise support tickets, and track issue statuses in real time, while providing administrators with a centralized dashboard to manage and resolve incoming tickets.

---

## 🚀 Key Features

### 👤 User Portal
* **Secure Authentication:** User registration and login with password hashing powered by `Flask-Bcrypt` and session-based access control.
* **Raise Support Tickets:** Submit new support tickets with a title, detailed description, and automatic timestamping.
* **Personal Dashboard & Ticket Tracking:** View all submitted tickets, inspect individual ticket details, and monitor real-time status updates (`Open`, `In Progress`, `Resolved`, `Closed`).

### 🛡️ Admin Portal
* **Dedicated Admin Authentication:** Separate admin login portal with automatic default admin account initialization on startup.
* **Centralized Ticket Overview:** View all tickets raised across every registered user in one dashboard.
* **Status Management:** Update ticket statuses as issues are investigated and resolved.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** MongoDB (`PyMongo`)
* **Security:** Flask-Bcrypt (Password Hashing), Flask Sessions
* **Frontend:** HTML5, Jinja2 Templates (Bootstrap recommended)

---

## 📁 Project Structure

```text
ticket-raising-system/
├── app.py                  # Main Flask application & routes
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── templates/              # Jinja2 HTML templates
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── raise_ticket.html
    ├── my_tickets.html
    ├── view_ticket.html
    ├── admin_login.html
    ├── admin_dashboard.html
    └── edit_ticket.html