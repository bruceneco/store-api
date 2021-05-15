import sqlite3
from flask_restful import Resource, reqparse


class User:
    """User entity representation."""

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """
        Gets user using its unique username.

        Parameters:
            username(str): unique username to be searched
        Returns:
            User instance of found user, or None if nothing was find.
        """
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
        """
        Gets user using its unique username.

        Parameters:
            _id(int): unique id to be searched
        Returns:
            User instance of found user, or None if nothing was find.
        """
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
    """User registration resource."""
    parser = reqparse.RequestParser()
    parser.add_argument(name="username", required=True, type=str, help="Username field must me filled.")
    parser.add_argument(name="password", required=True, type=str, help="Password field must me filled.")

    def post(self):
        """
        Creates a user with data passed in request body.

        Returns:
            dict with message if user was created or if username already exists.
        """
        data = self.parser.parse_args()

        if User.find_by_username(data["username"]):
            return {"message": "User already exists."}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (data["username"], data["password"]))

        connection.commit()
        connection.close()
        return {"message": "User created."}, 201
