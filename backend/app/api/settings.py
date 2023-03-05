import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from backend.app.api.auxiliary import get_request, post_request, HTTPErrorCode
from backend.app.database.user import Role
from backend.constants import MAX_LOGIN_SIZE, MAX_FULLNAME_SIZE, MAX_NAME_SIZE, MAX_PROJECT_NAME_SIZE, MAX_TAG_SIZE, \
    MAX_COMMENT_SIZE, MAX_BLOCK_NAME_SIZE, MAX_ANSWER_BLOCK_NAME, MAX_ANSWER_OPTION_SIZE, MAX_SHORT_ANSWER_OPTION_SIZE, \
    MAX_SHEET_TITLE_SIZE, MAX_ANSWER_SIZE, MAX_SHORT_QUESTION_SIZE, MAX_LEADERS_PAGE_SIZE, MAX_PROJECTS_PAGE_SIZE


class Settings(Resource):
    route: final(str) = '/settings'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        constants = {
            'MAX_LOGIN_SIZE': MAX_LOGIN_SIZE,
            'MAX_FULLNAME_SIZE': MAX_FULLNAME_SIZE,
            'MAX_NAME_SIZE': MAX_NAME_SIZE,
            'MAX_PROJECT_NAME_SIZE': MAX_PROJECT_NAME_SIZE,
            'MAX_TAG_SIZE': MAX_TAG_SIZE,
            'MAX_COMMENT_SIZE': MAX_COMMENT_SIZE,
            'MAX_BLOCK_NAME_SIZE': MAX_BLOCK_NAME_SIZE,
            'MAX_ANSWER_BLOCK_NAME': MAX_ANSWER_BLOCK_NAME,
            'MAX_ANSWER_OPTION_SIZE': MAX_ANSWER_OPTION_SIZE,
            'MAX_SHORT_ANSWER_OPTION_SIZE': MAX_SHORT_ANSWER_OPTION_SIZE,
            'MAX_SHEET_TITLE_SIZE': MAX_SHEET_TITLE_SIZE,
            'MAX_ANSWER_SIZE': MAX_ANSWER_SIZE,
            'MAX_SHORT_QUESTION_SIZE': MAX_SHORT_QUESTION_SIZE,
            'MAX_LEADERS_PAGE_SIZE': MAX_LEADERS_PAGE_SIZE,
            'MAX_PROJECTS_PAGE_SIZE': MAX_PROJECTS_PAGE_SIZE
        }
        return Response(json.dumps(constants), 200)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def patch() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('MAX_COMMENT_SIZE', type=int, location='json', required=False, default=None)
        parser.add_argument('MAX_LEADERS_PAGE_SIZE', type=int, location='json', required=False, default=None)
        parser.add_argument('MAX_PROJECTS_PAGE_SIZE', type=int, location='json', required=False, default=None)
        arguments = parser.parse_args()

        
