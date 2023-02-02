#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_NAME_SIZE
from backend.app.flask_app import FlaskApp
from .form import Form, FormState
from .editable import Editable
from typing import Any, Dict, Set, List
from .question_block import QuestionBlock
from .form_type import FormType
from .question import Question, Type


class Leader(Form, FlaskApp().db.Model):
    __tablename__ = 'leaders'
    _first_name = FlaskApp().db.Column('first_name', FlaskApp().db.Text(MAX_NAME_SIZE))
    _last_name = FlaskApp().db.Column('last_name', FlaskApp().db.Text(MAX_NAME_SIZE))
    _middle_name = FlaskApp().db.Column('middle_name', FlaskApp().db.Text(MAX_NAME_SIZE))

    def __init__(self, first_name: str, last_name: str, middle_name: str = ""):
        super(Form, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    def to_json(self, short_form: bool = False) -> Dict[str, Any]:
        form = QuestionBlock.get_form(FormType.LEADER)
        return super(Form).to_json() | {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'answers': [
                block.get_questions(with_answers=True, form_id=self.id, short_form=short_form) for block in form
            ]
        }

    @staticmethod
    def filter(name_substr: str, question_id: int, exact_value: Any = None, min_value: Any = None,
               max_value: Any = None, substring: str = None, row_question_id: int = None) -> Set[int]:

        name_pattern = f"%{name_substr}%"
        name_condition = FlaskApp().db.or_(Leader._first_name.like(name_pattern),
                                           Leader._middle_name.like(name_pattern))

        name_condition = FlaskApp().db.or_(Leader._last_name.like(name_pattern), name_condition)

        return Form._filter_ids(Leader, FormType.LEADER, name_condition,
                                question_id, exact_value, min_value, max_value, substring, row_question_id)

    @staticmethod
    def get_statistics(question_id: int) -> Dict[str, Any]:
        question = Question.get_by_id(question_id)
        if question.question_type in {Type.RELATION, Type.LONG_TEXT, Type.SHORT_TEXT}:
            return {}



    @staticmethod
    def get_by_ids(ids: Set[int]) -> List['Leader']:
        return Leader.query.filter(Leader.id.in_(ids)).all()

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    @Editable.on_edit
    def first_name(self, new_name: str) -> None:
        self._first_name = new_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    @Editable.on_edit
    def last_name(self, new_name: str) -> None:
        self._last_name = new_name

    @property
    def middle_name(self) -> str:
        return self._middle_name

    @middle_name.setter
    @Editable.on_edit
    def middle_name(self, new_name: str) -> None:
        self._middle_name = new_name

    @property
    def name(self) -> str:
        return self._last_name + ' ' + self.first_name + ' ' + self.middle_name
