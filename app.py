from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import apology, login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from config import DB_PATH


app = Flask(__name__)

app.config.from_object('config')
Session(app)


# Eğer veritabanı dosyası yoksa schema.sql'i çalıştırarak oluştur
if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
    print("Veritabanı ve tablolar başarıyla oluşturuldu!")

@app.route("/")

def index():
    return render_template('index.html', title = 'Home')

@app.route("/about")
@login_required
def about():
    return render_template('about.html', title = "About")
#örnek olarak yazdım

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        rows = cursor.execute('SELECT * FROM users WHERE display_name = ?', (request.form.get("name"),))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        #remember which user has logged in
        session["id"] = rows[0]["id"]
        conn.close()
        return redirect("/")

    else:
        return render_template('login.html')

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        role = request.form.get("role")
        address = request.form.get("address")

        if not name:
            return apology("Please enter your username")
        elif not email:
            return apology("Please enter your email")
        elif not password:
            return apology("Please enter your password")
        elif not confirmation:
            return apology("Please enter your confirmation")
        elif password != confirmation:
            return apology("Password and Confirm must be equal")

        if role == 'organization' and not address:
            return apology("Address information is mandatory for organizations")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM users WHERE display_name = ?',(name,))
        rows = cursor.fetchall()

        if len(rows) > 0:
            return apology("This username is taken")

        hash_value = generate_password_hash(password)

        cursor.execute('INSERT INTO users(display_name, email, password_hash, address, role) VALUES (?,?,?,?,?)', (name, email, hash_value, address, role))
        conn.commit()
        conn.close()

        return redirect("/login")
    else:
        return render_template('register.html')

    

@app.route("/register-org", methods = ["GET", "POST"])
def registerorg():
    return render_template('register_org.html')

@app.route("/explore", methods = ["GET", "POST"])
def explore():
    return render_template('exploremeal.html')

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    return render_template('profile.html')

@app.route("/my-reservations", methods = ["GET", "POST"])
def myreservations():
    return render_template('my_reservations.html')

@app.route("/details", methods = ["GET", "POST"])
def details():
    return render_template('listing_detail.html')


if __name__ == "__main__":
    app.run(debug=True)

