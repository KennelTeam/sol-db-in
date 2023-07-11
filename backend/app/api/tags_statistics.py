import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request
from backend.app.database import Tag, Question, Answer
from backend.app.database.user import Role


class TagsStatistics(Resource):
    route: Final[str] = '/tags_statistics'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        result = []
        questions = Question.get_long_text()
        tags = Tag.get_all_of_type(0)
        for tag in tags:
            result.append([])
            for question in questions:
                result[-1].append(Answer.count_with_tag(tag.id, question.id))
        return Response(json.dumps({
            'columns': [q.to_json_light() for q in questions],
            'rows': [t.to_json() for t in tags],
            'values': result
        }), 200)
