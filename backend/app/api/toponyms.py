#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import get_request, get_failure, HTTPErrorCode, post_request, post_failure, GetRequestParser
from backend.app.database.toponym import Toponym
from backend.app.flask_app import FlaskApp
from ..database.user import Role


class Toponyms(Resource):
    route: Final[str] = '/toponym'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        parser = GetRequestParser()
        parser.add_argument('id', type=int, default=-1)
        parser.add_argument('name', type=str, default='')
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()
        if arguments['name'] != '':
            top = Toponym.get_by_name(arguments['name'])
        elif arguments['id'] != -1:
            top = Toponym.get_by_id(arguments['id'])
        else:
            return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        if top is None:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)
        ancestors = top.get_ancestors()
        result = top.to_json(with_children=False)
        result['ancestors'] = [ancestor.to_json(with_children=False) for ancestor in ancestors]
        return Response(json.dumps(result), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.EDITOR)
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('parent_id', type=int, location='json', required=False, default=None)
        parser.add_argument('name', type=str, location='json', required=True)
        arguments = parser.parse_args()
        if Toponym.get_by_id(arguments['parent_id']) is None:
            post_failure(HTTPErrorCode.WRONG_ID, 400)
        if Toponym.get_by_name(arguments['name']) is not None:
            post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
        current = Toponym(arguments['name'], arguments['parent_id'])
        FlaskApp().add_database_item(current)
        FlaskApp().flush_to_database()
        return Response(str(current.id), 201)

    @staticmethod
    @jwt_required()
    @post_request(Role.EDITOR)
    def put() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=True)
        parser.add_argument('name', type=str, location='json', required=True)
        arguments = parser.parse_args()
        current = Toponym.get_by_id(arguments['id'])
        if current is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)
        current.name = arguments['name']
        FlaskApp().flush_to_database()
        return Response("", 200)
