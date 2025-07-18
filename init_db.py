import sqlite3

conn = sqlite3.connect("users.db")

conn.execute('''
DROP TABLE users
             ''')
conn.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    age NUMBER,
    gender TEXT,
    phoneno NUMBER,
    adress TEXT       
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS health_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    temperature REAL,
    heart_rate INTEGER,
    spo2 INTEGER,
    ecg TEXT,
    label TEXT, 
    disease TEXT, 
    cause TEXT, 
    symptoms TEXT, 
    solution TEXT, 
    treatment TEXT
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')


conn.close()
print("Database initialized.")
