import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrer INTEGER,
    referrals INTEGER DEFAULT 0,
    unlocked INTEGER DEFAULT 0
)
""")
conn.commit()
