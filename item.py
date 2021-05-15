import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    """Representation of a store item."""
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left empty!")

    @jwt_required()
    def get(self, name):
        """
        Gets item from database with name passed in argument.

        Parameters:
            name(str): name of the item.
        Returns:
             Dict with item, or dict with message.
        """
        item = self.get_by_name(name)
        if item:
            return item
        return {"message": "Item not found."}, 404

    @classmethod
    def get_by_name(cls, name):
        """
        Gets item from database with name passed in argument.

        Parameters:
            name(str): name of the item.
        Returns:
             Dict with item, or None.
        """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        item = cursor.execute("SELECT * FROM items WHERE name=?", (name,))
        item = item.fetchone()

        connection.close()

        if item:
            return {"name": item[0], "price": item[1]}
        return None

    def post(self, name):
        """
        Creates item with passed name and price in request body.

        Parameters:
            name(str): name of the item to be created;
        Return:
            dict with item created or dict with message.
        """
        req_data = self.parser.parse_args()
        item = self.create_item(name, req_data["price"])

        if not item:
            return {"message": f"An item with name {name} aready exists."}, 400
        return item, 201

    @classmethod
    def create_item(cls, name, price):
        """
        Creates item with name and price passed.

        Parameters:
            name(str): name of the item
        Returns:
            Dict with item or None.
        """
        if cls.get_by_name(name):
            return None

        item = {"name": name, "price": price}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO items VALUES (?, ?)", (item["name"], item["price"]))

        connection.commit()
        connection.close()
        return item

    def delete(self, name):
        """
        Removes item with passed name from database.

        Parameters:
            name(str): name of the item to be deleted.
        Return:
            dict with deletion message.
        """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM items WHERE name=?", (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}

    def put(self, name):
        """
        Updates item if already exists or create on if not exists.
        In both cases, is neccessary to have a request body with price.

        Parameters:
            name(str): name of the item to be created/updated.
        Returns:
            dict of item created or updated.
        """
        req_data = self.parser.parse_args()
        item = self.create_item(name, req_data["price"])
        if not item:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            cursor.execute("UPDATE items SET price=? WHERE name=?", (req_data["price"], name))

            connection.commit()
            connection.close()
            item = {"name": name, "price": req_data["price"]}

        return item


class ItemList(Resource):
    """Representation of whole collection of items."""

    def get(self):
        """
        Gets all the items from database.

        Returns:
            dict with items inside a list.
        """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        items = cursor.execute("SELECT * FROM items")
        items = items.fetchall()

        connection.close()

        items = [{"name": item[0], "price": item[1]} for item in items]

        return {"items": items}
