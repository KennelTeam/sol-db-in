#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable import Editable
from backend.constants import MAX_ANSWER_BLOCK_NAME, MAX_LANGUAGES_COUNT
import json
from typing import Dict, Any, List
from .answer_option import AnswerOption


class AnswerBlock(Editable, db.Model):
    __tablename__ = 'answer_blocks'
    _name = db.Column('name', db.Text(MAX_ANSWER_BLOCK_NAME * MAX_LANGUAGES_COUNT))

    def __init__(self, name: Dict[str, str]):
        super(Editable).__init__()
        self.name = name

    @property
    def name(self) -> Dict[str, str]:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: Dict[str, str]) -> str:
        self._name = json.dumps(new_name)
        return self._name

    def to_json(self) -> Dict[str, Any]:
        return {
            'options': AnswerOption.get_all_from_block(self.id),
            'name': self.name
        }

    @staticmethod
    def get_all_blocks() -> List[Dict[str, Any]]:
        return [
            block.to_json() for block in AnswerBlock.query.all()
        ]
