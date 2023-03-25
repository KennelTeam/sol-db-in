#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_failure, get_request, create_id_reqparser
from backend.app.database.form import Form
from ..database import QuestionBlock, FormattingSettings, Question, Answer, PrivacySettings, User, Toponym


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
        QuestionBlock.upload_cache()
        FormattingSettings.upload_cache()
        Question.upload_cache()
        # Answer.upload_cache()
        PrivacySettings.upload_cache()
        User.upload_cache()
        Toponym.upload_cache()
        print('successfully cached')
        blocks = QuestionBlock.get_form(options[0].form_type)
        values = [block.to_json(with_answers=True, form_id=arguments['id']) for block in blocks]
        result = options[0].to_json(with_answers=False) | {
            "answers": values
        }
        QuestionBlock.clear_cache()
        FormattingSettings.clear_cache()
        Question.clear_cache()
        # Answer.clear_cache()
        PrivacySettings.clear_cache()
        User.clear_cache()
        Toponym.clear_cache()
        return Response(json.dumps(result), 200)
