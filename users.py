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

def get_user_by_username(username):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if result:
        return result[0]

    return None