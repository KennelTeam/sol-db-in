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
    _default_filter = FlaskApp().db.Column('default_filter', FlaskApp().db.Boolean(), default=False)
    _cached = None

    def __init__(self, block_sorting: int, block_id: int, table_row: int = None, table_id: int = None,
                 table_column: int = None, show_on_main_page: bool = False, fixed_table_id: int = None,
                 default_filter: bool = None):

        super().__init__()
        self.block_sorting = block_sorting
        self.table_row = table_row
        self.table_column = table_column
        self.show_on_main_page = show_on_main_page

        self._block_id = block_id
        self._table_id = table_id
        self._fixed_table_id = fixed_table_id
        self._default_filter = default_filter

    def to_json(self) -> JSON:
        return super().to_json() | {
            'block_sorting': self.block_sorting,
            'table_row': self.table_row,
            'table_column': self.table_column,
            'show_on_main_page': self.show_on_main_page,
            'block_id': self.block_id,
            'table_id': self.table_id,
            'fixed_table_id': self.fixed_table_id,
            'default_filter': self.default_filter
        }

    @staticmethod
    def upload_cache():
        FormattingSettings._cached = FlaskApp().request(FormattingSettings).all()

    @staticmethod
    def clear_cache():
        FormattingSettings._cached = None

    @staticmethod
    def json_format() -> JSON:
        return {
            'block_sorting': int,
            'block_id': int,
            'show_on_main_page': bool
        }

    def copy(self, other: 'FormattingSettings') -> None:
        self.block_sorting = other.block_sorting
        self.table_row = other.table_row
        self.table_column = other.table_column
        self.show_on_main_page = other.show_on_main_page

    @staticmethod
    def get_by_id(id: int) -> 'FormattingSettings':
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            res = list(filter(lambda x: x.id == id, FormattingSettings._cached))
            return None if len(res) == 0 else res[0]
        return FlaskApp().request(FormattingSettings).filter_by(id=id).first()

    @staticmethod
    def query_from_block(block_id: int) -> Query | List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached:
            return list(filter(lambda x: x._block_id == block_id, FormattingSettings._cached))
        return FlaskApp().request(FormattingSettings).filter_by(_block_id=block_id)

    @staticmethod
    def get_from_question_table(question_table_id: int) -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            return list(filter(lambda x: x._table_id == question_table_id, FormattingSettings._cached))
        return FlaskApp().request(FormattingSettings).filter_by(_table_id=question_table_id).all()

    @staticmethod
    def get_from_fixed_table(fixed_table_id: int) -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            return list(filter(lambda x: x._fixed_table_id == fixed_table_id, FormattingSettings._cached))
        return FlaskApp().request(FormattingSettings).filter_by(_fixed_table_id=fixed_table_id).all()

    @staticmethod
    def get_main_page() -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            return list(filter(lambda x: x._show_on_main_page == True, FormattingSettings._cached))
        return FlaskApp().request(FormattingSettings).filter_by(_show_on_main_page=True).all()

    @staticmethod
    def filter_only_free_questions(query: Query | List['FormattingSettings'],
                                   short_form: bool = False) -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            if short_form:
                query = list(filter(lambda x: x._show_on_main_page == True, query))
            return list(filter(lambda x: x._table_id is None and x._fixed_table_id is None, query))
        if short_form:
            query = query.filter(FormattingSettings._show_on_main_page is True)
        return query.filter(FormattingSettings._table_id == None) \
            .filter(FormattingSettings._fixed_table_id == None).all()

    @staticmethod
    def filter_only_table_questions(query: Query | List['FormattingSettings']) -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            return list(filter(lambda x: x._table_id is not None, query))
        return query.filter(FormattingSettings._table_id is not None).all()

    @staticmethod
    def filter_only_fixed_table_questions(query: Query | List['FormattingSettings']) -> List['FormattingSettings']:
        # pylint: disable=protected-access
        if FormattingSettings._cached is not None:
            return list(filter(lambda x: x._fixed_table_id is not None, query))
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
    def default_filter(self) -> bool:
        return self._default_filter

    @default_filter.setter
    def default_filter(self, new_val: bool) -> None:
        self._default_filter = new_val

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
