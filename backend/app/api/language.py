from typing import final
from flask import Response
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, reqparse


class Language(Resource):
    route: final(str) = '/language'

    @staticmethod
    @jwt_required
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('language', location='json', required=True, type=str)
        lang = parser.parse_args()['language']
        current_user.selected_language = lang
        return Response("", 200)
