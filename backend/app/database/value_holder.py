#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from backend.app.flask_app import FlaskApp
from backend.constants import MAX_TEXT_SIZE
from typing import Any
from enum import Enum
from datetime import datetime


class ValueHolder:
    value_int = FlaskApp().db.Column('value_int', FlaskApp().db.Integer, nullable=True)
    value_text = FlaskApp().db.Column('value_text', FlaskApp().db.Text(MAX_TEXT_SIZE), nullable=True)
    value_datetime = FlaskApp().db.Column('value_datetime', FlaskApp().db.DateTime, nullable=True)
    value_bool = FlaskApp().db.Column('value_bool', FlaskApp().db.Boolean, nullable=True)

    @property
    def value(self) -> Any:
        if self.value_datetime is not None:
            return self.value_datetime
        if self.value_bool is not None:
            return self.value_bool
        if self.value_int is not None:
            return self.value_int
        return self.value_text

    def set_value(self, new_value: Any) -> None:

        if isinstance(new_value, bool):
            self.value_bool = new_value
        elif isinstance(new_value, Enum):
            self.value_int = new_value.value
        elif isinstance(new_value, int):
            self.value_int = new_value
        elif isinstance(new_value, str):
            self.value_text = new_value
        elif isinstance(new_value, datetime):
            self.value_datetime = new_value
    
    @value.setter
    def value(self, value: Any) -> None:
        self.set_value(value)
