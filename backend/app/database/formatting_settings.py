#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import sqlalchemy.orm
from typing import List
from . import db
from .editable import Editable


class FormattingSettings(Editable, db.Model):
    __tablename__ = 'formatting_settings'

    _block_sorting = db.Column('block_sorting', db.Integer)
    _table_column = db.Column('table_column', db.Integer, nullable=True)
    _table_row = db.Column('table_row', db.Integer, nullable=True)
    _block_id = db.Column('block_id', db.ForeignKey('question_blocks.id'), nullable=True, default=None)
    _table_id = db.Column('table_id', db.ForeignKey('question_tables.id'), nullable=True, default=None)
    _fixed_table_id = db.Column('fixed_table_id', db.ForeignKey('fixed_tables.id'), nullable=True, default=None)

    def __init__(self, block_sorting: int, block_id: int, table_row: int = 0, table_id: int = None,
                 table_column: int = None, fixed_table_id: int = None):

        super(Editable).__init__()
        self.block_sorting = block_sorting
        self.table_row = table_row
        self.table_column = table_column

        self._block_id = block_id
        self._table_id = table_id
        self._fixed_table_id = fixed_table_id

    @staticmethod
    def get_by_id(id: int) -> 'FormattingSettings':
        return FormattingSettings.query.filter_by(id=id).first()

    @staticmethod
    def query_from_block(block_id: int) -> sqlalchemy.orm.Query:
        return FormattingSettings.query.filter_by(_block_id=block_id)

    @staticmethod
    def get_from_question_table(question_table_id: int) -> List['FormattingSettings']:
        return FormattingSettings.query.filter_by(_table_id=question_table_id).all()

    @staticmethod
    def get_from_fixed_table(fixed_table_id: int) -> List['FormattingSettings']:
        return FormattingSettings.query.filter_by(_fixed_table_id=fixed_table_id).all()

    @staticmethod
    def filter_only_free_questions(query: sqlalchemy.orm.Query) -> List['FormattingSettings']:
        return query.filter(FormattingSettings.table_id is None).filter(FormattingSettings._fixed_table_id is None).all()

    @staticmethod
    def filter_only_table_questions(query: sqlalchemy.orm.Query) -> List['FormattingSettings']:
        return query.filter(FormattingSettings._table_id is not None).all()

    @staticmethod
    def filter_only_fixed_table(query: sqlalchemy.orm.Query) -> List['FormattingSettings']:
        return query.filter(FormattingSettings._fixed_table_id is not None).all()

    @property
    def block_id(self) -> int:
        return self._block_id

    @property
    def block_sorting(self) -> int:
        return self._block_sorting

    @block_sorting.setter
    @Editable.on_edit
    def block_sorting(self, new_value: int) -> None:
        self._block_sorting = new_value

    @property
    def table_column(self) -> int:
        return self._table_column

    @table_column.setter
    @Editable.on_edit
    def table_column(self, new_col: int) -> None:
        self._table_column = new_col

    @property
    def table_id(self) -> int:
        return self._table_id

    @property
    def table_row(self) -> int:
        return self._table_row

    @table_row.setter
    @Editable.on_edit
    def table_row(self, new_row: int) -> None:
        self._table_row = new_row

    @property
    def fixed_table_id(self) -> int:
        return self._fixed_table_id
