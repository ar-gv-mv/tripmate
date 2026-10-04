CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER REFERENCES trips ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    UNIQUE(trip_id, user_id)
);