import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if result:
        return result[0]
    return None

def get_user_trips(user_id):
    sql = """SELECT id, start_location, destination, travel_date
             FROM trips
             WHERE user_id = ?
             ORDER BY id DESC"""
    return db.query(sql, [user_id])