#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_failure, get_request
from backend.app.database.form import Form
from ..database.auxiliary import prettify_answer


class FormPage(Resource):
    @staticmethod
    @jwt_required()
    @get_request()
    def get(id: int) -> Response:
        options = Form.get_by_ids({id})
        if len(options) == 0:
            return get_failure(HTTPErrorCode.WRONG_ID, 404)
        result = options[0]
        result['answers'] = [prettify_answer(answer) for answer in result['answers']]
        return Response(result, 200)
