import json
from typing import Final

from flask import request, Response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource, reqparse

from backend.app.api.auxiliary import get_failure, HTTPErrorCode
from backend.app.database import User
from backend.constants import DEFAULT_LANGUAGE


class Login(Resource):
    route: Final[str] = '/login'

    @staticmethod
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        parser.add_argument('language', type=str, location='json', required=False, default=DEFAULT_LANGUAGE)
        arguments = parser.parse_args()

        user = User.get_by_login(arguments['login'])
        if not user:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)

        user = user.auth(arguments['login'], arguments['password'])
        if not user:
            return get_failure(HTTPErrorCode.WRONG_ID, 403)

        user.current_ip = request.remote_addr
        user.selected_language = arguments['language']
        access_token = create_access_token(identity=user)
        response = Response(json.dumps({'role': user.role.name}), 200)
        set_access_cookies(response, access_token)
        return response
