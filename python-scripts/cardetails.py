import sqlite3

conn = sqlite3.connect('customers.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cardetails (
  id INTEGER PRIMARY KEY ,
 customername TEXT NOT NULL,
  carname TEXT NOT NULL,
   yearsold INTEGER NOT NULL,
  kmdriven INTEGER DEFAULT 0,
  price INTEGER NOT NULL
)
''')

conn.commit()
conn.close()