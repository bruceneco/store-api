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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        item = cursor.execute("SELECT * FROM items WHERE name=?", (name,))
        item = item.fetchone()

        connection.close()

        if item:
            return {"item": {"name": item[0], "price": item[1]}}
        return {"message": "Item not found."}, 404

    def post(self, name):
        """
        Creates item with passed name and price in request body.

        Parameters:
            name(str): name of the item to be created;
        Return:
            dict with item created or dict with message.
        """
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name {name} aready exists."}, 400
        req_data = self.parser.parse_args()
        item = {"name": name, "price": req_data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        """
        Removes item with passed name from database.

        Parameters:
            name(str): name of the item to be deleted.
        Return:
            dict with deletion message.
        """
        global items
        items = next(filter(lambda x: x["name"] != name, items), None)
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
        item = next(filter(lambda x: x["name"] == name, items), None)
        req_data = self.parser.parse_args()
        if item:
            item.update(req_data)
        else:
            item = {"name": name, "price": req_data["price"]}
            items.append(item)
        return item


class ItemList(Resource):
    """Representation of whole collection of items."""

    def get(self):
        """
        Gets all the items from database.

        Returns:
            dict with items inside a list.
        """
        return {"items": items}
