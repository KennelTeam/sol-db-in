#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from datetime import datetime, timedelta
from typing import Any, Set, List, Type
from sqlalchemy import func
import sqlalchemy
from enum import Enum
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .answer import Answer, ExtremumType
from .question import Question, QuestionType
from .toponym import Toponym
from .user import User
from .answer_option import AnswerOption
from backend.constants import DATE_FORMAT
from backend.auxiliary import JSON, LogicException


class FormState(Enum):
    PLANNED = 1
    STARTED = 2
    FINISHED = 3


class Form(Editable):
    _state = FlaskApp().db.Column('state', FlaskApp().db.Enum(FormState))

    def __init__(self, state=FormState.PLANNED):
        super(Editable).__init__()
        self.state = state

    def to_json(self) -> JSON:
        return super(Editable).to_json() | {
            'state': self.state
        }

    @property
    def state(self) -> FormState:
        return self._state

    @staticmethod
    def _filter_by_answers_count(question_id: int, min_answers_count: int, max_answers_count: int) -> Set[int]:
        query = Answer.query_question_grouped_by_forms(question_id)
        # Somehow Pylint does not see that count is a class, so it's not a call, it's a construction of an object
        condition = sqlalchemy.and_(func.count() >= min_answers_count,  # pylint: disable=not-callable
                                    func.count() < max_answers_count)  # pylint: disable=not-callable
        query = query.having(condition)
        return set(item.form_id for item in query.all())

    @staticmethod
    def _filter_ids(table: Type[FlaskApp().db.Model], name_condition,
                    question_id: int, exact_value: Any, min_value: Any,
                    max_value: Any, substring: str, row_question_id: int
                    ) -> Set[int]:

        name_search = FlaskApp().request(table).filter(name_condition)

        ids = Answer.get_distinct_filtered(question_id, exact_value, min_value, max_value, substring, row_question_id)
        query = name_search.filter(table.id.in_(ids))
        query = query.with_entities(table.id).distinct(table.id)

        return set(item.id for item in query.all())

    @state.setter
    @Editable.on_edit
    def state(self, new_state: FormState) -> None:
        self._state = new_state

    @staticmethod
    def _prepare_statistics(table: Type[FlaskApp().db.Model], question_id: int,
                            min_value: int | datetime = None, max_value: int | datetime = None,
                            step: int | datetime = None):

        question = Question.get_by_id(question_id)
        filters = Form._get_statistics_filters(question, min_value, max_value, step)

        result = {}
        for state in FormState:
            forms = FlaskApp().request(table).with_entities(table.id)
            # It's not an encapsulation violation because the table is derived from Form, so actually it's the access
            # of Form's field _state
            forms = forms.filter_by(_state=state)
            ids = [form.id for form in forms.all()]
            result[state.name] = {}
            for condition in filters:
                result[state.name][condition['name']] = Answer.count_with_condition(ids, condition)

        return result

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
                'name': option.text,
                'filter': Answer.value_int.in_([option.id])
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
