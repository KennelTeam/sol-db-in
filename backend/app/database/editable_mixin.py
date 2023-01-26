#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db


class EditableMixin:
    id = db.Column('id', db.Integer, unique=True, primary_key=True)
    create_timestamp = db.Column('create_timestamp', db.DateTime)
    deleted = db.Column('deleted', db.Boolean)
