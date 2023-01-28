#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_NAME_SIZE
from . import db
from .editable_mixin import EditableMixin


class Leader(EditableMixin, db.Model):
    __tablename__ = 'leaders'
    first_name = db.Column('first_name', db.Text(MAX_NAME_SIZE))
    last_name = db.Column('last_name', db.Text(MAX_NAME_SIZE))
    middle_name = db.Column('middle_name', db.Text(MAX_NAME_SIZE))
