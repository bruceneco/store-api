import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left empty!")

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        item = cursor.execute("SELECT * FROM items WHERE name=?", (name,))
        item = item.fetchone()

        connection.close()

        if item:
            return {"item": {"name": item[0], "price": item[1]}}
        return {"message": "Item not found."}, 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name {name} aready exists."}, 400
        req_data = self.parser.parse_args()
        item = {"name": name, "price": req_data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = next(filter(lambda x: x["name"] != name, items), None)
        return {"message": "Item deleted"}

    def put(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        req_data = self.parser.parse_args()
        if item:
            item.update(req_data)
        else:
            item = {"name": name, "price": req_data["price"]}
            items.append(item)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}
