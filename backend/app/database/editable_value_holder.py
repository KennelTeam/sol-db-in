#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import datetime

import sqlalchemy.orm

from .value_holder import ValueHolder
from .editable import Editable
from typing import Any
from enum import Enum
from backend.constants import INT_MIN, INT_MAX
from datetime import datetime
from backend.app.flask_app import FlaskApp


class EditableValueHolder(ValueHolder, Editable):
    def __init__(self):
        super(Editable).__init__()

    @ValueHolder.value.setter
    @Editable.on_edit
    def value(self, value: Any) -> None:
        super(ValueHolder).value = value

    @staticmethod
    def filter_by_value(table: FlaskApp().db.Model, exact_value: Any = None, substring: str = None,
                        min_value: Any = None, max_value: Any = None) -> sqlalchemy.orm.Query:
        if exact_value is not None:
            return EditableValueHolder.filter_exact_value(table, exact_value)
        if substring is not None:
            return EditableValueHolder.filter_substring(table, substring)
        return EditableValueHolder.filter_range(table, min_value, max_value)

    @staticmethod
    def filter_exact_value(table: FlaskApp().db.Model, exact_value: Any) -> sqlalchemy.orm.Query:
        if exact_value is int or exact_value is Enum:
            return table.query.filter(table.value_int == exact_value)
        if exact_value is str:
            return table.query.filter(table.value_text == exact_value)
        if exact_value is bool:
            return table.query.filter(table.value_bool == exact_value)
        return table.query.filter(table.value_datetime == exact_value)

    @staticmethod
    def filter_range(table: FlaskApp().db.Model, min_value: Any, max_value: Any) -> sqlalchemy.orm.Query:
        if min_value is int or max_value is int:
            if min_value is None:
                min_value = INT_MIN
            if max_value is None:
                max_value = INT_MAX
            return table.query.filter(table.value_int <= max_value).filter(table.value_int >= min_value)
        if min_value is None:
            min_value = datetime.min
        if max_value is None:
            max_value = datetime.max
        return table.query.filter(table.value_datetime <= max_value).filter(table.value_datetime >= min_value)

    @staticmethod
    def filter_substring(table: FlaskApp().db.Model, substr: str) -> sqlalchemy.orm.Query:
        return table.query.filter(table.value_text.like(f"%{substr}%"))
