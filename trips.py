import db

def get_trips():
    sql = """SELECT t.id, t.start_location, t.destination, t.travel_date,
                    t.seat_count, t.description, t.user_id, u.username
             FROM trips t, users u
             WHERE t.user_id = u.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def add_trip(start_location, destination, travel_date, seat_count,
             description, user_id):
    sql = """INSERT INTO trips
             (start_location, destination, travel_date, seat_count,
              description, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [start_location, destination, travel_date, seat_count,
                     description, user_id])

def get_trip(trip_id):
    sql = """SELECT t.id, t.start_location, t.destination, t.travel_date,
                    t.seat_count, t.description, t.user_id, u.username
             FROM trips t, users u
             WHERE t.user_id = u.id AND t.id = ?"""
    return db.query(sql, [trip_id])[0]

def update_trip(trip_id, start_location, destination, travel_date,
                seat_count, description):
    sql = """UPDATE trips
             SET start_location = ?, destination = ?, travel_date = ?,
                 seat_count = ?, description = ?
             WHERE id = ?"""
    db.execute(sql, [start_location, destination, travel_date,
                     seat_count, description, trip_id])

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