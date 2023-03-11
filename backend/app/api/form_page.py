#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_failure, get_request, create_id_reqparser
from backend.app.database.form import Form
from ..database.auxiliary import prettify_answer


class FormPage(Resource):
    route: final(str) = '/form_page'

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
        result = options[0].to_json()
        result['answers'] = [prettify_answer(answer) for answer in result['answers']]
        return Response(json.dumps(result), 200)
