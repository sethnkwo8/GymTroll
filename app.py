import sqlite3
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import bcrypt #For hashing passwords

app = Flask(__name__)

# Get app configurations from config file
app.config.from_object('config')

# Activate Session
Session(app)

# Get database connection
def get_db_connection():
    connection = sqlite3.connect("gymtroll.db")
    connection.row_factory = sqlite3.Row
    return connection

# Helper function for password hashing
def gen_password_hash(input):
    if not input:
        return render_template("error.html", code = 403, message = "Please enter a Password")
    # Ensure the input is encoded to bytes
    password = input.encode('utf-8') if isinstance(input, str) else input

    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed

# Index page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # if request.method == "POST":
    #     if not username:

        
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    hashed_password = gen_password_hash(password)
    connect = get_db_connection()
    cursor = connect.cursor()

    if request.method == "POST":
        # Validate form inputs
        if not username:
            return render_template("error.html", code = 403, message = "Please enter a username")
        if not password:
            return render_template("error.html", code = 403, message = "Please enter a Password")
        if not confirm:
            return render_template("error.html", code = 403, message = "Please Confrim Password")
        if confirm != password:
            return render_template("error.html", code = 403, message = "Passwords don't match")
        
        # Checks if username exists
        rows = cursor.execute("SELECT username FROM users").fetchall()
        if any(row["username"] == username for row in rows):
            return render_template("error.html", code = 403, message = "Username already exists")
        
        
        cursor.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, hashed_password))
        connect.commit()
        connect.close()
        return redirect("/login")

    return render_template("register.html")