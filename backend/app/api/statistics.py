import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from backend.app.api.auxiliary import get_request, get_failure, HTTPErrorCode
from backend.app.database import Form, Question
from backend.app.database.user import Role
from backend.auxiliary import LogicException
from backend.auxiliary.string_dt import string_to_datetime


class Statistics(Resource):
    route: final(str) = '/statistics'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', type=int, location='json', required=True)
        parser.add_argument('min_value', type=int | str, location='json', required=False, default=None)
        parser.add_argument('max_value', type=int | str, location='json', required=False, default=None)
        parser.add_argument('step', type=int, location='json', required=True)
        arguments = parser.parse_args()

        min_value = arguments['min_value']
        if min_value is not None and isinstance(min_value, str):
            min_value = string_to_datetime(min_value)
        max_value = arguments['min_value']
        if max_value is not None and isinstance(max_value, str):
            max_value = string_to_datetime(max_value)

        if Question.get_by_id(arguments['question_id']) is None:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)

        try:
            statistics = Form.prepare_statistics(arguments['question_id'], min_value, max_value, arguments['step'])
            return Response(json.dumps(statistics), 200)
        except LogicException:
            return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
