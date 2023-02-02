#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from datetime import datetime
from typing import Dict, Any, Set, List
import sqlalchemy.orm
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .form_type import FormType
from .answer import Answer, ExtremumType
from enum import Enum
from .question import Question, Type
from .toponym import Toponym
from .user import User
from .answer_option import AnswerOption


class FormState(Enum):
    PLANNED = 1
    STARTED = 2
    FINISHED = 3


class Form(Editable):
    _state = FlaskApp().db.Column('state', FlaskApp().db.Enum(FormState))

    def __init__(self, state=FormState.PLANNED):
        super(Editable).__init__()
        self.state = state

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'state': self.state
        }

    @property
    def state(self) -> FormState:
        return self._state

    @staticmethod
    def _filter_ids(table: FlaskApp().db.Table, form_type: FormType, name_condition: sqlalchemy.orm.Query,
                    question_id: int, exact_value: Any, min_value: Any,
                    max_value: Any, substring: str, row_question_id: int
                    ) -> Set[int]:

        name_search = table.query.filter(name_condition)

        ids = Answer.get_distinct_filtered(question_id, form_type,
                                           exact_value, min_value, max_value, substring, row_question_id)
        query = name_search.filter(table.id.in_(ids))
        query = query.with_entities(table.id).distinct(table.id)

        return set(item.id for item in query.all())

    @state.setter
    @Editable.on_edit
    def state(self, new_state: FormState) -> None:
        self._state = new_state

    @staticmethod
    def _prepare_statistics(table: FlaskApp().db.Table, form_type: FormType, question_id: int,
                            min_value: int | datetime = None, max_value: int | datetime = None,
                            step_days: int | datetime = None):

        question = Question.get_by_id(question_id)
        filters = Form._get_statistics_filters(question, min_value, max_value, step_days)

        id_column = Answer._leader_id if form_type == FormType.LEADER else Answer._project_id

        result = {}
        for state in FormState:
            forms = table.query.filter_by(table._state == state).with_entities(table.id)
            result[state.name] = {}
            for filter in filters:
                query = Answer.query.filter(filter)
                query = query.filter(id_column.in_(forms)).distinct(id_column)
                result[state.name][filter['name']] = query.count()

        return result

    @staticmethod
    def _get_statistics_filters(question: Question, min_value: int | datetime = None, max_value: int | datetime = None,
                                step_days: int | datetime = None) -> List[Dict[str, Any]]:

        if question.question_type in {Type.DATE, Type.NUMBER}:
            if min_value is None:
                min_value = Answer.get_extremum(question.id, question.question_type, ExtremumType.MINIMUM)
            if max_value is None:
                max_value = Answer.get_extremum(question.id, question.question_type, ExtremumType.MAXIMUM)
            if step_days is None:
                raise Exception(f"step is not passed as argument while it's required for {question.question_type.name}")
            if min_value is None:
                return []
            if question.question_type == Type.DATE:
                pass
            elif question.question_type == Type.NUMBER:
                pass
        elif question.question_type in {Type.CHECKBOX, Type.MULTIPLE_CHOICE}:
            options = AnswerOption.get_all_from_block(question.answer_block_id)
            return [
                {
                    'name': option.text,
                    'filter': Answer.value_int.in_([option.id])
                } for option in options
            ]
        if question.question_type == Type.USER:
            users = User.get_all_users()
            return [
                {
                    'name': user.name,
                    'filter': Answer.value_int.in_([user.id])
                } for user in users
            ]
        if question.question_type == Type.LOCATION:
            locations = Toponym.get_all()
            return [
                {
                    'name': location.name,
                    'filter': Answer.value_int.in_([location.id])
                } for location in locations
            ]
        if question.question_type == Type.BOOLEAN:
            return [{
                'name': 'False',
                'filter': Answer.value_bool.in_([False])
            }, {
                'name': 'True',
                'filter': Answer.value_bool.in_([True])
            }]
        return []
