#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from sqlalchemy.orm import Query
from typing import List
from backend.app.flask_app import FlaskApp
from .editable import Editable
from backend.auxiliary import JSON


class FormattingSettings(Editable, FlaskApp().db.Model):
    __tablename__ = 'formatting_settings'

    _block_sorting = FlaskApp().db.Column('block_sorting', FlaskApp().db.Integer)
    _table_column = FlaskApp().db.Column('table_column', FlaskApp().db.Integer, nullable=True)
    _table_row = FlaskApp().db.Column('table_row', FlaskApp().db.Integer, nullable=True)
    _show_on_main_page = FlaskApp().db.Column('show_on_main_page', FlaskApp().db.Boolean)
    _block_id = FlaskApp().db.Column('block_id', FlaskApp().db.ForeignKey('question_blocks.id'), nullable=True,
                                     default=None)
    _table_id = FlaskApp().db.Column('table_id', FlaskApp().db.ForeignKey('question_tables.id'), nullable=True,
                                     default=None)
    _fixed_table_id = FlaskApp().db.Column('fixed_table_id', FlaskApp().db.ForeignKey('fixed_tables.id'), nullable=True,
                                           default=None)

    def __init__(self, block_sorting: int, block_id: int, table_row: int = 0, table_id: int = None,
                 table_column: int = None, show_on_main_page: bool = False, fixed_table_id: int = None):

        super().__init__()
        self.block_sorting = block_sorting
        self.table_row = table_row
        self.table_column = table_column
        self.show_on_main_page = show_on_main_page

        self._block_id = block_id
        self._table_id = table_id
        self._fixed_table_id = fixed_table_id

    def to_json(self) -> JSON:
        return super().to_json() | {
            'block_sorting': self.block_sorting,
            'table_row': self.table_row,
            'table_column': self.table_column,
            'show_on_main_page': self.show_on_main_page,
            'block_id': self.block_id,
            'table_id': self.table_id,
            'fixed_table_id': self.fixed_table_id
        }

    @staticmethod
    def get_by_id(id: int) -> 'FormattingSettings':
        return FlaskApp().request(FormattingSettings).filter_by(id=id).first()

    @staticmethod
    def query_from_block(block_id: int) -> Query:
        return FlaskApp().request(FormattingSettings).filter_by(_block_id=block_id)

    @staticmethod
    def get_from_question_table(question_table_id: int) -> List['FormattingSettings']:
        return FlaskApp().request(FormattingSettings).filter_by(_table_id=question_table_id).all()

    @staticmethod
    def get_from_fixed_table(fixed_table_id: int) -> List['FormattingSettings']:
        return FlaskApp().request(FormattingSettings).filter_by(_fixed_table_id=fixed_table_id).all()

    @staticmethod
    def filter_only_free_questions(query: Query, short_form: bool = False) -> List['FormattingSettings']:
        if short_form:
            query = query.filter(FormattingSettings._show_on_main_page is True)
        return query.filter(FormattingSettings.table_id is None) \
            .filter(FormattingSettings._fixed_table_id is None).all()

    @staticmethod
    def filter_only_table_questions(query: Query) -> List['FormattingSettings']:
        return query.filter(FormattingSettings._table_id is not None).all()

    @staticmethod
    def filter_only_fixed_table_questions(query: Query) -> List['FormattingSettings']:
        return query.filter(FormattingSettings._fixed_table_id is not None).all()

    @property
    def show_on_main_page(self) -> bool:
        return self._show_on_main_page

    @show_on_main_page.setter
    @Editable.on_edit
    def show_on_main_page(self, value: bool) -> None:
        self._show_on_main_page = value

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
