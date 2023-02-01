#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_PROJECT_NAME_SIZE
from backend.app.flask_app import FlaskApp
from .form import Form
from .editable import Editable
from sqlalchemy.dialects.mysql import VARCHAR
from typing import Dict, Any
from .question_block import QuestionBlock
from .form_type import FormType


class Project(Form, FlaskApp().db.Model):
    __tablename__ = 'projects'
    _name = FlaskApp().db.Column('name', VARCHAR(MAX_PROJECT_NAME_SIZE), unique=True)

    def __init__(self, name: str):
        super(Form, self).__init__()
        self.name = name

    def to_json(self, short_form: bool = False) -> Dict[str, Any]:
        form = QuestionBlock.get_form(FormType.PROJECT)
        return super(Form).to_json() | {
            'name': self.name,
            'answers': [
                block.get_questions(with_answers=True, form_id=self.id, short_form=short_form) for block in form
            ]
        }

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @Editable.on_edit
    def name(self, new_name: str) -> None:
        self._name = new_name
