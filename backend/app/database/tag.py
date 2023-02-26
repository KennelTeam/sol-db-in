#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from backend.auxiliary import JSON, TranslatedText
from backend.app.flask_app import FlaskApp
from .editable import Editable
from typing import List
import json


class Tag(Editable, FlaskApp().db.Model):
    __tablename__ = 'tags'
    _text = FlaskApp().db.Column('text', FlaskApp().db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))
    _type_id = FlaskApp().db.Column('type_id', FlaskApp().db.ForeignKey('tag_types.id'))
    _parent_id = FlaskApp().db.Column('parent_id', FlaskApp().db.ForeignKey('tags.id'), nullable=True)

    def __init__(self, text: TranslatedText, type_id: int, parent_id: int = None) -> None:
        super().__init__()
        self.text = text
        self._type_id = type_id
        self._parent_id = parent_id

    def to_json(self) -> JSON:
        return super().to_json() | {
            'text': self.text,
            'type_id': self.type_id,
            'parent_id': self.parent_id
        }

    @staticmethod
    def get_by_id(id: int) -> 'Tag':
        return FlaskApp().request(Tag).filter_by(id=id).first()

    @property
    def text(self) -> JSON:
        return json.loads(self._text)

    @text.setter
    @Editable.on_edit
    def text(self, new_text: JSON):
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
        return FlaskApp().request(Tag).filter_by(_parent_id=self.id).all()

    def build_tree(self) -> JSON:
        result = self.to_json()
        result['children'] = []
        for child in self.children:
            result['children'].append(child.build_tree())
        return result

    @staticmethod
    def get_all_of_type(type_id: int) -> List['Tag']:
        return FlaskApp().request(Tag).filter_by(_type_id=type_id).all()

    @staticmethod
    def get_roots_of_type(type_id: int) -> List['Tag']:
        return FlaskApp().request(Tag).filter_by(_type_id=type_id).filter_by(_parent_id=None).all()

    def get_ancestors(self) -> List['Tag']:
        result = [self]
        current = self.parent_id

        # not sure about correctness of this check: int NULL value might be 0 - IDK
        while current is not None:
            node = FlaskApp().request(Tag).filter_by(id=current)
            result.append(node)
            current = node.parent_id
        return result
