#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import datetime

from . import db
from sqlalchemy.dialects.mysql import VARCHAR
from typing import Any, List
from datetime import datetime
from flask_jwt_extended import current_user
from .timestamp_range import TimestampRange
from .value_holder import ValueHolder


class Action(ValueHolder, db.Model):
    __tablename__ = 'actions'
    id = db.Column('id', primary_key=True, unique=True)
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    table_id = db.Column('table_id', VARCHAR(64))
    column_id = db.Column('column_id', VARCHAR(64))
    row_id = db.Column('row_id', db.Integer)
    ip = db.Column('ip', VARCHAR(64))
    timestamp = db.Column('timestamp', db.DateTime)

    def __init__(self, table_id: str, column_id: str, row_id: str, value: Any) -> None:
        self.user_id = current_user.id
        self.table_id = table_id
        self.column_id = column_id
        self.row_id = row_id
        self.ip = current_user.current_ip
        self.timestamp = datetime.utcnow()
        self.set(value)

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

        if value is int:
            query = query.filter_by(value_int=value)
        elif value is str:
            query = query.filter_by(value_str=value)
        elif value is datetime.datetime:
            query = query.filter_by(value_datetime=value)
        elif value is bool:
            query = query.filter_by(value_boolean=value)

        query = query.filter(timestamp_range.begin <= Action.timestamp)
        query = query.filter(Action.timestamp <= timestamp_range.end)
        return query.all()
