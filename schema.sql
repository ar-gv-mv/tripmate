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
CREATE TABLE classifications (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(category, name)
);
CREATE TABLE trip_classifications (
    trip_id INTEGER NOT NULL REFERENCES trips ON DELETE CASCADE,
    classification_id INTEGER NOT NULL REFERENCES classifications,
    PRIMARY KEY (trip_id, classification_id)
);
INSERT INTO classifications (category, name) VALUES
    ('style', 'Quiet'),
    ('style', 'Social'),
    ('preference', 'Pets allowed'),
    ('preference', 'Large luggage allowed'),
    ('preference', 'Music allowed');
CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    UNIQUE(trip_id, user_id)
);