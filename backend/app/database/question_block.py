#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.config_loader import ConfigLoader
from . import db
from .editable_mixin import EditableMixin


form_types = {
    'Leader': 1,
    'Project': 2
}


class QuestionBlock(EditableMixin, db.Model):
    __tablename__ = 'question_blocks'
    form = db.Column('form', db.Integer)
    name = db.Column('name', db.Text(ConfigLoader.get_config("MAX_BLOCK_NAME_SIZE")))
    sorting = db.Column('sorting', db.Integer)
