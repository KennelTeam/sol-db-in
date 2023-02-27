import json
from typing import final

from flask import request, Response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource

from backend.app.api.auxiliary import get_failure, HTTPErrorCode
from backend.app.database import User


class Login(Resource):
    route: final(str) = '/login'

    @staticmethod
    def post() -> Response:
        login = request.json.get('login')
        password = request.json.get('password')
        if not login or not password:
            return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)

        user = User.get_by_login(login)
        if not user:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)

        user = user.auth(login, password)
        if not user:
            return get_failure(HTTPErrorCode.WRONG_ID, 403)

        user.current_ip = request.remote_addr
        access_token = create_access_token(identity=user)
        response = Response(json.dumps({'role': user.role.name}), 200)
        set_access_cookies(response, access_token)
        return response
