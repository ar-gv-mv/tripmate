import db
import sqlite3

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

def get_participants(trip_id):
    sql = """SELECT u.id, u.username
             FROM participants p, users u
             WHERE p.user_id = u.id AND p.trip_id = ?
             ORDER BY p.id"""
    return db.query(sql, [trip_id])

def add_participant(trip_id, user_id):
    sql = "SELECT id, user_id FROM trips WHERE id = ?"
    result = db.query(sql, [trip_id])

    if not result:
        return "not_found"

    trip = result[0]

    if trip["user_id"] == user_id:
        return "own_trip"

    sql = """SELECT id FROM participants
             WHERE trip_id = ? AND user_id = ?"""
    if db.query(sql, [trip_id, user_id]):
        return "already_joined"

    sql = """INSERT INTO participants (trip_id, user_id)
             SELECT t.id, ?
             FROM trips t
             WHERE t.id = ?
               AND t.user_id != ?
               AND (SELECT COUNT(*)
                    FROM participants p
                    WHERE p.trip_id = t.id) < t.seat_count
               AND NOT EXISTS
                   (SELECT 1 FROM participants p
                    WHERE p.trip_id = t.id AND p.user_id = ?)"""

    try:
        db.execute(sql, [user_id, trip_id, user_id, user_id])
    except sqlite3.IntegrityError:
        return "already_joined"

    sql = """SELECT id FROM participants
             WHERE trip_id = ? AND user_id = ?"""

    if db.query(sql, [trip_id, user_id]):
        return "joined"

    return "full"