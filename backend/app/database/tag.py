#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from . import db
from .editable_mixin import EditableMixin


class Tag(EditableMixin, db.Model):
    __tablename__ = 'tags'
    text = db.Column('text', db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))
    type_id = db.Column('type_id', db.ForeignKey('tag_types.id'))
    parent_id = db.Column('parent_id', db.ForeignKey('tags.id'), nullable=True)
