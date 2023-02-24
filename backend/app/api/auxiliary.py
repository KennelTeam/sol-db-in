#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Any
from flask_jwt_extended import current_user, jwt_required
from flask_restful import reqparse

from backend.app.flask_app import FlaskApp
from backend.auxiliary.types import JSON
from backend.app.database.user import Role

from flask import Response
import enum


class HTTPErrorCode(enum.Enum):
    SUCCESS = 0
    INVALID_ARG_LOCATION = 1
    INVALID_ARG_TYPE = 2
    MISSING_ARGUMENT = 3
    WRONG_ID = 4
    INVALID_ARG_FORMAT = 5
    CONFLICTING_ARGUMENTS = 6
    NOT_ENOUGH_RIGHTS = 7


def get_class_item_by_id_request(Class) -> Response:
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, location='json', required=True)
    arguments = parser.parse_args()
    current = Class.get_by_id(arguments['id'])
    if current is None:
        return get_failure(HTTPErrorCode.WRONG_ID, 404)
    return Response(json.dumps(current.to_json()), 200)


def create_standard_reqparser() -> reqparse.RequestParser:
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, location='json', required=False, default=-1)
    parser.add_argument('name', type=dict, location='json')
    parser.add_argument('deleted', type=bool, location='json', required=False, default=False)
    return parser


@jwt_required()
def check_rights(min_access_level: Role) -> bool:
    return current_user.role.value >= min_access_level.value


def get_request(min_access_level: Role = Role.GUEST):
    def decorator(func):
        def wrapper() -> Response:
            if not check_rights(min_access_level):
                return Response({'error': HTTPErrorCode.NOT_ENOUGH_RIGHTS}, 403)
            return func()
        return wrapper
    return decorator


def post_request(min_access_level: Role = Role.INTERN):
    def decorator(func):
        def wrapper():
            if not check_rights(min_access_level):
                return Response({'error': HTTPErrorCode.NOT_ENOUGH_RIGHTS}, 403)
            FlaskApp().db.session.begin_nested()
            return func()
        return wrapper
    return decorator


def post_failure(error: HTTPErrorCode, status: int) -> Response:
    FlaskApp().db.session.rollback()
    return Response(json.dumps({'error': error.name}), status)


def get_failure(error: HTTPErrorCode, status: int) -> Response:
    return Response(json.dumps({'error': error.name}), status)


def check_json_format(source: Any, json_format: JSON) -> HTTPErrorCode:
    if type(source) != dict:
        return HTTPErrorCode.INVALID_ARG_FORMAT
    for key in json_format:
        if key not in source:
            return HTTPErrorCode.MISSING_ARGUMENT
        if type(json_format[key]) != set:
            if type(source[key]) != json_format[key]:
                return HTTPErrorCode.INVALID_ARG_TYPE
        elif type(source[key]) not in json_format[key]:
            return HTTPErrorCode.INVALID_ARG_TYPE
    return HTTPErrorCode.SUCCESS
