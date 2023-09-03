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
        print(tagged_answers)
        tagging_questions = set(item.id for item in FlaskApp().request(Question).
                                filter_by(_question_type=QuestionType.LONG_TEXT).all())
        table_formattings = set(item.id for item in FlaskApp().request(FormattingSettings).filter(FormattingSettings._table_id != None).all())
        table_questions = set(item.id for item in FlaskApp().request(Question).filter(Question._formatting_settings.in_(table_formattings)))
        print(tagging_questions)
        tagging_questions = tagging_questions - table_questions
        not_tagged_answers = FlaskApp().request(Answer).filter(Answer._question_id.in_(tagging_questions)).\
            filter(Answer.id.notin_(tagged_answers)).all()
        for answer in not_tagged_answers:
            print(json.dumps(answer.to_json()))
        forms = FlaskApp().request(Form).filter(Form.id.in_(set(item.form_id for item in not_tagged_answers))).all()
        links = [
            {
                'link': "/" + str(item.form_type).split('.')[1].lower() + "/" + str(item.id),
                'name': item.name
            } for item in forms
        ]
        return Response(json.dumps({
            "data": links
        }), 200)
