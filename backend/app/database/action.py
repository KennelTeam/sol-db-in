#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from . import db
from backend.config_loader import ConfigLoader
from sqlalchemy.dialects.mysql import VARCHAR


class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column('id', primary_key=True, unique=True)
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    table_id = db.Column('table_id', VARCHAR(64))
    column_id = db.Column('column_id', VARCHAR(64))
    row_id = db.Column('row_id', db.Integer)
    ip = db.Column('ip', VARCHAR(64))
    timestamp = db.Column('timestamp', db.DateTime)
    value_int = db.Column('value_int', db.Integer)
    value_datetime = db.Column('value_datetime', db.DateTime)
    value_text = db.Column('value_text', db.Text(ConfigLoader.get_config("MAX_TEXT_SIZE")))
    value_boolean = db.Column('value_boolean', db.Boolean)
