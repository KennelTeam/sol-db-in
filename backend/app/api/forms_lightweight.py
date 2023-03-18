#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from typing import Final

from .auxiliary import HTTPErrorCode, get_failure, get_request, GetRequestParser
from backend.app.database.form import Form, FormType


class FormsLightweight(Resource):
    route: Final[str] = '/forms_lightweight'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        parser = GetRequestParser()
        parser.add_argument('form_type', type=str, required=True)
        if parser.error is not None:
            return parser.error
        arguments = parser.parse_args()

        if arguments['form_type'] not in FormType.items():
            return get_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        form_type = FormType[arguments['form_type']]
        ids = Form.get_all_ids(form_type)
        forms = Form.get_by_ids(ids)

        result = [
            {
                "id": form.id,
                "name": form.name
            } for form in forms
        ]
        return Response(json.dumps(result), 200)
