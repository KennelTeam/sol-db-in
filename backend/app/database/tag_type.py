#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from .tag import Tag
from typing import List, Dict, Any


class TagType(EditableMixin, db.Model):
    __tablename__ = 'tag_types'
    text = db.Column('text', db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))

    def __init__(self, text: str) -> None:
        self.text = text
        super(EditableMixin).__init__(self.__dict__)

    def set_text(self, text: str) -> None:
        super(EditableMixin).edit(TagType.__tablename__, 'text', text)
        self.text = text

    def get_tags(self) -> List[Tag]:
        query = Tag.query.filter_by(type_id=self.id)
        return [tag.to_json() for tag in query.all()]

    def to_json(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'tags': self.get_tags()
        }

    @staticmethod
    def get_all_names() -> List['TagType']:
        return TagType.query.all()
