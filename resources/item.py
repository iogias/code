from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Price can not be blank"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Store ID can not be blank"
    )

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "OK", "data": item.json()}
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except SystemError as e:
            return {"message": "Error inserting data {}".format(e)}, 500

        return {"message": "OK", "data": item.json()}, 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {"message": "Item {} not found".format(name)}, 404
        try:
            item.delete_from_db()
        except SystemError as e:
            return {"message": "Error deleting data {}".format(e)}, 500

        return {"message": "Item deleted"}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return {"message": "OK", "data": item.json()}


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        data = list(map(lambda x: x.json(), items))
        return {"message": "OK", "data": data}
