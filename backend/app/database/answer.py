#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import sqlalchemy.orm

from backend.app.flask_app import FlaskApp
from .editable_value_holder import EditableValueHolder
from typing import Any, List, Dict


class Answer(EditableValueHolder, FlaskApp().db.Model):
    __tablename__ = 'answers'
    _table_row = FlaskApp().db.Column('table_row', FlaskApp().db.Integer, nullable=True)
    _row_question_id = FlaskApp().db.Column('table_column', FlaskApp().db.ForeignKey('questions.id'), nullable=True)
    _question_id = FlaskApp().db.Column('question_id', FlaskApp().db.ForeignKey('questions.id'))
    _leader_id = FlaskApp().db.Column('leader_id', FlaskApp().db.ForeignKey('leaders.id'), nullable=True)
    _project_id = FlaskApp().db.Column('project_id', FlaskApp().db.ForeignKey('projects.id'), nullable=True)

    def __init__(self, table_row: int, question_id: int, leader_id: int, project_id: int,
                 row_question_id: int, value: Any) -> None:
        super(EditableValueHolder).__init__()
        self._leader_id = leader_id
        self._project_id = project_id
        self._question_id = question_id
        self._table_row = table_row
        self._row_question_id = row_question_id
        self.value = value

    def to_json(self) -> Dict[str, Any]:
        return {
            'leader_id': self.leader_id,
            'project_id': self.project_id,
            'question_id': self.question_id,
            'table_row': self.table_row if self.table_row is not None else 0,
            'row_question_id': self.row_question_id,
            'value': self.value
        }

    @property
    def row_question_id(self):
        return self._row_question_id

    @property
    def table_row(self) -> int:
        return self._table_row

    @property
    def question_id(self) -> int:
        return self._question_id

    @property
    def leader_id(self) -> int:
        return self._leader_id

    @property
    def project_id(self) -> int:
        return self._project_id

    @staticmethod
    def count_leaders_answers(leader_id: int, question_id: int) -> int:
        return Answer.count_distinct_answers(Answer.query.filter_by(_leader_id=leader_id), question_id)

    @staticmethod
    def count_projects_answers(project_id: int, question_id: int) -> int:
        return Answer.count_distinct_answers(Answer.query.filter_by(_project_id=project_id), question_id)

    @staticmethod
    def count_distinct_answers(query: sqlalchemy.orm.Query, question_id: int):
        query = query.filter_by(_question_id=question_id).with_entities(Answer._table_row)
        return len(query.distinct().all())

    @staticmethod
    def filter(question_id: int = None, row_question_id: int = None, leader_id: int = None,
               project_id: int = None, exact_value: Any = None, min_value: Any = None,
               max_value: Any = None, substring: str = None) -> List['Answer']:

        query = EditableValueHolder.filter_by_value(Answer, exact_value=exact_value, min_value=min_value,
                                                    max_value=max_value, substring=substring)
        if question_id is not None:
            query = query.filter_by(_question_id=question_id)
        if row_question_id is not None:
            query = query.filter_by(_row_question_id=row_question_id)
        if leader_id is not None:
            query = query.filter_by(_leader_id=leader_id)
        if project_id is not None:
            query = query.filter_by(_project_id=project_id)
        return query.all()
