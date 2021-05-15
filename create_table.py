import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create user table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)")

# create some users
create_user = "INSERT INTO users VALUES (?, ?, ?)"
users = [
    (1, "bruce", "asd"),
    (2, "neco", "qwe"),
    (3, "jose", "zxc"),
]
cursor.executemany(create_user, users)

# create item table
cursor.execute("CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)")

# create test item
cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()
connection.close()
