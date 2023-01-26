#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from config_loader import get_config


class TagType(EditableMixin, db.Model):
    __tablename__ = 'tag_types'
    text = db.Column('text', db.Text(get_config("MAX_TAG_SIZE") * get_config("MAX_LANGUAGES_COUNT")))
