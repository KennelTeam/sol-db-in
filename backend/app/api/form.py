#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_request, get_failure, GetRequestParser
from .. import FlaskApp
from ..database import QuestionBlock
from ..database.form_type import FormType
from ...constants import ALL_LANGUAGES_TAG


class FormSchema(Resource):
    route: Final[str] = '/form'

    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        FlaskApp().set_language(ALL_LANGUAGES_TAG)
        parser = GetRequestParser()
        parser.add_argument('form_type', type=str, required=True)
        if parser.error is not None:
            return parser.error
        form_type = parser.parse_args()['form_type']
        if form_type not in FormType.items():
            return get_failure(HTTPErrorCode.INVALID_ARG_TYPE, 400)
        form_type = FormType[form_type]

        result = {
            'form_type': form_type.name,
            'question_blocks': [block.to_json() for block in QuestionBlock.get_form(form_type)]
        }
        return Response(json.dumps(result), 200)
