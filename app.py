from bcrypt import gensalt, checkpw, hashpw # For hashing passwords
import sqlite3

from datetime import timedelta # For session lifetime
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from functools import wraps # For login decorator


app = Flask(__name__)

# Get app configurations from config file
app.config.from_object('config')

# Set the session lifetime to 2 hours
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

# Activate Session
Session(app)

# Decorator for login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Get database connection
def get_db_connection():
    connection = sqlite3.connect("gymtroll.db")
    connection.row_factory = sqlite3.Row
    return connection

# Disables browser caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Helper function for password hashing
def gen_password_hash(input):
    if not input:
        return render_template("error.html", code = 403, message = "Please enter a Password")
    # Ensure the input is encoded to bytes
    password = input.encode('utf-8') if isinstance(input, str) else input

    # Generate salt and hash the password
    salt = gensalt()
    hashed = hashpw(password, salt)
    return hashed

# Index page
@app.route("/")
def index():
    return render_template("index.html")

# Log in route
@app.route("/login", methods = ["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # Get username and password from form
    username = request.form.get("username")
    password = request.form.get("password")

    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor()
    if request.method == "POST":
        #  Validate form inputs
        if not username:
            return render_template("error.html", code = 403, message = "Please enter your username")
        elif not password:
            return render_template("error.html", code = 403, message = "Please enter your Password")
        
        # Query database for user
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        #  Check if user exists and passwords match
        if len(rows) != 1 or not checkpw(password.encode('utf-8'), rows[0]["password"]):
            return render_template("error.html", code = 403, message = "Invalid username and/or password")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/")
    
    else:
        return render_template("login.html")

# Register route
@app.route("/register", methods = ["GET", "POST"])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    hashed_password = gen_password_hash(password)
    connect = get_db_connection()
    cursor = connect.cursor()

    if request.method == "POST":
        # Validate form inputs
        if not first_name or not last_name:
            return render_template("error.html", code = 403, message = "Please enter your name")
        elif not username:
            return render_template("error.html", code = 403, message = "Please enter a username")
        elif not password:
            return render_template("error.html", code = 403, message = "Please enter a Password")
        elif not confirm:
            return render_template("error.html", code = 403, message = "Please Confrim Password")
        elif confirm != password:
            return render_template("error.html", code = 403, message = "Passwords don't match")
        
        # Checks if username exists
        rows = cursor.execute("SELECT username FROM users").fetchall()
        if any(row["username"] == username for row in rows):
            return render_template("error.html", code = 403, message = "Username already exists")
        
        # Insert user data into database
        cursor.execute("INSERT INTO users(first_name, last_name, username, password) VALUES(?,?,?,?)", (first_name , last_name, username, hashed_password))
        connect.commit()
        connect.close()
        return redirect("/login")

    # Display register page
    return render_template("register.html")

# Log out route
@app.route("/logout")
@login_required
def logout():
    # Clear session
    session.clear()

    # Redirect to homepage
    return redirect("/")

@app.route("/plan")
@login_required
def plan():

    return render_template("plan1.html")