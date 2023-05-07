#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from typing import Final

from .auxiliary import get_request
from backend.app.database.question_type import QuestionType
from ..database import Question
from ..database.localization import localize


class AllQuestions(Resource):
    route: Final[str] = '/all_questions'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        questions = Question.all()

        result = [
            {
                "id": q.id,
                "name": localize(q.text),
                "accept_step": q.question_type in (QuestionType.NUMBER, QuestionType.DATE)
            } for q in questions
        ]
        return Response(json.dumps(result), 200)
