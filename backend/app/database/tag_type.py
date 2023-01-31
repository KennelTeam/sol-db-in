#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable import Editable
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from .tag import Tag
from typing import List, Dict, Any


class TagType(Editable, db.Model):
    __tablename__ = 'tag_types'
    _text = db.Column('text', db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))

    def __init__(self, text: str) -> None:
        super(Editable).__init__()
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    @Editable.on_edit
    def text(self, new_text: str) -> None:
        self._text = new_text

    def get_tags(self) -> List[Dict[str, Any]]:
        return [tag.to_json() for tag in Tag.get_all_of_type(self.id)]

    def get_forest(self) -> List[Dict[str, Any]]:
        return [root.build_tree() for root in Tag.get_roots_of_type(self.id)]

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'text': self.text,
            'tags': self.get_tags()
        }

    @staticmethod
    def get_all_names() -> List['TagType']:
        return TagType.query.all()

    @staticmethod
    def get_all_tag_blocks() -> List[Dict[str, List[Dict[str, Any]]]]:
        blocks = TagType.query.all()
        return [block.get_forest() for block in blocks]
