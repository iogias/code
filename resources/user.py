from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        try:
            user.delete_from_db()
        except SystemError as e:
            return {"message": "Error deleting data {}".format(e)}, 500

        return {"message": "Item deleted"}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This can not be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This can not be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data["username"], data["password"])
        user.save_to_db()

        return {"message": "OK"}, 201
