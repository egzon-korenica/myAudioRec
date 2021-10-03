import sqlite3

conn = sqlite3.connect('qdas/site.db')

print("Opened database successfully");

cursor = conn.cursor()
#cursor.execute("SELECT q1, q2, q3 FROM Questions ")
cursor.execute("CREATE TABLE contacts (\
	contact_id INTEGER PRIMARY KEY,\
	first_name TEXT NOT NULL,\
	last_name TEXT NOT NULL,\
	email TEXT NOT NULL UNIQUE,\
	phone TEXT NOT NULL UNIQUE\
);")

rows = cursor.fetchall()
