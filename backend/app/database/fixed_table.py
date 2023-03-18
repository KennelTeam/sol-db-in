#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from typing import Set, List
from .question import Question
from .answer import Answer
from .formatting_settings import FormattingSettings
from backend.app.flask_app import FlaskApp
from .editable import Editable
from backend.auxiliary import JSON


class FixedTable(Editable, FlaskApp().db.Model):
    __tablename__ = 'fixed_tables'
    _block_sorting = FlaskApp().db.Column('block_sorting', FlaskApp().db.Integer)

    def __init__(self, block_sorting: int) -> None:
        super().__init__()
        self._block_sorting = block_sorting

    @property
    def block_sorting(self) -> int:
        return self._block_sorting

    @block_sorting.setter
    @Editable.on_edit
    def block_sorting(self, new_value: int) -> None:
        self._block_sorting = new_value

    @staticmethod
    def get_by_ids(ids: Set[int]) -> List['FixedTable']:
        return FlaskApp().request(FixedTable).filter(FixedTable.id.in_(ids)).all()

    @staticmethod
    def get_by_id(id: int) -> 'FixedTable':
        result = FixedTable.get_by_ids({id})
        if len(result) == 0:
            return None
        return result[0]

    def get_questions(self, with_answers=False, form_id: int = None) -> JSON:
        if not with_answers:
            return self._get_only_questions()
        return self._get_questions_with_answers(form_id)

    def _get_only_questions(self) -> JSON:
        formattings = FormattingSettings.get_from_fixed_table(self.id)
        questions = Question.get_all_with_formattings(formattings)

        def get_formatting(q: Question) -> FormattingSettings:
            return q.formatting_settings

        def get_column(q: Question) -> int:
            return get_formatting(q).table_column

        def get_row(q: Question) -> int:
            return get_formatting(q).table_row

        columns = list(filter(lambda q: get_column(q) is not None, questions))
        rows = list(filter(lambda q: get_row(q) is not None, questions))
        columns.sort(key=get_column)
        rows.sort(key=get_row)
        return {
            'columns': [q.to_json() for q in columns],
            'rows': [q.to_json() for q in rows]
        }

    def _get_questions_with_answers(self, form_id: int = None) -> JSON:
        questions = self._get_only_questions()
        columns = questions['columns']
        rows = questions['rows']
        answers = [[None for _ in columns] for _ in rows]
        for i, r in enumerate(rows):
            for j, c in enumerate(columns):
                options = Answer.filter(c['id'], row_question_id=r['id'], form_id=form_id)
                answers[i][j] = [option.to_json() for option in options]
        return questions | {
            'answers': answers
        }
