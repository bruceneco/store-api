import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# create table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id int, username text, password text, PRIMARY KEY (id))")

# create some users
create_user = "INSERT INTO users VALUES (?, ?, ?)"
users = [
    (1, "bruce", "asd"),
    (2, "neco", "qwe"),
    (3, "jose", "zxc"),
]
cursor.executemany(create_user, users)

connection.commit()
connection.close()
