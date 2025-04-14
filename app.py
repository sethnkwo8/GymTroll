from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)

# Get app configurations from config file
app.config.from_object('config')

# Activate Session
Session(app)

# Index page
@app.route("/")
def index():
