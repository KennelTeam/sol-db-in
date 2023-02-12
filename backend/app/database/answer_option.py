#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from typing import List
import json
from .editable import Editable
from backend.constants import MAX_ANSWER_OPTION_SIZE, MAX_LANGUAGES_COUNT, MAX_SHORT_ANSWER_OPTION_SIZE
from backend.auxiliary import TranslatedText, JSON


class AnswerOption(Editable, FlaskApp().db.Model):
    __tablename__ = 'answer_options'
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))
    _short_name = FlaskApp().db.Column('short_name',
                                       FlaskApp().db.Text(MAX_SHORT_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))

    _answer_block_id = FlaskApp().db.Column('answer_block_id', FlaskApp().db.ForeignKey('answer_blocks.id'))

    def __init__(self, name: TranslatedText, short_name: TranslatedText, answer_block_id: int):
        super().__init__()
        self.name = name
        self.short_name = short_name
        self._answer_block_id = answer_block_id

    def to_json(self) -> JSON:
        return super().to_json() | {
            'name': self.name,
            'short_name': self.short_name,
            'answer_block_id': self._answer_block_id
        }

    @staticmethod
    def get_all_from_block(block_id: int) -> List[JSON]:
        return [item.to_json() for item in FlaskApp().request(AnswerOption).filter_by(_answer_block_id=block_id).all()]

    @property
    def answer_block_id(self) -> int:
        return self._answer_block_id

    @property
    def name(self) -> TranslatedText:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: TranslatedText) -> str:
        self._name = json.dumps(new_name)
        return self._name

    @property
    def short_name(self) -> TranslatedText:
        return json.loads(self._short_name)

    @short_name.setter
    @Editable.on_edit
    def short_name(self, new_short_name: TranslatedText) -> str:
        self._short_name = json.dumps(new_short_name)
        return self._short_name
