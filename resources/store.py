from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("description", type=str)

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "OK", "data": store.json()}
        return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "Name {} already exists".format(name)}, 400
        data = Store.parser.parse_args()
        store = StoreModel(name, **data)
        try:
            store.save_to_db()
        except SystemError as e:
            return {"message": "Error inserting data {}".format(e)}, 500

        return {"message": "OK", "data": store.json()}, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": "Store {} not found".format(name)}, 404
        try:
            store.delete_from_db()
        except SystemError as e:
            return {"message": "Error deleting data {}".format(e)}, 500

        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        data = list(map(lambda x: x.json(), stores))
        return {"message": "OK", "data": data}
