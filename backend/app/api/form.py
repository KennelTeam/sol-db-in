#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import HTTPErrorCode, get_request, get_failure
from ..database import QuestionBlock
from ..database.form_type import FormType


class FormSchema(Resource):
    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('form_type', type=str, required=True)
        form_type = parser.parse_args()['form_type']
        if form_type not in FormType:
            return get_failure(HTTPErrorCode.INVALID_ARG_TYPE, 400)
        else:
            form_type = FormType[form_type]

        result = {
            'form_type': form_type.name,
            'question_blocks': QuestionBlock.get_form(form_type)
        }
        return Response(json.dumps(result), 200)
