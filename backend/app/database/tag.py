#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from config_loader import get_config
from . import db
from .editable_mixin import EditableMixin


class Tag(EditableMixin, db.Model):
    __tablename__ = 'tags'
    text = db.Column('text', db.Text(get_config("MAX_TAG_SIZE") * get_config("MAX_LANGUAGES_COUNT")))
    type_id = db.Column('type_id', db.ForeignKey('tag_types.id'))
    parent_id = db.Column('parent_id', db.ForeignKey('tags.id'), nullable=True)
