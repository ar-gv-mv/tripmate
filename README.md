# TripMate

The application helps users find travel companions for trips, e.g. when someone needs to get from Helsinki to Tampere.

* Users can create an account and log in.
* Users can create trip posts and edit or delete their own posts.
* A trip post contains the starting location, destination, date, number of available seats and a description of the trip.
* Users can browse trips created by other users.
* Users can search for trips by starting location, destination and date.
* The user page shows the number of trips created by the user and lists their trips.
* Trips can be classified, for example, by transportation type and travel style.
* Users can join trips created by other users.
* A trip page shows the users who have joined the trip.

## Installation

Clone the repository:

```bash
git clone https://github.com/ar-gv-mv/tripmate.git
cd tripmate
```

Create a virtual environment:

`python3 -m venv venv`

Activate the virtual environment:

`source venv/bin/activate`

Install Flask:

`pip install flask`

Create the database:

`sqlite3 database.db < schema.sql`

Start the application:

`flask run`

Open the application in your browser:

`http://127.0.0.1:5000`