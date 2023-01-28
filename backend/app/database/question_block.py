#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_BLOCK_NAME_SIZE
from . import db
from .editable_mixin import EditableMixin


form_types = {
    'Leader': 1,
    'Project': 2
}


class QuestionBlock(EditableMixin, db.Model):
    __tablename__ = 'question_blocks'
    form = db.Column('form', db.Integer)
    name = db.Column('name', db.Text(MAX_BLOCK_NAME_SIZE))
    sorting = db.Column('sorting', db.Integer)
