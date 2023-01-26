#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from config_loader import get_config
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR


class Project(EditableMixin, db.Model):
    __tablename__ = 'projects'
    name = db.Column('name', db.Text(get_config("MAX_PROJECT_NAME_SIZE")))
    name_hash = db.Column('name_hash', VARCHAR(512//8, charset='utf8'), unique=True)

