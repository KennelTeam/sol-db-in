#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import datetime
from sqlalchemy.orm import Query
from typing import Any, Type
from enum import Enum
from datetime import datetime
from backend.constants import INT_MIN, INT_MAX
from backend.app.flask_app import FlaskApp
from .value_holder import ValueHolder
from .editable import Editable


class EditableValueHolder(ValueHolder, Editable):
    def __init__(self):
        super().__init__()

    @ValueHolder.value.setter
    @Editable.on_edit
    def value(self, value: Any) -> None:
        super().value = value

    @staticmethod
    def filter_by_value(table: Type[FlaskApp().db.Model], exact_value: Any = None, substring: str = None,
                        min_value: Any = None, max_value: Any = None) -> Query:
        if exact_value is not None:
            return EditableValueHolder.filter_exact_value(table, exact_value)
        if substring is not None:
            return EditableValueHolder.filter_substring(table, substring)
        return EditableValueHolder.filter_range(table, min_value, max_value)

    @staticmethod
    def filter_exact_value(table: Type[FlaskApp().db.Model], exact_value: Any) -> Query:
        if exact_value is int or exact_value is Enum:
            return FlaskApp().request(table).filter(table.value_int == exact_value)
        if exact_value is str:
            return FlaskApp().request(table).filter(table.value_text == exact_value)
        if exact_value is bool:
            return FlaskApp().request(table).filter(table.value_bool == exact_value)
        return FlaskApp().request(table).filter(table.value_datetime == exact_value)

    @staticmethod
    def filter_range(table: Type[FlaskApp().db.Model], min_value: Any, max_value: Any) -> Query:
        if min_value is int or max_value is int:
            if min_value is None:
                min_value = INT_MIN
            if max_value is None:
                max_value = INT_MAX
            return FlaskApp().request(table).filter(table.value_int <= max_value).filter(table.value_int >= min_value)
        if min_value is None:
            min_value = datetime.min
        if max_value is None:
            max_value = datetime.max
        return FlaskApp().request(table).filter(table.value_datetime <= max_value)\
            .filter(table.value_datetime >= min_value)

    @staticmethod
    def filter_substring(table: Type[FlaskApp().db.Model], substr: str) -> Query:
        return FlaskApp().request(table).filter(table.value_text.like(f"%{substr}%"))
