#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from config_loader import get_config


class AnswerOption(EditableMixin, db.Model):
    __tablename__ = 'answer_options'
    name = db.Column('name', db.Text(get_config("MAX_ANSWER_OPTION_SIZE") * get_config("MAX_LANGUAGES_COUNT")))
    short_name = db.Column('short_name', db.Text(get_config("MAX_SHORT_ANSWER_OPTION_SIZE")
                                                 * get_config("MAX_LANGUAGES_COUNT")))
