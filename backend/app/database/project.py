#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_PROJECT_NAME_SIZE
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR


class Project(EditableMixin, db.Model):
    __tablename__ = 'projects'
    name = db.Column('name', VARCHAR(MAX_PROJECT_NAME_SIZE), unique=True)

