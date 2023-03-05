#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import final

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request, HTTPErrorCode, post_request, post_failure, get_class_item_by_id_request, get_failure
from backend.app.database.answer_option import AnswerOption
from backend.app.flask_app import FlaskApp
from ..database import AnswerBlock
from ..database.user import Role


class AnswerOptionsPage(Resource):
    route: final(str) = '/answer_options'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return get_class_item_by_id_request(AnswerOption)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        id = request.args.get('id', type=int, default=-1)
        name = request.args.get('name', type=dict, default=None)
        if name is None:
            get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        short_name = request.args.get('short_name', type=dict, default=None)
        if short_name is None:
            get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        answer_block_id = request.args.get('answer_block_id', type=int, default=None)
        if answer_block_id is None:
            get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        deleted = request.args.get('deleted', type=bool, default=False)

        if AnswerBlock.get_by_id(answer_block_id) is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)

        if id == -1:
            current = AnswerOption(name, short_name, answer_block_id)
            FlaskApp().add_database_item(current)
        else:
            current = AnswerOption.get_by_id(id)
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            current.name = name
            current.short_name = short_name
            current.deleted = deleted
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)
