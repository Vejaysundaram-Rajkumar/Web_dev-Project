import sqlite3

conn = sqlite3.connect('customers.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  verification INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
