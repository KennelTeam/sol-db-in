#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from .action import Action
from backend.auxiliary import JSON
from datetime import datetime
from typing import Any


class Editable:
    id = FlaskApp().db.Column('id', FlaskApp().db.Integer, unique=True, primary_key=True)
    create_timestamp = FlaskApp().db.Column('create_timestamp', FlaskApp().db.DateTime)
    _deleted = FlaskApp().db.Column('deleted', FlaskApp().db.Boolean)

    def __init__(self) -> None:
        self.create_timestamp = datetime.utcnow()
        self._deleted = False

    @property
    def deleted(self):
        return self._deleted

    @deleted.setter
    def deleted(self, value: bool):
        self.edit('deleted', value, self.__dict__['__tablename__'])  # so strange method of getting the tablename
        # because it is not in editable, but supposed to be in derived classes (which are FlaskApp().db.Models)
        self._deleted = value

    def edit(self, column_id: str, value: Any, table_id: str = "") -> None:
        act = Action(table_id, column_id, self.id, value)
        FlaskApp().db.session.add(act)

    def to_json(self) -> JSON:
        return {
            'id': self.id,
            'create_timestamp': self.create_timestamp,
            'deleted': self._deleted
        }

    # on_edit decorator should wrap setters for the database column properties of ORM classes
    # since they are setters their names should be the same as columns' names
    # if the stored value differs from the argument of the function,
    # the setter should return the actual stored value
    @staticmethod
    def on_edit(func):
        def wrapper(self, value):
            result = func(self, value)
            if result is None:
                self.edit(func.__name__, value, self.__tablename__)
            else:
                self.edit(func.__name__, result, self.__tablename__)
        return wrapper
