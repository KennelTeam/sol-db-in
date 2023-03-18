#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_failure, get_request, create_id_reqparser
from backend.app.database.form import Form
from ..database import QuestionBlock
from ..database.auxiliary import prettify_answer


class FormPage(Resource):
    route: Final[str] = '/form_page'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        parser = create_id_reqparser()
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()

        options = Form.get_by_ids({arguments['id']})
        if len(options) == 0:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)
        blocks = QuestionBlock.get_form(options[0].form_type)
        values = [block.get_questions(with_answers=True, form_id=arguments['id']) for block in blocks]
        result = options[0].to_json(with_answers=False) | {
            "answers": values
        }
        return Response(json.dumps(result), 200)
