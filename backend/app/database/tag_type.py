#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_TAG_SIZE, MAX_LANGUAGES_COUNT
from backend.auxiliary import JSON, TranslatedText
from backend.app.flask_app import FlaskApp
from .localization import localize
from .editable import Editable
from .tag import Tag
from typing import List
import json


class TagType(Editable, FlaskApp().db.Model):
    __tablename__ = 'tag_types'
    _text = FlaskApp().db.Column('text', FlaskApp().db.Text(MAX_TAG_SIZE * MAX_LANGUAGES_COUNT))

    def __init__(self, text: TranslatedText) -> None:
        super().__init__()
        self.text = text

    @staticmethod
    def get_by_id(id: int) -> 'TagType':
        return FlaskApp().request(TagType).filter_by(id=id).first()

    @property
    def text(self) -> TranslatedText:
        return json.loads(self._text)

    @text.setter
    @Editable.on_edit
    def text(self, new_text: TranslatedText) -> str:
        self._text = json.dumps(new_text)
        return self._text

    def get_tags(self) -> List[JSON]:
        return [tag.to_json() for tag in Tag.get_all_of_type(self.id)]

    def get_forest(self) -> List[JSON]:
        return [root.build_tree() for root in Tag.get_roots_of_type(self.id)]

    def to_json(self) -> JSON:
        return super().to_json() | {
            'text': localize(self.text),
            'tags': self.get_forest()
        }

    @staticmethod
    def get_all_names() -> List['TagType']:
        return FlaskApp().request(TagType).all()

    @staticmethod
    def get_all_tag_blocks() -> List[JSON]:
        blocks = FlaskApp().request(TagType).all()
        return [block.to_json() for block in blocks]
