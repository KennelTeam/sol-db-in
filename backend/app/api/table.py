#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import HTTPErrorCode, post_request, post_failure
from backend.app.flask_app import FlaskApp
from ..database import FixedTable, QuestionTable
from ..database.user import Role


class Table(Resource):
    route: final(str) = '/table'

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('block_sorting', type=int, location='json', required=True)
        parser.add_argument('id', type=int, location='json', required=False, default=-1)
        parser.add_argument('type', type=str, location='json', required=True)
        parser.add_argument('deleted', type=bool, location='json', required=False, default=False)
        arguments = parser.parse_args()

        if arguments['type'] not in {'FIXED_TABLE', 'QUESTION_TABLE'}:
            return post_failure(HTTPErrorCode.INVALID_ARG_TYPE, 400)
        TableClass = FixedTable if arguments['type'] == "FIXED_TABLE" else QuestionTable
        if arguments['id'] != -1:
            current = TableClass.get_by_id(arguments['id'])
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            current.block_sorting = arguments['block_sorting']
        else:
            current = TableClass(arguments['block_sorting'])
            FlaskApp().add_database_item(current)
        if current.deleted != arguments['deleted']:
            current.deleted = arguments['deleted']
        FlaskApp().flush_to_database()
        return Response(current.id, 200)
