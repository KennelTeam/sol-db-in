#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.database.form_type import FormType
from backend.app.database.localization import localize
from backend.app.api.auxiliary import get_request, get_failure, HTTPErrorCode, GetRequestParser
from backend.app.database import Form, Question, Answer
from backend.app.database.user import Role


class FullnessStatistics(Resource):
    route: Final[str] = '/fullness_statistics'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get():
        parser = GetRequestParser()
        parser.add_argument('report_type', type=str, required=True)
        parser.add_argument('form_type', type=str, required=True)
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()
        if arguments['report_type'] not in ('BY_FORM', 'BY_QUESTION'):
            return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        if arguments['form_type'] not in FormType.items():
            return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        form_type = FormType[arguments['form_type']]
        result = []
        if arguments['report_type'] == 'BY_FORM':
            max_count = Question.count_form_type_questions(form_type)
            for form in Form.get_all_forms(form_type):
                result.append({
                    'id': form.id,
                    'count': Answer.count_answered_questions(form.id),
                    'name': form.name
                })
        else:
            max_count = Form.count_of_type(form_type)
            for question in Question.get_of_form_type(form_type):
                result.append({
                    'id': question.id,
                    'name': localize(question.text),
                    'count': Answer.count_answered_forms(question.id)
                })
        return Response(json.dumps({
            'max_count': max_count,
            'statistics': result
        }), 200)
