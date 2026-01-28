from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import os
import sqlite3


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connectioin():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        conn = get_db_connectioin()
        emails = [row["email"] for row in conn.execute("SELECT email from users").fetchall()]
        password = request.form.get("password")
        confirm_pass = request.form.get("confirm_pass")
        email = request.form.get("email")
        if email:    

            if not password or not confirm_pass:
                # conn.close()
                message = "Please Enter Both password fields"
                return render_template("signup.html", message=message)
            
            if email in emails:
                message = "Email already exists"
                return render_template("signup.html", message = message)

            if password == confirm_pass:
                message = "Successfully Signed Up"
                session["email"] = email
                conn.execute("INSERT INTO users(email, password) VALUES (?,?)", (email,password))
                conn.commit()
                conn.close()
                return render_template("index.html", message=message)
            else:
                # conn.close()
                message = "Password do not match"
                return render_template("signup.html", message=message)
    # conn.close()
    return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    conn = get_db_connectioin()
    users = [row["email"] for row in conn.execute("SELECT email FROM users").fetchall()]
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_pass = request.form.get("confirm_pass")

    if "email" in session:
        conn.close()
        return render_template("index.html", message = "Logged In")
    

    if email:
        if email and password and confirm_pass:
            if email not in users:
                return render_template("login.html", message = "User does not exist")
            if email in users:
                row = conn.execute("SELECT password from users where email = (?)", (email,)).fetchone()
                db_pass = row["password"]
                if password == db_pass and password == confirm_pass:
                    session["email"] = email
                    conn.close()
                    return render_template("index.html", message = "Logged In")
                else:
                    return render_template("login.html", message = "Incorrect Password")
        else:
            return render_template("login.html", message = "Some fields cannot be empty")

    conn.close()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/store", methods = ["GET", "POST"])
def store():
    working = int(request.form["working"])
    present = int(request.form["present"])
    subject = request.form.get("subjects")
    conn = get_db_connectioin()
    # emails = [row["email"] for row in conn.execute("SELECT email FROM users").fetchall()]

    
    if "email" not in session:
        return render_template("login.html", message = "Login To Save Your Attendance.")
    row = conn.execute("SELECT email FROM users WHERE email = ?", (session["email"],)).fetchone()
    email = row["email"]
    rows = conn.execute("SELECT id from users where email = ?", (session["email"],)).fetchone()
    student_id = rows["id"]
    rows = conn.execute("SELECT student_id, subject FROM attendance").fetchall()
    subjects = [row["subject"] for row in rows]
    conn.close()
    ids = [row["student_id"] for row in rows]
    if email:
        if subject in subjects and student_id in ids:
            conn = get_db_connectioin()
            query = """
            UPDATE attendance SET present = ?, working = ? WHERE student_id = ? AND subject = ?
            """
            conn.execute(query,(present,working, student_id, subject))
            conn.commit()
            conn.close()
        else:
            conn = get_db_connectioin()
            query = """
            INSERT INTO attendance(student_id, subject, present, working)
            VALUES (?, ?, ?, ?)
            """
            conn.execute(query,(student_id, subject, present, working))
            conn.commit()
            conn.close()
        return render_template("index.html", message = "Logged In")

if __name__ == "__main__":
    app.run(port = 5500, host = '0.0.0.0', debug = True)
