from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authentication, identity

app = Flask(__name__)
app.secret_key = "bruce"
api = Api(app)

jwt = JWT(app, authentication, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True, help="This field cannot be left empty!")


    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

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


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run()
