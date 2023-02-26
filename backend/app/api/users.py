import json
from typing import final

from flask import request, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.database import User
from .auxiliary import post_request, get_request
from backend.app.database.user import Role


class Users(Resource):
    route: final(str) = '/users'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        return Response(json.dumps([user.to_json() for user in User.get_all_users()]), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        login = request.json.get('login')
        user = User.get_by_login(login)
        if user is not None:
            user.update(request.json)
            return Response(json.dumps({'message': 'Successfully updated'}), 200)
        new_user = User(**request.json)
        new_user.save_to_db()
        return Response(json.dumps({'message': 'Successfully registered'}), 201)
