import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            user = cls(*user)
        else:
            user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE id=?", (_id,))
        user = cursor.fetchone()

        if user:
            user = cls(*user)
        else:
            user = None

        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="username", required=True, type=str, help="Username field must me filled.")
    parser.add_argument(name="password", required=True, type=str, help="Password field must me filled.")

    def post(self):
        data = self.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "User already exists."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (data["username"], data["password"]))

        connection.commit()
        connection.close()
        return {"message": "User created."}, 201
