#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable import Editable
from backend.constants import MAX_ANSWER_OPTION_SIZE, MAX_LANGUAGES_COUNT, MAX_SHORT_ANSWER_OPTION_SIZE
from typing import Dict, Any, List
import json


class AnswerOption(Editable, db.Model):
    __tablename__ = 'answer_options'
    _name = db.Column('name', db.Text(MAX_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))
    _short_name = db.Column('short_name', db.Text(MAX_SHORT_ANSWER_OPTION_SIZE * MAX_LANGUAGES_COUNT))
    _answer_block_id = db.Column('answer_block_id', db.ForeignKey('answer_blocks.id'))

    def __init__(self, name: Dict[str, str], short_name: Dict[str, str], answer_block_id: int):
        super(Editable).__init__()
        self.name = name
        self.short_name = short_name
        self._answer_block_id = answer_block_id

    @staticmethod
    def get_all_from_block(block_id: int) -> List['AnswerOption']:
        return AnswerOption.query.filter_by(_answer_block_id=block_id).all()

    @property
    def answer_block_id(self) -> int:
        return self._answer_block_id

    @property
    def name(self) -> Dict[str, str]:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: Dict[str, str]) -> str:
        self._name = json.dumps(new_name)
        return self._name

    @property
    def short_name(self) -> Dict[str, str]:
        return json.loads(self._short_name)

    @short_name.setter
    @Editable.on_edit
    def short_name(self, new_short_name: Dict[str, str]) -> str:
        self._short_name = json.dumps(new_short_name)
        return self._short_name
