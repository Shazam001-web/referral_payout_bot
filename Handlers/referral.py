from database import cursor, conn

def register_user(user_id, referrer):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if cursor.fetchone():
        return

    cursor.execute(
        "INSERT INTO users (user_id, referrer) VALUES (?, ?)",
        (user_id, referrer)
    )

    if referrer and referrer != user_id:
        cursor.execute(
            "UPDATE users SET referrals = referrals + 1 WHERE user_id=?",
            (referrer,)
        )
    conn.commit()

def get_user(user_id):
    cursor.execute(
        "SELECT referrals, unlocked FROM users WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchone()
