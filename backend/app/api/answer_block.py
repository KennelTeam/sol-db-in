#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from typing import final

from .auxiliary import get_request, get_class_item_by_id_request, HTTPErrorCode, post_request, post_failure, \
    create_standard_reqparser
from backend.app.flask_app import FlaskApp
from ..database import AnswerBlock
from ..database.user import Role


class AnswerBlockPage(Resource):
    route: final(str) = '/answer_block'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return get_class_item_by_id_request(AnswerBlock)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        parser = create_standard_reqparser()
        arguments = parser.parse_args()
        if arguments['id'] != -1:
            current = AnswerBlock.get_by_id(arguments['id'])
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            current.name = arguments['name']
            current.deleted = arguments['deleted']
        else:
            current = AnswerBlock(arguments['name'])
            FlaskApp().add_database_item(current)
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)


