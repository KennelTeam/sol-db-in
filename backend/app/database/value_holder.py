#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from . import db
from backend.constants import MAX_TEXT_SIZE
from typing import Any
from enum import Enum
from datetime import datetime


class ValueHolder:
    value_int = db.Column('value_int', db.Integer, nullable=True)
    value_text = db.Column('value_text', db.Text(MAX_TEXT_SIZE), nullable=True)
    value_datetime = db.Column('value_datetime', db.DateTime, nullable=True)
    value_bool = db.Column('value_bool', db.Boolean, nullable=True)

    def set(self, value: Any) -> None:
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

    def get(self) -> Any:
        if self.value_datetime is not None:
            return self.value_datetime
        if self.value_bool is not None:
            return self.value_bool
        if self.value_int is not None:
            return self.value_int
        return self.value_text
