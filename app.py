from bcrypt import gensalt, checkpw, hashpw # For hashing passwords
import sqlite3
import smtplib
from email.mime.text import MIMEText

from datetime import timedelta # For session lifetime
from flask import Flask, render_template, redirect, request, session, flash
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

        cursor.execute(
    "SELECT last_workout_plan FROM user_details WHERE username = ?",
    (session["username"],)
    )
        row = cursor.fetchone()
        if row and row["last_workout_plan"]:
            session["workout_plan"] = row["last_workout_plan"]
        else:
            session["workout_plan"] = None

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

@app.route("/plan", methods=["GET", "POST"])
@login_required
def plan():
    if request.method == "POST":

        # Step 1: Goal Selection
        if "card-input" in request.form:
            goal = request.form.get("card-input")
            if not goal:
                return render_template("error.html", code=400, message="Please select a goal.")
            session["goal"] = goal

            return redirect("/plan")

        # Step 2: Split Selection
        if "split" in request.form:
            split = request.form.get("split")
            if not split:
                return render_template("error.html", code=400, message="Please select a workout split.")
            session["split"] = split

            return redirect("/plan")

        # Step 3: Current Weight
        if "current-weight" in request.form:
            current_weight = request.form.get("current-weight")
            if not current_weight or not current_weight.isdigit() or int(current_weight) < 30 or int(current_weight) > 250:
                return render_template("error.html", code=400, message="Please enter a valid current weight (30-250 kg).")
            session["current_weight"] = current_weight  # Save current weight to session

            return redirect("/plan")  # Redirect to the next step

        # Step 4: Desired Weight
        if "desired-weight" in request.form:
            desired_weight = request.form.get("desired-weight")
            if not desired_weight or not desired_weight.isdigit() or int(desired_weight) < 30 or int(desired_weight) > 250:
                return render_template("error.html", code=400, message="Please enter a valid desired weight (30-250 kg).")
            session["desired_weight"] = desired_weight  # Save desired weight to session

            return redirect("/plan")  # Redirect to the next step

        # Step 5: Workout Preference
        if "card-input-workout" in request.form:
            workout = request.form.get("card-input-workout")
            if not workout:
                return render_template("error.html", code=400, message="Please select where you prefer to work out.")
            session["workout"] = workout  # Save workout preference to session

            # Check if user already submitted a plan this session
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM user_details WHERE username = ?",
                (session["username"],)
            )
            existing = cursor.fetchone()
            if existing:
                connection.close()
                return render_template("error.html", code=400, message="You have already submitted your plan for this session.")

            # Save all data to the database
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO user_details (username, goal, days_split, weight_kg, desired_weight, workout_type) VALUES (?,?,?,?,?,?)",
                (session["username"], session["goal"], session["split"], session["current_weight"], session["desired_weight"], session["workout"])
            )
            connection.commit()
            connection.close()

            
            # After inserting the new plan in /plan route, before redirecting to /final_plan
            goal = session.get("goal")
            if goal == "weight-loss":
                goal = "weight loss"
            split = int(session.get("split"))
            current_weight = session.get("current_weight")
            desired_weight = session.get("desired_weight")
            workout = session.get("workout")
            
            if int(current_weight) > int(desired_weight):
                weight_change = "decrease"
            else:
                weight_change = "increase"
                
            if workout == "home-workout":
                environment = "home"
            else:
                environment = "gym"

            if goal == "weight loss":
                if int(current_weight) < int(desired_weight):
                    return render_template("error.html", code=400, message="Your desired weight can't be more than your current weight during weight loss")
                
            if goal == "bulking":
                if int(current_weight) > int(desired_weight):
                    return render_template("error.html", code=400, message="Your desired weight can't be less than your current weight during bulking")

            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT workout_plan FROM workout_plans
                WHERE goal = ?
                AND split = ?
                AND environment = ?
                AND weight_change = ?
                """,
                (goal, split, environment, weight_change)
            )
            plan_row = cursor.fetchone()
            if plan_row:
                generated_plan = plan_row["workout_plan"]
            else:
                generated_plan = "No plan found for your selection."

            # Update the last_workout_plan column for this user
            cursor.execute(
                "UPDATE user_details SET last_workout_plan = ? WHERE username = ?",
                (generated_plan, session["username"])
            )
            connection.commit()
            connection.close()

            return redirect('/final_plan')

    # Render the appropriate step based on session data
    if "goal" not in session:
        return render_template("plan.html", step="goal")
    elif "split" not in session:
        return render_template("plan.html", step="split")
    elif "current_weight" not in session:
        return render_template("plan.html", step="current_weight")
    elif "desired_weight" not in session:
        return render_template("plan.html", step="desired_weight")
    elif "workout" not in session:
        return render_template("plan.html", step="workout")
    
    return redirect("/final_plan")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        user_email = request.form.get("user_email")
        title = request.form.get("title")
        message = request.form.get("message")

        # Compose email
        full_message = f"Message from: {user_email}\n\n{message}"
        msg = MIMEText(full_message)
        msg["Subject"] = title
        msg["From"] = "sethnkwocool@gmail.com"  # Your email 
        msg["To"] = "sethnkwocool@gmail.com"    # Your email
        msg["Reply-To"] = user_email            # User's email for reply

        # Send email (using Gmail SMTP as example)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("sethnkwocool@gmail.com", "your_app_password")
                server.send_message(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash("Failed to send message: " + str(e), "danger")

        return redirect("/contact")
    return render_template("contact.html")

@app.route("/final_plan")
@login_required
def final_plan():
    connect = get_db_connection()
    cursor = connect.cursor()

    cursor.execute(
        "SELECT last_workout_plan FROM user_details WHERE username = ?",
        (session["username"],)
    )
    row = cursor.fetchone()
    workout_plan = row["last_workout_plan"] if row and row["last_workout_plan"] else None
    session["workout_plan"] = workout_plan
    return render_template("final_plan.html", workout_plan=workout_plan)

@app.route("/cancel_plan")
@login_required
def cancel_plan():
    connect = get_db_connection()
    cursor = connect.cursor()
    cursor.execute(
        "DELETE FROM user_details WHERE username = ?",
        (session["username"],)
    )
    connect.commit()
    connect.close()
    for key in ["workout_plan", "goal", "split", "current_weight", "desired_weight", "workout"]:
        session.pop(key, None)
    return redirect("/")

@app.route("/workout_library")
@login_required
def workout_library():

    return render_template('workout_library.html')

@app.route("/bmi_calculator", methods=["GET", "POST"])
@login_required
def bmi_calculator():
    if request.method == "POST":
        weight = request.form.get("weight")
        height = request.form.get("height")
        age = request.form.get("age")
        gender = request.form.get("gender")

        # Validate presence
        if not weight or not height:
            return render_template("error.html", code=400, message="Please enter both weight and height.")

        # Validate numeric
        try:
            weight = float(weight)
            height = float(height)
        except ValueError:
            return render_template("error.html", code=400, message="Weight and height must be numbers.")

        # Validate reasonable ranges
        if weight < 20 or weight > 300:
            return render_template("error.html", code=400, message="Please enter a valid weight (20-300 kg).")
        if height < 100 or height > 250:
            return render_template("error.html", code=400, message="Please enter a valid height (100-250 cm).")

        # Calculate BMI
        height_m = height / 100  # convert cm to meters
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        return render_template('bmi_calculator.html', bmi=bmi, weight=weight, height=height)

    return render_template('bmi_calculator.html')

@app.route("/nutrition")
@login_required
def nutrition():

    return render_template('nutrition.html')

@app.route("/start_plan")
@login_required
def start_plan():
    # Clear plan-related session variables
    for key in ["goal", "split", "current_weight", "desired_weight", "workout"]:
        session.pop(key, None)
    # Remove user row from user_details
    connection = get_db_connection()
    connection.execute("DELETE FROM user_details WHERE username = ?", (session["username"],))
    connection.commit()
    connection.close()
    return redirect("/plan")

@app.route("/plan/back/<step>")
@login_required
def plan_back(step):
    # Define the order of steps
    steps = ["goal", "split", "current_weight", "desired_weight", "workout"]
    # Map step names in URL to session keys
    step_map = {
        "goal": "goal",
        "split": "split",
        "current_weight": "current_weight",
        "desired_weight": "desired_weight",
        "workout": "workout"
    }
    # Find the index of the step to go back to
    if step in step_map:
        idx = steps.index(step_map[step])
        # Clear this step and all steps after it
        for s in steps[idx:]:
            session.pop(s, None)
    return redirect("/plan")