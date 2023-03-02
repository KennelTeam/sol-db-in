#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from datetime import datetime, timedelta
from typing import Any, Set, List
from sqlalchemy import func
import sqlalchemy
from sqlalchemy.dialects.mysql import VARCHAR
from enum import Enum
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .answer import Answer, ExtremumType
from .question import Question, QuestionType
from .toponym import Toponym
from .user import User
from .answer_option import AnswerOption
from .form_type import FormType
from backend.constants import DATE_FORMAT, MAX_NAME_SIZE
from backend.auxiliary import JSON, LogicException


class FormState(Enum):
    PLANNED = 1
    STARTED = 2
    FINISHED = 3

    @staticmethod
    def items() -> Set[str]:
        return set(FormState.__members__.keys())


class Form(Editable, FlaskApp().db.Model):
    __tablename__ = 'forms'
    _state = FlaskApp().db.Column('state', FlaskApp().db.Enum(FormState))
    _name = FlaskApp().db.Column('name', VARCHAR(MAX_NAME_SIZE), unique=True)
    _form_type = FlaskApp().db.Column('form_type', FlaskApp().db.Enum(FormType))

    def __init__(self, form_type: FormType, name: str, state=FormState.PLANNED):
        super().__init__()
        self._form_type = form_type
        self.state = state
        self.name = name

    def to_json(self) -> JSON:
        return super().to_json() | {
            'state': self.state.name,
            'name': self.name,
            'form_type': self.form_type.name,
            'answers': Answer.get_form_answers(self.id)
        }

    @staticmethod
    def filter(name_substr: str, question_id: int, exact_value: Any = None, min_value: Any = None,
               max_value: Any = None, substring: str = None, row_question_id: int = None) -> Set[int]:

        name_pattern = f"%{name_substr}%"
        name_condition = Form._name.like(name_pattern)
        name_search = FlaskApp().request(Form).filter(name_condition)

        ids = Answer.get_distinct_filtered(question_id, exact_value, min_value, max_value, substring, row_question_id)
        query = name_search.filter(Form.id.in_(ids))
        query = query.with_entities(Form.id).distinct(Form.id)
        return set(item.id for item in query.all())

    @staticmethod
    def get_by_ids(ids: Set[int]) -> List['Form']:
        return FlaskApp().request(Form).filter(Form.id.in_(ids)).all()

    @staticmethod
    def get_all_ids() -> Set[int]:
        return {item.id for item in FlaskApp().request(Form).with_entities(Form.id).all()}

    @staticmethod
    def prepare_statistics(question_id: int, min_value: int | datetime = None, max_value: int | datetime = None,
                           step: int = None) -> JSON:

        question = Question.get_by_id(question_id)
        filters = Form._get_statistics_filters(question, min_value, max_value, step)

        result = {}
        for state in FormState:
            forms = FlaskApp().request(Form).with_entities(Form.id)
            forms = forms.filter_by(_state=state)
            ids = [form.id for form in forms.all()]
            result[state.name] = {}
            for condition in filters:
                result[state.name][str(condition['name'])] = Answer.count_with_condition(ids, condition['filter'])

        return result

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @Editable.on_edit
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def form_type(self):
        return self._form_type

    @property
    def state(self) -> FormState:
        return self._state

    @state.setter
    @Editable.on_edit
    def state(self, new_state: FormState) -> str:
        self._state = new_state
        return self._state.name

    @staticmethod
    def _filter_by_answers_count(question_id: int, min_answers_count: int, max_answers_count: int) -> Set[int]:
        query = Answer.query_question_grouped_by_forms(question_id)
        # Somehow Pylint does not see that count is a class, so it's not a call, it's a construction of an object
        condition = sqlalchemy.and_(func.count() >= min_answers_count,  # pylint: disable=not-callable
                                    func.count() < max_answers_count)  # pylint: disable=not-callable
        query = query.having(condition)
        return set(item.form_id for item in query.all())

    @staticmethod
    def _get_statistics_filters(question: Question, min_value: int | datetime = None, max_value: int | datetime = None,
                                step: int = None) -> List[JSON]:

        if question.question_type in {QuestionType.DATE, QuestionType.NUMBER}:
            if min_value is None:
                min_value = Answer.get_extremum(question.id, question.question_type, ExtremumType.MINIMUM)
            if max_value is None:
                max_value = Answer.get_extremum(question.id, question.question_type, ExtremumType.MAXIMUM)
            if step is None:
                raise LogicException(
                    f"step is not passed as argument while it's required for {question.question_type.name}"
                )
            if min_value is None:
                return []
            if question.question_type == QuestionType.DATE:
                return Form._prepare_date(min_value, max_value, step)
            return Form._prepare_number(min_value, max_value, step)
        if question.question_type in {QuestionType.CHECKBOX, QuestionType.MULTIPLE_CHOICE}:
            return Form._prepare_choice_answer(question)
        preparation_function = {
            QuestionType.USER: Form._prepare_user,
            QuestionType.LOCATION: Form._prepare_location,
            QuestionType.BOOLEAN: Form._prepare_boolean,
            QuestionType.SHORT_TEXT: lambda: [],
            QuestionType.LONG_TEXT: lambda: []
        }

        return preparation_function[question.question_type]()

    @staticmethod
    def _prepare_date(min_value: datetime, max_value: datetime, step: int):
        step_timedelta = timedelta(days=step)
        count = 1 + (max_value - min_value) // step_timedelta
        bounds = [min_value + step_timedelta * i for i in range(count)]
        return [{
            'name': Form._range_format(bound.strftime(DATE_FORMAT), (bound + step_timedelta).strftime(DATE_FORMAT)),
            'filter': sqlalchemy.and_(Answer.value_datetime >= bound, Answer.value_datetime < bound + step_timedelta)
        } for bound in bounds]

    @staticmethod
    def _prepare_number(min_value: int, max_value: int, step: int):
        count = 1 + (max_value - min_value - 1) // step
        bounds = [min_value + step * i for i in range(count)]
        return [{
            'name': Form._range_format(str(bound), str(bound + step - 1)),
            'filter': sqlalchemy.and_(Answer.value_int >= bound, Answer.value_int < bound + step)
        } for bound in bounds]

    @staticmethod
    def _range_format(left_bound: str, right_bound: str) -> str:
        if left_bound == right_bound:
            return left_bound
        return f"{left_bound} - {right_bound}"

    @staticmethod
    def _prepare_choice_answer(question: Question):
        options = AnswerOption.get_all_from_block(question.answer_block_id)
        return [
            {
                'name': option['name'],
                'filter': Answer.value_int.in_([option['id']])
            } for option in options
        ]

    @staticmethod
    def _prepare_user():
        users = User.get_all_users()
        return [
            {
                'name': user.name,
                'filter': Answer.value_int.in_([user.id])
            } for user in users
        ]

    @staticmethod
    def _prepare_location():
        locations = Toponym.get_all()
        return [
            {
                'name': location.name,
                'filter': Answer.value_int.in_([location.id])
            } for location in locations
        ]

    @staticmethod
    def _prepare_boolean():
        return [{
            'name': 'False',
            'filter': Answer.value_bool.in_([False])
        }, {
            'name': 'True',
            'filter': Answer.value_bool.in_([True])
        }]
