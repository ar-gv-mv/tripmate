CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    start_location TEXT,
    destination TEXT,
    travel_date TEXT,
    seat_count INTEGER,
    description TEXT,
    user_id INTEGER REFERENCES users
);