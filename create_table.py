import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create user table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)")

# create item table
cursor.execute("CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)")

connection.commit()
connection.close()
