import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app.api.auxiliary import get_request
from backend.app.database import TagToAnswer, Form, Answer, Question, FormattingSettings
from backend.app.database.question_type import QuestionType
from backend.app.database.user import Role
from backend.app.flask_app import FlaskApp


class TagsUsage(Resource):
    route: Final[str] = '/tags_usage'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:

        tagged_answers = set(item.answer_id for item in TagToAnswer.query.all())
        forms = []
        print(tagged_answers)
        for form in FlaskApp().request(Form).all():
            print(form.id)
            for question in FlaskApp().request(Question).filter_by(_question_type=QuestionType.LONG_TEXT).all():
                if question.form_type != form.form_type:
                    continue
                answers = FlaskApp().request(Answer).filter_by(_form_id=form.id).filter_by(_question_id=question.id).all()
                if len(answers) > 0:
                    print(answers)
                if len(answers) > 0 and len(set(item.id for item in answers) & tagged_answers) == 0:
                    forms.append(form)
                    break

        links = [
            {
                'link': "/" + str(item.form_type).split('.')[1].lower() + "/" + str(item.id),
                'name': item.name
            } for item in forms
        ]
        return Response(json.dumps({
            "data": links
        }), 200)
