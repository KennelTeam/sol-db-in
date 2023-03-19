#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, post_request, post_failure, create_standard_reqparser
from backend.app.flask_app import FlaskApp
from ..database import QuestionBlock
from backend.app.database.form_type import FormType
from ..database.user import Role


class QuestionBlockPage(Resource):
    route: Final[str] = '/question_block'

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        parser = create_standard_reqparser()
        parser.add_argument('form_type', type=str, location='json', required=True)
        parser.add_argument('sorting', type=int, location='json', required=True)
        arguments = parser.parse_args()
        if arguments['form_type'] not in FormType.items():
            return post_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        arguments['form_type'] = FormType[arguments['form_type']]
        if arguments['id'] != -1:
            current = QuestionBlock.get_by_id(arguments['id'])
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            if current.form != arguments['form_type']:
                return post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
            current.name = arguments['name']
            current.sorting = arguments['sorting']
            current.deleted = arguments['deleted']
        else:
            current = QuestionBlock(arguments['name'], arguments['form_type'], arguments['sorting'])
            FlaskApp().add_database_item(current)
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)

