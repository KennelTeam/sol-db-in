import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from backend.app.api.auxiliary import get_request, post_request
from backend.app.database.user import Role
from backend import constants


class Settings(Resource):
    route: Final[str] = '/settings'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        constants_dict = {
            'MAX_LOGIN_SIZE': constants.MAX_LOGIN_SIZE,
            'MAX_FULLNAME_SIZE': constants.MAX_FULLNAME_SIZE,
            'MAX_NAME_SIZE': constants.MAX_NAME_SIZE,
            'MAX_PROJECT_NAME_SIZE': constants.MAX_PROJECT_NAME_SIZE,
            'MAX_TAG_SIZE': constants.MAX_TAG_SIZE,
            'MAX_USER_COMMENT_SIZE': constants.MAX_USER_COMMENT_SIZE,
            'MAX_QUESTION_COMMENT_SIZE': constants.MAX_QUESTION_COMMENT_SIZE,
            'MAX_COMMENT_SIZE_IN_LEADERS_LIST': constants.MAX_COMMENT_SIZE_IN_LEADERS_LIST,
            'MAX_BLOCK_NAME_SIZE': constants.MAX_BLOCK_NAME_SIZE,
            'MAX_ANSWER_BLOCK_NAME': constants.MAX_ANSWER_BLOCK_NAME,
            'MAX_ANSWER_OPTION_SIZE': constants.MAX_ANSWER_OPTION_SIZE,
            'MAX_SHORT_ANSWER_OPTION_SIZE': constants.MAX_SHORT_ANSWER_OPTION_SIZE,
            'MAX_SHEET_TITLE_SIZE': constants.MAX_SHEET_TITLE_SIZE,
            'MAX_ANSWER_SIZE': constants.MAX_ANSWER_SIZE,
            'MAX_SHORT_QUESTION_SIZE': constants.MAX_SHORT_QUESTION_SIZE,
            'MAX_LEADERS_PAGE_SIZE': constants.MAX_LEADERS_PAGE_SIZE,
            'MAX_PROJECTS_PAGE_SIZE': constants.MAX_PROJECTS_PAGE_SIZE
        }
        return Response(json.dumps(constants_dict), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def patch() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('MAX_COMMENT_SIZE_IN_LEADERS_LIST', type=int, location='json', required=False, default=None)
        parser.add_argument('MAX_LEADERS_PAGE_SIZE', type=int, location='json', required=False, default=None)
        parser.add_argument('MAX_PROJECTS_PAGE_SIZE', type=int, location='json', required=False, default=None)
        arguments = parser.parse_args()

        if arguments['MAX_LEADERS_PAGE_SIZE'] is not None:
            constants.MAX_LEADERS_PAGE_SIZE = arguments['MAX_LEADERS_PAGE_SIZE']
        if arguments['MAX_PROJECTS_PAGE_SIZE'] is not None:
            constants.MAX_PROJECTS_PAGE_SIZE = arguments['MAX_PROJECTS_PAGE_SIZE']
        if arguments['MAX_COMMENT_SIZE_IN_LEADERS_LIST'] is not None:
            constants.MAX_COMMENT_SIZE_IN_LEADERS_LIST = arguments['MAX_COMMENT_SIZE_IN_LEADERS_LIST']

        return Response(json.dumps({'message': 'Success'}), 200)
