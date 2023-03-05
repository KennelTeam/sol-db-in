import json
from typing import final

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request, get_failure, HTTPErrorCode
from backend.app.database import Action
from backend.app.database.timestamp_range import TimestampRange
from backend.app.database.user import Role
from backend.auxiliary.string_dt import string_to_datetime


class Actions(Resource):
    route: final(str) = '/actions'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        user_id = request.args.get('user_id', type=int, default=-1)
        timestamp_from = request.args.get('timestamp_from', type=str, default=None)
        timestamp_to = request.args.get('timestamp_to', type=str, default=None)
        table_id = request.args.get('table_id', type=int, default=-1)
        column_id = request.args.get('column_id', type=str, default='')
        row_id = request.args.get('row_id', type=int, default=-1)
        value = request.args.get('value', type=int, default=None)

        timestamp_range = TimestampRange()
        if timestamp_from is not None:
            try:
                timestamp_range.begin = string_to_datetime(timestamp_from)
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        if timestamp_to is not None:
            try:
                timestamp_range.end = string_to_datetime(timestamp_to)
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)

        filtered_actions = Action.filter(user_id, timestamp_range, table_id, column_id, row_id, value)

        return Response(json.dumps([action.to_json() for action in filtered_actions]), 200)
