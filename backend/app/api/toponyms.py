#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import final

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import get_request, get_failure, HTTPErrorCode, post_request, post_failure
from backend.app.database.toponym import Toponym
from backend.app.flask_app import FlaskApp
from ..database.user import Role


class Toponyms(Resource):
    route: final(str) = '/toponym'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        id = request.args.get('id', type=int, default=-1)
        name = request.args.get('name', type=str, default='')
        if name != '':
            top = Toponym.get_by_name(name)
        elif id != -1:
            top = Toponym.get_by_id(id)
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
        parser.add_argument('parent_id', type=int, location='json', required=True)
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
