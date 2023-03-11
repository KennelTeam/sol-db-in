from typing import Final

from flask import jsonify, Response
from flask_jwt_extended import unset_jwt_cookies
from flask_restful import Resource


class Logout(Resource):
    route: Final[str] = '/logout'

    @staticmethod
    def post() -> Response:
        response = jsonify(message='Logout successful')
        unset_jwt_cookies(response)
        return response
