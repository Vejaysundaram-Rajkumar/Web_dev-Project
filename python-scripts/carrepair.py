import sqlite3

conn = sqlite3.connect('customers.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS carrepair (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
 customername TEXT NOT NULL,
 carname TEXT NOT NULL,
  desc TEXT NOT NULL,
  kmdriven INTEGER DEFAULT 0,
  phone INTEGER NOT NULL
)
''')

conn.commit()
conn.close()