#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from .editable import Editable
from backend.constants import MAX_ANSWER_BLOCK_NAME, MAX_LANGUAGES_COUNT
import json
from typing import Dict, Any, List
from .answer_option import AnswerOption


class AnswerBlock(Editable, FlaskApp().db.Model):
    __tablename__ = 'answer_blocks'
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_ANSWER_BLOCK_NAME * MAX_LANGUAGES_COUNT))

    def __init__(self, name: Dict[str, str]):
        super(Editable).__init__()
        self.name = name

    @staticmethod
    def get_by_id(id: int) -> 'AnswerBlock':
        return AnswerBlock.query.filter_by(id=id).first()

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
