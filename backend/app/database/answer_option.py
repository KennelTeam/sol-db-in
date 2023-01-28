#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.constants import MAX_ANSWER_OPTION_SIZE, MAX_LANGUAGES_COUNT, MAX_SHORT_ANSWER_OPTION_SIZE


class AnswerOption(EditableMixin, db.Model):
    __tablename__ = 'answer_options'
    name = db.Column('name', db.Text(MAX_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))
    short_name = db.Column('short_name', db.Text(MAX_SHORT_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))
