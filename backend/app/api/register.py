from typing import final

from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.database import User


class Register(Resource):
    route: final(str) = '/register'

    @staticmethod
    @jwt_required()
    def post() -> Response:
        login = request.json.get('login')
        if User.get_by_login(login):
            response = jsonify(message='User already exists')
            response.status_code = 304
            return response
        new_user = User(**request.json)
        new_user.save_to_db()
        response = jsonify(message='Successfully registered')
        response.status_code = 201
        return response
