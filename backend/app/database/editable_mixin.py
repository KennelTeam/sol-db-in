#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from datetime import datetime
from typing import Dict, Any
from .action import Action


class EditableMixin:
    id = db.Column('id', db.Integer, unique=True, primary_key=True)
    create_timestamp = db.Column('create_timestamp', db.DateTime)
    deleted = db.Column('deleted', db.Boolean)

    def __init__(self, fields: Dict[str, Any]) -> None:
        self.create_timestamp = datetime.utcnow()
        self.deleted = False
        for field in fields.keys():
            if field not in {'__tablename__', 'id', 'create_timestamp', 'deleted'}:
                self.edit(fields['__tablename__'], field, fields[field])

    def edit(self, table_id: str, column_id: str, value: Any) -> None:
        act = Action(table_id, column_id, self.id, value)
        db.session.add(act)
