#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request, GetRequestParser, get_failure, HTTPErrorCode
from backend.app.database import Question
from backend.app.database.form_type import FormType
from backend.app.database.question_type import QuestionType
from backend.app.database.user import Role


class QuestionsLightweight(Resource):
    route: Final[str] = '/questions_lightweight'

    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        parser = GetRequestParser()
        parser.add_argument('form_type', type=str, required=True)
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()
        if arguments['form_type'] not in FormType.items():
            return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        form_type = FormType[arguments['form_type']]
        data = [item.to_json() for item in Question.get_of_form_type(form_type) if item.question_type in
                      {QuestionType.DATE, QuestionType.CHECKBOX, QuestionType.MULTIPLE_CHOICE, QuestionType.NUMBER}]
        return Response(json.dumps(
            {"questions": data}
        ), 200)

