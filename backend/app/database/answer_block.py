#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from config_loader import get_config


class AnswerBlock(EditableMixin, db.Model):
    __tablename__ = 'answer_blocks'
    name = db.Column('name', db.Text(get_config("MAX_ANSWER_BLOCK_NAME")))
