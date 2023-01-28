#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.config_loader import ConfigLoader


class AnswerOption(EditableMixin, db.Model):
    __tablename__ = 'answer_options'
    name = db.Column('name', db.Text(ConfigLoader.get_config("MAX_ANSWER_OPTION_SIZE")
                                     * ConfigLoader.get_config("MAX_LANGUAGES_COUNT")))

    short_name = db.Column('short_name', db.Text(ConfigLoader.get_config("MAX_SHORT_ANSWER_OPTION_SIZE")
                                                 * ConfigLoader.get_config("MAX_LANGUAGES_COUNT")))
