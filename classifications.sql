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