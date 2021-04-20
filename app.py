from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        'name': "Store One",
        'items': [
            {'name': "Wardrobe", 'price': 129.99},
            {'name': "Desk", 'price': 30},
        ]
    }
]


@app.route('/store', methods=["POST"])
def create_store():
    req_data = request.get_json()
    new_store = {
        'name': req_data['name'],
        'items': []
    }
    stores.append(new_store)
    return new_store


@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store
    return {'message': "store doesn't exist."}


@app.route('/store')
def get_stores():
    return {'stores': stores}


@app.route('/store/<string:store_name>/item', methods=['POST'])
def create_item_in_store(store_name):
    req_data = request.get_json()
    for store in stores:
        if store["name"] == store_name:
            store['items'].append(req_data)
            return req_data
    return {'message': "store doesn't exist."}


@app.route('/store/<string:store_name>/item')
def get_items_in_store(store_name):
    for store in stores:
        if store['name'] == store_name:
            return {'items': store['items']}


if __name__ == '__main__':
    app.run(debug=True)
