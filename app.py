import sqlite3
from flask import Flask, abort
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import trips
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def get_selected_classifications():
    styles = request.form.getlist("style")
    preferences = request.form.getlist("preference")

    if len(styles) != 1:
        return None

    if len(preferences) != len(set(preferences)):
        return None

    options = trips.get_classifications()

    allowed_styles = {
        str(option["id"]) for option in options
        if option["category"] == "style"
    }
    allowed_preferences = {
        str(option["id"]) for option in options
        if option["category"] == "preference"
    }

    if styles[0] not in allowed_styles:
        return None

    if not set(preferences).issubset(allowed_preferences):
        return None

    return [int(value) for value in styles + preferences]

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

    if not username or len(username) >50:
        return "ERROR: invalid username"
    if not password1:
        return "ERROR: password cannot be empty"

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
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/new_trip")
def new_trip():
    if "user_id" not in session:
        return redirect("/")

    classifications = trips.get_classifications()
    return render_template("new_trip.html", classifications=classifications)

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

    classification_ids = get_selected_classifications()
    if classification_ids is None:
        return "ERROR: invalid trip classifications", 400

    trips.add_trip(
        start_location,
        destination,
        travel_date,
        seat_count,
        description,
        user_id,
        classification_ids
    )
    return redirect("/")

@app.route("/trip/<int:trip_id>")
def show_trip(trip_id):
    trip = trips.get_trip(trip_id)
    selected = trips.get_trip_classifications(trip_id)
    style = "Not specified"
    preferences = []

    for item in selected:
        if item["category"] == "style":
            style = item["name"]
        if item["category"] == "preference":
            preferences.append(item["name"])

    return render_template("trip.html", trip=trip, style=style, preferences=preferences)

@app.route("/edit_trip/<int:trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):
    trip = trips.get_trip(trip_id)

    if "user_id" not in session:
        return redirect("/")

    if trip["user_id"] != session["user_id"]:
        return "ERROR: access denied"

    if request.method == "GET":
        classifications = trips.get_classifications()
        selected = trips.get_trip_classifications(trip_id)
        selected_ids = [item["id"] for item in selected]

        return render_template(
            "edit_trip.html",
            trip=trip,
            classifications=classifications,
            selected_ids=selected_ids
        )

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

        classification_ids = get_selected_classifications()
        if classification_ids is None:
            return "ERROR: invalid trip classifications", 400

        trips.update_trip(
            trip["id"],
            start_location,
            destination,
            travel_date,
            seat_count,
            description,
            classification_ids
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

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    if request.method == "POST":
        start_location = request.form["start_location"]
        destination = request.form["destination"]
        travel_date = request.form["travel_date"]

        results = trips.search_trips(
            start_location,
            destination,
            travel_date
        )
        return render_template("search.html", results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    user_trips = users.get_user_trips(user_id)
    trip_count = len(user_trips)

    return render_template("user.html", user=user, trips=user_trips, trip_count=trip_count)
