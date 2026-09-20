import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import trips

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_trips = trips.get_trips()
    return render_template("index.html", trips=all_trips)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "ERROR: passwords are not the same"

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username is already taken"

    return "Account created"

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if not result:
        return "ERROR: wrong username or password"

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "ERROR: wrong username or password"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/new_trip")
def new_trip():
    if "user_id" not in session:
        return redirect("/")

    return render_template("new_trip.html")

@app.route("/create_trip", methods=["POST"])
def create_trip():
    if "user_id" not in session:
        return redirect("/")

    start_location = request.form["start_location"]
    destination = request.form["destination"]
    travel_date = request.form["travel_date"]
    seat_count = request.form["seat_count"]
    description = request.form["description"]
    user_id = session["user_id"]

    if not start_location or len(start_location) > 100:
        return "ERROR: invalid starting location"

    if not destination or len(destination) > 100:
        return "ERROR: invalid destination"

    if not travel_date:
        return "ERROR: invalid date"

    if not seat_count.isdigit():
        return "ERROR: invalid number of seats"

    seat_count = int(seat_count)

    if seat_count < 1 or seat_count > 100:
        return "ERROR: invalid number of seats"

    if len(description) > 1000:
        return "ERROR: description is too long"

    trips.add_trip(
        start_location,
        destination,
        travel_date,
        seat_count,
        description,
        user_id
    )
    return redirect("/")

@app.route("/trip/<int:trip_id>")
def show_trip(trip_id):
    trip = trips.get_trip(trip_id)
    return render_template("trip.html", trip=trip)

@app.route("/edit_trip/<int:trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):
    trip = trips.get_trip(trip_id)

    if "user_id" not in session:
        return redirect("/")

    if trip["user_id"] != session["user_id"]:
        return "ERROR: access denied"

    if request.method == "GET":
        return render_template("edit_trip.html", trip=trip)

    if request.method == "POST":
        start_location = request.form["start_location"]
        destination = request.form["destination"]
        travel_date = request.form["travel_date"]
        seat_count = request.form["seat_count"]
        description = request.form["description"]

        if not start_location or len(start_location) > 100:
            return "ERROR: invalid starting location"

        if not destination or len(destination) > 100:
            return "ERROR: invalid destination"

        if not travel_date:
            return "ERROR: invalid date"

        if not seat_count.isdigit():
            return "ERROR: invalid number of seats"

        seat_count = int(seat_count)

        if seat_count < 1 or seat_count > 100:
            return "ERROR: invalid number of seats"

        if len(description) > 1000:
            return "ERROR: description is too long"

        trips.update_trip(
            trip["id"],
            start_location,
            destination,
            travel_date,
            seat_count,
            description
        )

        return redirect("/trip/" + str(trip["id"]))

@app.route("/remove_trip/<int:trip_id>", methods=["GET", "POST"])
def remove_trip(trip_id):
    trip = trips.get_trip(trip_id)

    if "user_id" not in session:
        return redirect("/")

    if trip["user_id"] != session["user_id"]:
        return "ERROR: access denied"

    if request.method == "GET":
        return render_template("remove_trip.html", trip=trip)

    if request.method == "POST":
        if "continue" in request.form:
            trips.remove_trip(trip["id"])

        return redirect("/")