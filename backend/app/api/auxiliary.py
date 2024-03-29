#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Any
from flask_jwt_extended import current_user, jwt_required
from flask_restful import reqparse

from backend.app.flask_app import FlaskApp
from backend.auxiliary.types import JSON
from backend.app.database.user import Role

from flask import Response, request
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
    JWT_NOT_FOUND = 8
    JWT_EXPIRED = 9
    INVALID_JWT = 10


class GetRequestParser:
    def __init__(self):
        self.arguments = {}
        self.error: Response = None

    def add_argument(self, name: str, type=None, required=False, default=None) -> None:
        if required:
            if request.args.get(name) is None and self.error is None:
                self.error = get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
            if request.args.get(name, type=type) is None and self.error is None:
                self.error = get_failure(HTTPErrorCode.INVALID_ARG_TYPE, 400)
        self.arguments[name] = request.args.get(name, type=type, default=default)

    def parse_args(self):
        return self.arguments


def create_id_reqparser() -> GetRequestParser:
    parser = GetRequestParser()
    parser.add_argument('id', type=int, required=True)
    return parser


def get_class_item_by_id_request(Class) -> Response:
    parser = create_id_reqparser()
    if parser.error is not None:
        return parser.error
    arguments = parser.parse_args()
    current = Class.get_by_id(arguments['id'])
    if current is None:
        return get_failure(HTTPErrorCode.WRONG_ID, 404)
    return Response(json.dumps(current.to_json()), 200)


def create_standard_reqparser() -> reqparse.RequestParser:
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, location='json', required=False, default=-1)
    parser.add_argument('name', type=dict, location='json', required=True)
    parser.add_argument('deleted', type=bool, location='json', required=False, default=False)
    return parser


def standard_text_object_update(Class, arguments: JSON) -> Response:
    current = Class.get_by_id(arguments['id'])
    if current is None:
        return post_failure(HTTPErrorCode.WRONG_ID, 404)
    current.text = arguments['name']
    current.deleted = arguments['deleted']
    FlaskApp().flush_to_database()
    return Response(current.id, 200)


@jwt_required()
def check_rights(min_access_level: Role) -> bool:
    return current_user.role.value >= min_access_level.value


def get_request(min_access_level: Role = Role.GUEST):
    def decorator(func):
        def wrapper() -> Response:
            try:
                FlaskApp().db.session.begin_nested()
                FlaskApp().db.session.rollback()
            except Exception:  # pylint: disable=broad-except
                pass
            if not check_rights(min_access_level):
                return Response({'error': HTTPErrorCode.NOT_ENOUGH_RIGHTS}, 403)
            FlaskApp().set_language(current_user.selected_language)
            return func()
        return wrapper
    return decorator


def post_request(min_access_level: Role = Role.INTERN):
    def decorator(func):
        def wrapper():
            try:
                FlaskApp().db.session.commit()
            except Exception:  # pylint: disable=broad-except
                pass
            if not check_rights(min_access_level):
                return Response({'error': HTTPErrorCode.NOT_ENOUGH_RIGHTS}, 403)
            FlaskApp().db.session.begin_nested()
            FlaskApp().use_deleted_items_in_this_request()
            return func()
        return wrapper
    return decorator


def post_failure(error: HTTPErrorCode, status: int) -> Response:
    FlaskApp().db.session.rollback()
    return Response(json.dumps({'error': error.name}), status)


def get_failure(error: HTTPErrorCode, status: int) -> Response:
    return Response(json.dumps({'error': error.name}), status)


def check_json_format(source: Any, json_format: JSON) -> HTTPErrorCode:
    if not isinstance(source, dict):
        return HTTPErrorCode.INVALID_ARG_FORMAT
    for key in json_format:
        if isinstance(json_format[key], set) and None in json_format[key] and (key not in source or source[key] is None):
            continue
        if key not in source:
            return HTTPErrorCode.MISSING_ARGUMENT
        if not type(json_format[key]) == set and issubclass(json_format[key], enum.Enum):
            if not isinstance(source[key], str) or source[key] not in json_format[key].items():
                return HTTPErrorCode.INVALID_ARG_TYPE
        elif type(json_format[key]) == set:
            if type(source[key]) not in json_format[key]:
                return HTTPErrorCode.INVALID_ARG_TYPE
        elif not type(json_format[key]) == set and issubclass(json_format[key], enum.Enum):
            if not isinstance(source[key], str) or source[key] not in json_format[key].items():
                return HTTPErrorCode.INVALID_ARG_TYPE
        elif type(source[key]) != json_format[key]:
            return HTTPErrorCode.INVALID_ARG_TYPE
    return HTTPErrorCode.SUCCESS
