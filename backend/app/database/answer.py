#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from sqlalchemy.orm import Query
from backend.app.flask_app import FlaskApp
from .tag_to_answer import TagToAnswer
from .editable_value_holder import EditableValueHolder
from enum import Enum
from typing import Any, List, Set
from .question_type import QuestionType
from backend.auxiliary import JSON


class ExtremumType(Enum):
    MINIMUM = 1
    MAXIMUM = 2


class Answer(EditableValueHolder, FlaskApp().db.Model):
    __tablename__ = 'answers'
    _table_row = FlaskApp().db.Column('table_row', FlaskApp().db.Integer, nullable=True)
    _row_question_id = FlaskApp().db.Column('row_question_id', FlaskApp().db.Integer, nullable=True)
    _question_id = FlaskApp().db.Column('question_id', FlaskApp().db.ForeignKey('questions.id'))
    _form_id = FlaskApp().db.Column('form_id', FlaskApp().db.ForeignKey('forms.id'), nullable=False)

    def __init__(self, question_id: int, form_id: int,
                 value: Any, table_row: int, row_question_id: int) -> None:
        super().__init__()
        self._form_id = form_id
        self._question_id = question_id
        self._table_row = table_row
        self._row_question_id = row_question_id
        self.value = value

    def to_json(self) -> JSON:
        return super().to_json() | {
            'form_id': self.form_id,
            'question_id': self.question_id,
            'table_row': self.table_row if self.table_row is not None else 0,
            'row_question_id': self.row_question_id,
            'tags': TagToAnswer.get_answers_tags(self.id),
            'value': self.value
        }

    @staticmethod
    def json_format() -> JSON:
        return {
            'question_id': int,
            'table_row': int,
            'row_question_id': int,
            'value': {int, str, bool},
            'tags': list,
        }

    @staticmethod
    def get_by_id(id: int) -> 'Answer':
        return FlaskApp().request(Answer).filter_by(id=id).first()

    @staticmethod
    def query_for_question_ids(question_ids: Set[int]) -> Query:
        return FlaskApp().request(Answer).filter(Answer._question_id.in_(question_ids))

    @staticmethod
    def query_question_grouped_by_forms(question_id: int) -> Query:
        return FlaskApp().request(Answer).filter_by(question_id=question_id)\
            .group_by(Answer._form_id).with_entities(Answer._form_id)

    @staticmethod
    def count_with_condition(ids: List[int], condition) -> int:
        query = FlaskApp().request(Answer).filter(condition)
        query = query.filter(Answer._form_id.in_(ids)).distinct(Answer._form_id)
        return query.count()

    @staticmethod
    def get_extremum(question_id: int, question_type: QuestionType, extremum: ExtremumType):
        if question_type == QuestionType.NUMBER:
            sorting = Answer.value_int.desc() if extremum == ExtremumType.MINIMUM else Answer.value_int.asc()
        else:
            sorting = Answer.value_datetime.desc() if extremum == ExtremumType.MINIMUM else Answer.value_datetime.asc()
        item = FlaskApp().request(Answer).filter_by(question_id=question_id).order_by(sorting).first()
        if item is None:
            return None
        return item.value_datetime if question_type == QuestionType.DATE else item.value_int

    @staticmethod
    def get_form_answers(form_id: int, question_id: int = -1) -> List['Answer']:
        query = FlaskApp().request(Answer).filter_by(_form_id=form_id)
        if question_id != -1:
            query = query.filter_by(_question_id=question_id)
        return query.all()

    @staticmethod
    def count_forms_answers(form_id: int, question_id: int) -> int:
        return Answer.count_distinct_answers(FlaskApp().request(Answer).filter_by(_form_id=form_id), question_id)

    @staticmethod
    def count_inverse_answers(form_id: int, question_id: int) -> int:
        return Answer.count_distinct_answers(FlaskApp().request(Answer).filter_by(value_int=form_id), question_id)

    @staticmethod
    def count_distinct_answers(query: Query, question_id: int):
        query = query.filter_by(_question_id=question_id)
        return query.distinct().count()

    @staticmethod
    def filter(question_id: int = None, row_question_id: int = None, form_id: int = None,
               exact_values: List[Any] = None, min_value: Any = None,
               max_value: Any = None, substring: str = None) -> List['Answer']:

        return Answer._filter_query(question_id, row_question_id, form_id,
                                    exact_values, min_value, max_value, substring).all()

    @staticmethod
    def get_distinct_filtered(question_id: int, exact_values: List[Any], min_value: Any,
                              max_value: Any, substring: str, row_question_id: int) -> List[int]:

        query = Answer._filter_query(question_id, row_question_id=row_question_id, exact_values=exact_values,
                                     min_value=min_value, max_value=max_value, substring=substring)

        answers = query.with_entities(Answer._form_id).distinct(Answer._form_id).all()
        return [item.form_id for item in answers]

    @staticmethod
    def _filter_query(question_id: int = None, row_question_id: int = None, form_id: int = None,
                      exact_values: List[Any] = None, min_value: Any = None,
                      max_value: Any = None, substring: str = None) -> Query:

        query = EditableValueHolder.filter_by_value(Answer, exact_values=exact_values, min_value=min_value,
                                                    max_value=max_value, substring=substring)
        if question_id is not None:
            query = query.filter_by(_question_id=question_id)
        if row_question_id is not None:
            query = query.filter_by(_row_question_id=row_question_id)
        if form_id is not None:
            query = query.filter_by(_form_id=form_id)
        return query

    @property
    def row_question_id(self):
        return self._row_question_id

    @property
    def table_row(self) -> int:
        return self._table_row

    @table_row.setter
    @EditableValueHolder.on_edit
    def table_row(self, value: int) -> None:
        self._table_row = value

    @property
    def question_id(self) -> int:
        return self._question_id

    @property
    def form_id(self) -> int:
        return self._form_id
