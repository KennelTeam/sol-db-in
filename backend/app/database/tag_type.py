#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.config_loader import ConfigLoader


class TagType(EditableMixin, db.Model):
    __tablename__ = 'tag_types'
    text = db.Column('text', db.Text(ConfigLoader.get_config("MAX_TAG_SIZE")
                                     * ConfigLoader.get_config("MAX_LANGUAGES_COUNT")))
