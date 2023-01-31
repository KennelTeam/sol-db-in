#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from . import db
from .editable import Editable
from typing import List, Dict, Any
import json


class Tag(Editable, db.Model):
    __tablename__ = 'tags'
    _text = db.Column('text', db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))
    _type_id = db.Column('type_id', db.ForeignKey('tag_types.id'))
    _parent_id = db.Column('parent_id', db.ForeignKey('tags.id'), nullable=True)

    def __init__(self, text: Dict[str, str], type_id: int, parent_id: int = None) -> None:
        super(Editable).__init__()
        self.text = text
        self._type_id = type_id
        self._parent_id = parent_id

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'text': self.text,
            'type_id': self.type_id,
            'parent_id': self.parent_id
        }

    @property
    def text(self) -> Dict[str, str]:
        return json.loads(self._text)

    @text.setter
    @Editable.on_edit
    def text(self, new_text: Dict[str, str]):
        self._text = json.dumps(new_text)
        return self._text

    @property
    def type_id(self) -> int:
        return self._type_id

    @property
    def parent_id(self):
        return self._parent_id

    @property
    def children(self) -> List['Tag']:
        return Tag.query.filter_by(_parent_id=self.id).all()

    def build_tree(self) -> Dict[str, Any]:
        result = self.to_json()
        result['children'] = []
        for child in self.children:
            result['children'].append(child.build_tree())
        return result

    @staticmethod
    def get_all_of_type(type_id: int) -> List['Tag']:
        return Tag.query.filter_by(_type_id=type_id).all()

    @staticmethod
    def get_roots_of_type(type_id: int) -> List['Tag']:
        return Tag.query.filter_by(_type_id=type_id).filter_by(_parent_id=None).all()

    def get_ancestors(self) -> List['Tag']:
        result = [self]
        current = self.parent_id

        # not sure about correctness of this check: int NULL value might be 0 - IDK
        while current is not None:
            node = Tag.query.filter_by(id=current)
            result.append(node)
            current = node.parent_id
        return result
