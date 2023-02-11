from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.database import User


class Register(Resource):

    @staticmethod
    # @jwt_required()
    def post() -> Response:
        login = request.json.get('login', None)
        if User.get_by_login(login):
            return jsonify(message='User already exists')
        new_user = User(**request.json)
        new_user.save_to_db()
        return jsonify(message='Successfully registered')
