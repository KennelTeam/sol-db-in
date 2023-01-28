#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.config_loader import ConfigLoader
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR


class Project(EditableMixin, db.Model):
    __tablename__ = 'projects'
    name = db.Column('name', VARCHAR(ConfigLoader.get_config("MAX_PROJECT_NAME_SIZE")), unique=True)

