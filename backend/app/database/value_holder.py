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
    
    @value.setter
    def value(self, value: Any) -> None:
        if value is int:
            self.value_int = value
        elif value is Enum:
            self.value_int = value.value
        elif value is str:
            self.value_text = value
        elif value is datetime:
            self.value_datetime = value
        else:
            self.value_bool = value
