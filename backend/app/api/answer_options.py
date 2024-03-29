#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Final

import flask
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import get_request, HTTPErrorCode, post_request, post_failure, get_class_item_by_id_request
from backend.app.database.answer_option import AnswerOption
from backend.app.flask_app import FlaskApp
from ..database import AnswerBlock
from ..database.user import Role


class AnswerOptionsPage(Resource):
    route: Final[str] = '/answer_options'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return get_class_item_by_id_request(AnswerOption)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        print(flask.request)
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=False, default=-1)
        parser.add_argument('name', type=dict, location='json', required=True)
        parser.add_argument('short_name', type=dict, location='json', required=True)
        parser.add_argument('answer_block_id', type=int, location='json', required=True)
        parser.add_argument('deleted', type=bool, location='json', required=False, default=False)
        arguments = parser.parse_args()
        print(arguments)
        if AnswerBlock.get_by_id(arguments['answer_block_id']) is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)

        if arguments['id'] == -1:
            current = AnswerOption(arguments['name'], arguments['short_name'], arguments['answer_block_id'])
            FlaskApp().add_database_item(current)
        else:
            current = AnswerOption.get_by_id(arguments['id'])
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            current.name = arguments['name']
            current.short_name = arguments['short_name']
            current.deleted = arguments['deleted']
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)
