import sqlite3
from flask_login import UserMixin

# ✅ Define User class
class User(UserMixin):
    def __init__(self, id, username, password,age, gender, phoneno, adress):
        self.id = id
        self.username = username
        self.password = password
        self.age = age
        self.gender=gender
        self.phoneno=phoneno
        self.adress=adress

# ✅ Load user by ID
def get_user_by_id(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# ✅ Load user by username
def get_user_by_username(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# ✅ Add new user
def add_user(username, password,age,gender,phoneno,adress):
    conn = sqlite3.connect("users.db")
    conn.execute("INSERT INTO users (username, password, age,gender, phoneno, adress) VALUES (?, ?, ?, ?, ?, ?)", (username, password,age,gender,phoneno,adress))
    conn.commit()
    conn.close()
