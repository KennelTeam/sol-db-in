import json
from typing import Final

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request, get_failure, HTTPErrorCode, GetRequestParser
from backend.app.database import Form, Question
from backend.app.database.user import Role
from backend.auxiliary import LogicException
from backend.auxiliary.string_dt import string_to_datetime


class Statistics(Resource):
    route: Final[str] = '/statistics'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        parser = GetRequestParser()
        parser.add_argument('question_id', type=int, required=True)
        parser.add_argument('step', type=int, required=False, default=365)
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()

        min_value = request.args.get('min_value', type=int)
        date_min_value = request.args.get('min_value', type=str)
        if min_value is None and date_min_value is not None:
            try:
                min_value = string_to_datetime(date_min_value)
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        max_value = request.args.get('max_value', type=int)
        date_max_value = request.args.get('max_value', type=str)
        if max_value is None and date_max_value is not None:
            try:
                max_value = string_to_datetime(date_max_value)
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)

        if Question.get_by_id(arguments['question_id']) is None:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)

        try:
            statistics = Form.prepare_statistics(arguments['question_id'], min_value, max_value, arguments['step'])
            return Response(json.dumps(statistics), 200)
        except LogicException:
            return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
