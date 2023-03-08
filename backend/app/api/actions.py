import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request, get_failure, HTTPErrorCode, GetRequestParser
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
        parser = GetRequestParser()
        parser.add_argument('user_id', type=int, default=-1)
        parser.add_argument('timestamp_from', type=str)
        parser.add_argument('timestamp_to', type=str)
        parser.add_argument('table_id', type=int, default=-1)
        parser.add_argument('column_id', type=str, default='')
        parser.add_argument('row_id', type=int, default=-1)
        parser.add_argument('value', type=int, default=None)
        arguments = parser.parse_args()

        timestamp_range = TimestampRange()
        if arguments['timestamp_from'] is not None:
            try:
                timestamp_range.begin = string_to_datetime(arguments['timestamp_from'])
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        if arguments['timestamp_to'] is not None:
            try:
                timestamp_range.end = string_to_datetime(arguments['timestamp_to'])
            except ValueError:
                return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)

        filtered_actions = Action.filter(arguments['user_id'], timestamp_range, arguments['table_id'],
                                         arguments['column_id'], arguments['row_id'], arguments['value'])

        return Response(json.dumps([action.to_json() for action in filtered_actions]), 200)
