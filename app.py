# ------------------- Imports -------------------
from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# ------------------- Flask Setup -------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"   # change in production
bcrypt = Bcrypt(app)

# ------------------- MongoDB Setup -------------------
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client.ticket_system

users = db.users
admins = db.admins
tickets = db.tickets

# ------------------- Auto-create Admin -------------------
default_admin_username = "admin"
default_admin_password = "admin123"

if not admins.find_one({"username": default_admin_username}):
    hashed_pw = bcrypt.generate_password_hash(default_admin_password).decode("utf-8")
    admins.insert_one({
        "username": default_admin_username,
        "password": hashed_pw
    })

# ------------------- Home -------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------- User Registration -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if users.find_one({"email": email}):
            return "User already exists"

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw
        })

        return redirect("/login")

    return render_template("register.html")

# ------------------- User Login -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = str(user["_id"])
            session["name"] = user["name"]
            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")

# ------------------- User Dashboard -------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user_tickets = list(
        tickets.find({"user_id": ObjectId(session["user"])})
    )

    return render_template(
        "dashboard.html",
        name=session["name"],
        tickets=user_tickets
    )

# ------------------- Raise Ticket -------------------
@app.route("/raise_ticket", methods=["GET", "POST"])
def raise_ticket():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        tickets.insert_one({
            "user_id": ObjectId(session["user"]),
            "title": request.form["title"],
            "description": request.form["description"],
            "status": "Open",
            "created_at": datetime.datetime.now()
        })

        return redirect("/dashboard")

    return render_template("raise_ticket.html")

# ------------------- My Tickets -------------------
@app.route("/my_tickets")
def my_tickets():
    if "user" not in session:
        return redirect("/login")

    user_tickets = list(
        tickets.find({"user_id": ObjectId(session["user"])})
    )

    return render_template("my_tickets.html", tickets=user_tickets)

# ------------------- View Single Ticket -------------------
@app.route("/view_ticket/<ticket_id>")
def view_ticket(ticket_id):
    if "user" not in session:
        return redirect("/login")

    ticket = tickets.find_one({
        "_id": ObjectId(ticket_id),
        "user_id": ObjectId(session["user"])
    })

    if not ticket:
        return "Ticket not found"

    return render_template("view_ticket.html", ticket=ticket)

# ------------------- User Logout -------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =================== ADMIN SECTION ===================

# ------------------- Admin Login -------------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = admins.find_one({"username": username})

        if admin and bcrypt.check_password_hash(admin["password"], password):
            session["admin"] = username
            return redirect("/admin/dashboard")

        return "Invalid admin credentials"

    return render_template("admin_login.html")

# ------------------- Admin Dashboard -------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin/login")

    all_tickets = list(tickets.find())
    return render_template("admin_dashboard.html", tickets=all_tickets)

# ------------------- Edit Ticket Status -------------------
@app.route("/admin/edit_ticket/<ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    if "admin" not in session:
        return redirect("/admin/login")

    ticket = tickets.find_one({"_id": ObjectId(ticket_id)})

    if request.method == "POST":
        status = request.form["status"]
        tickets.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": {"status": status}}
        )
        return redirect("/admin/dashboard")

    return render_template("edit_ticket.html", ticket=ticket)

# ------------------- Admin Logout -------------------
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")

# ------------------- Run App -------------------
if __name__ == "__main__":
    print("Running on http://localhost:5000")
    app.run(debug=True, host="127.0.0.1", port=8000)
