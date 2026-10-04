import db

def get_trips():
    sql = """SELECT t.id, t.start_location, t.destination, t.travel_date,
                    t.seat_count, t.description, t.user_id, u.username
             FROM trips t, users u
             WHERE t.user_id = u.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def add_trip(start_location, destination, travel_date, seat_count,
             description, user_id, classification_ids):
    sql = """INSERT INTO trips
             (start_location, destination, travel_date, seat_count,
              description, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [start_location, destination, travel_date, seat_count,
                     description, user_id])

    trip_id = db.last_insert_id()

    sql = """INSERT INTO trip_classifications
             (trip_id, classification_id)
             VALUES (?, ?)"""

    for classification_id in classification_ids:
        db.execute(sql, [trip_id, classification_id])

    return trip_id

def get_trip(trip_id):
    sql = """SELECT t.id, t.start_location, t.destination, t.travel_date,
                    t.seat_count, t.description, t.user_id, u.username
             FROM trips t, users u
             WHERE t.user_id = u.id AND t.id = ?"""
    return db.query(sql, [trip_id])[0]

def update_trip(trip_id, start_location, destination, travel_date,
                seat_count, description, classification_ids):
    sql = """UPDATE trips
             SET start_location = ?, destination = ?, travel_date = ?,
                 seat_count = ?, description = ?
             WHERE id = ?"""
    db.execute(sql, [start_location, destination, travel_date,
                     seat_count, description, trip_id])

    sql = "DELETE FROM trip_classifications WHERE trip_id = ?"
    db.execute(sql, [trip_id])

    sql = """INSERT INTO trip_classifications
             (trip_id, classification_id)
             VALUES (?, ?)"""

    for classification_id in classification_ids:
        db.execute(sql, [trip_id, classification_id])

def remove_trip(trip_id):
    sql = "DELETE FROM trips WHERE id = ?"
    db.execute(sql, [trip_id])

def search_trips(start_location, destination, travel_date):
    sql = """SELECT t.id, t.start_location, t.destination, t.travel_date,
                    t.seat_count, t.description, t.user_id, u.username
             FROM trips t, users u
             WHERE t.user_id = u.id
               AND t.start_location LIKE ?
               AND t.destination LIKE ?
               AND t.travel_date LIKE ?
             ORDER BY t.id DESC"""
    return db.query(sql, ["%" + start_location + "%",
                          "%" + destination + "%",
                          "%" + travel_date + "%"])

def get_classifications():
    sql = """SELECT id, category, name
             FROM classifications
             ORDER BY category, id"""
    return db.query(sql)

def get_trip_classifications(trip_id):
    sql = """SELECT c.id, c.category, c.name
             FROM classifications c, trip_classifications tc
             WHERE c.id = tc.classification_id
               AND tc.trip_id = ?
             ORDER BY c.category, c.id"""
    return db.query(sql, [trip_id])