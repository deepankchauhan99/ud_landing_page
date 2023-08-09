import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

def connect_db():
    return sqlite3.connect('underdogs-clothing.db') 


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# db = SQL(os.getenv("DATABASE_URL"))


@app.route("/", methods=["GET","POST"])
def index():

    if request.methods == "POST":
        # Take values from the form
        email = request.form['email']
        location = request.form['location']
        status = 'active'

        # Connect to the database
        connection = connect_db()
        cursor = connection.cursor()

        # Insert data into the 'subscriber' table
        cursor.execute("INSERT INTO subscriber (email, location, status) VALUES (?, ?, ?)",
                   (email, location, status))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("index.html")
