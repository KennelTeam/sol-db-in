import json
from typing import final

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

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
        question_id = request.args.get('question_id', type=int, default=None)
        if question_id is None:
            get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        min_value = request.args.get('min_value', type=int | str, default=None)
        max_value = request.args.get('max_value', type=int | str, default=None)
        step = request.args.get('step', type=int, default=None)
        if step is None:
            get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)

        if min_value is not None and isinstance(min_value, str):
            min_value = string_to_datetime(min_value)
        if max_value is not None and isinstance(max_value, str):
            max_value = string_to_datetime(max_value)

        if Question.get_by_id(question_id) is None:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)

        try:
            statistics = Form.prepare_statistics(question_id, min_value, max_value, step)
            return Response(json.dumps(statistics), 200)
        except LogicException:
            return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
