#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Dict, Any

from backend.app.flask_app import FlaskApp
from .editable import Editable
from enum import Enum


class FormState(Enum):
    PLANNED = 1
    STARTED = 2
    FINISHED = 3


class Form(Editable):
    _state = FlaskApp().db.Column('state', FlaskApp().db.Enum(FormState))

    def __init__(self, state=FormState.PLANNED):
        super(Editable).__init__()
        self.state = state

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'state': self.state
        }

    @property
    def state(self) -> FormState:
        return self._state

    @state.setter
    @Editable.on_edit
    def state(self, new_state: FormState) -> None:
        self._state = new_state
