#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable import Editable
from typing import Set, List, Tuple
from .question import Question
from .formatting_settings import FormattingSettings

# List of column questions and list of row questions
FixedTable_T = Tuple[List[Question], List[Question]]


class FixedTable(Editable, db.Model):
    __tablename__ = 'fixed_tables'
    _block_sorting = db.Column('block_sorting', db.Integer)

    def __init__(self, block_sorting: int) -> None:
        super(Editable).__init__()
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
        return FixedTable.query.filter(FixedTable.id.in_(ids)).all()

    def get_questions(self) -> FixedTable_T:
        formattings = FormattingSettings.get_from_fixed_table(self.id)
        ids = [item.id for item in formattings]
        formattings_indexed = {item.id: item for item in formattings}
        questions = Question.get_by_ids(ids)

        def get_formatting(q: Question) -> FormattingSettings:
            return formattings_indexed[q.formatting_settings]

        def get_column(q: Question) -> int:
            return get_formatting(q).table_column

        def get_row(q: Question) -> int:
            return get_formatting(q).table_row

        columns = list(filter(lambda q: get_column(q) is not None, questions))
        rows = list(filter(lambda q: get_row(q) is not None, questions))
        columns.sort(key=get_column)
        rows.sort(key=get_row)
        return columns, rows
