#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from backend.app.flask_app import FlaskApp
from sqlalchemy.dialects.mysql import VARCHAR
from typing import Any, List
from datetime import datetime
from flask_jwt_extended import current_user, jwt_required
from backend.auxiliary import JSON
from .timestamp_range import TimestampRange
from .value_holder import ValueHolder
from ...auxiliary.string_dt import datetime_to_string


class Action(ValueHolder, FlaskApp().db.Model):
    __tablename__ = 'actions'
    id = FlaskApp().db.Column('id', FlaskApp().db.Integer(), primary_key=True, unique=True)
    user_id = FlaskApp().db.Column('user_id', FlaskApp().db.ForeignKey('users.id'))
    table_id = FlaskApp().db.Column('table_id', VARCHAR(64))
    column_id = FlaskApp().db.Column('column_id', VARCHAR(64))
    row_id = FlaskApp().db.Column('row_id', VARCHAR(64))
    ip = FlaskApp().db.Column('ip', VARCHAR(64))
    timestamp = FlaskApp().db.Column('timestamp', FlaskApp().db.DateTime)

    @jwt_required()
    def __init__(self, table_id: str, column_id: str, row_id: str, value: Any) -> None:
        self.user_id = current_user.id
        self.table_id = table_id
        self.column_id = column_id
        self.row_id = row_id
        self.ip = current_user.current_ip
        self.timestamp = datetime.utcnow()
        self.value = value

    def to_json(self) -> JSON:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'table_id': self.table_id,
            'column_id': self.column_id,
            'row_id': self.row_id,
            'ip': self.ip,
            'timestamp': datetime_to_string(self.timestamp),
            'value': self.value
        }

    @staticmethod
    def filter(user_id: int = -1, timestamp_range: TimestampRange = TimestampRange(), table_id: int = -1,
               column_id: str = "", row_id: int = -1, value: Any = None) -> List['Action']:

        query = Action.query
        if user_id != -1:
            query = query.filter_by(user_id=user_id)
        if table_id != -1:
            query = query.filter_by(table_id=table_id)
        if column_id != "":
            query = query.filter_by(column_id=column_id)
        if row_id != -1:
            query = query.filter_by(row_id=row_id)
        if isinstance(value, bool):
            query = query.filter_by(value_boolean=value)
        elif isinstance(value, int):
            query = query.filter_by(value_int=value)
        elif isinstance(value, str):
            query = query.filter_by(value_str=value)
        elif isinstance(value, datetime):
            query = query.filter_by(value_datetime=value)

        query = query.filter(timestamp_range.begin <= Action.timestamp)
        query = query.filter(Action.timestamp <= timestamp_range.end)
        return query.all()
