import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'your-secret-key'

# Configure Flask-Mail
app.config['MAIL_SERVER']='smtpout.secureserver.net'
app.config['MAIL_PORT'] = 80
app.config['MAIL_DEFAULT_SENDER'] = 'support@underdogs-clothing.com'#os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USERNAME'] = 'support@underdogs-clothing.com'#os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = 'Ud@02072023$'#os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


def connect_db():
    return sqlite3.connect('underdogs-clothing.db') 


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":
        # Take values from the form
        email = request.form.get("email")
        status = 'active'

        print(email)
        # Connect to the database
        connection = connect_db()
        cursor = connection.cursor()

        # Check if a subscriber with the same email already exists
        cursor.execute("SELECT id FROM subscriber WHERE email = ?", (email,))
        existing_subscriber = cursor.fetchone()

        if existing_subscriber:
            # Handle case when subscriber with the same email already exists
            # You can choose to update the status or perform any other action here
            flash("This email address is already subscribed.")
        else:
            # Insert data into the 'subscriber' table
            cursor.execute("INSERT INTO subscriber (email, status) VALUES (?, ?)",
                        (email, status))
            flash("Subscribed!")
            # Sending email
            msg = Message(
            'You have successfully subscribed!',
            sender = ('Underdogs Clothing', 'support@underdogs-clothing.com'), #os.getenv('MAIL_USERNAME')),
            recipients = [email]
            )
            msg.body = "Dear " + email + "!\nThank you for showing interest in our latest brand. We will keep you updated on our big launch.\nDo not worry we will not spam you.\nThank you\nTeam Underdogs Clothing"
            mail.send(msg)

        # Insert data into the 'subscriber' table
        # cursor.execute("INSERT INTO subscriber (email, status) VALUES (?, ?)",
        #            (email, status))

        # Commit the changes and close the connection
        connection.commit()
        connection.close()
        

        
        return redirect("/")
    # flash("Not registered!")
        
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)