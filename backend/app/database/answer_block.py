#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.constants import MAX_ANSWER_BLOCK_NAME


class AnswerBlock(EditableMixin, db.Model):
    __tablename__ = 'answer_blocks'
    name = db.Column('name', db.Text(MAX_ANSWER_BLOCK_NAME))
