#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
import json
from typing import List
from .answer_option import AnswerOption
from .localization import localize
from .editable import Editable
from backend.constants import MAX_ANSWER_BLOCK_NAME, MAX_LANGUAGES_COUNT
from backend.auxiliary import TranslatedText, JSON


class AnswerBlock(Editable, FlaskApp().db.Model):
    __tablename__ = 'answer_blocks'
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_ANSWER_BLOCK_NAME * MAX_LANGUAGES_COUNT))

    def __init__(self, name: TranslatedText):
        super().__init__()
        self.name = name

    @staticmethod
    def get_by_id(id: int) -> 'AnswerBlock':
        return FlaskApp().request(AnswerBlock).filter_by(id=id).first()

    @property
    def name(self) -> TranslatedText:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: TranslatedText) -> str:
        self._name = json.dumps(new_name)
        return self._name

    def to_json(self) -> JSON:
        return super().to_json() | {
            'options': AnswerOption.get_all_from_block(self.id),
            'name': localize(self.name)
        }

    @staticmethod
    def get_all_blocks() -> List[JSON]:
        return [
            block.to_json() for block in FlaskApp().request(AnswerBlock).all()
        ]
