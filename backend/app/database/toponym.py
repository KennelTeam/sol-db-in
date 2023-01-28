#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from backend.config_loader import ConfigLoader


class Toponym(db.Model):
    __tablename__ = 'toponyms'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    name = db.Column('name', db.Text(ConfigLoader.get_config("MAX_TOPONYM_SIZE")))
    parent_id = db.Column('parent_id', db.ForeignKey('toponyms.id'), nullable=True, default=None)
