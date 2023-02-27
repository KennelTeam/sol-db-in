import json
from typing import final

from flask import request, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.database import User
from .auxiliary import post_request, get_request, post_failure, HTTPErrorCode
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
        if login is None:
            return post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        if User.get_by_login(login) is not None:
            return post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
        new_user = User(**request.json)
        new_user.save_to_db()
        return Response(json.dumps({'message': 'Successfully registered'}), 201)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def patch() -> Response:
        user_id = request.json.get('id')
        if user_id is None:
            return post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        user = User.get_by_id(user_id)
        if user is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)
        new_login = request.json.get('login')
        new_name = request.json.get('name')
        new_comment = request.json.get('comment')
        new_password = request.json.get('password')
        if new_password is not None and user.check_password(new_password):
            new_password = None
        new_role = request.json.get('role')
        if new_role is not None:
            new_role = Role[new_role]
        user.update(login=new_login, name=new_name, comment=new_comment, password=new_password, role=new_role)
        return Response(json.dumps({'message': 'Successfully updated'}), 200)
