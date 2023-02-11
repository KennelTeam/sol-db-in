#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from backend.app.flask_app import FlaskApp
from .editable import Editable
from enum import Enum

from ...auxiliary import JSON


class AccessType(Enum):
    CAN_NOTHING = 1
    CAN_SEE = 2
    CAN_EDIT = 3


class PrivacySettings(Editable, FlaskApp().db.Model):
    __tablename__ = 'privacy_settings'
    _editor_access = FlaskApp().db.Column('editor_access', FlaskApp().db.Enum(AccessType))
    _intern_access = FlaskApp().db.Column('intern_access', FlaskApp().db.Enum(AccessType))
    _guest_access = FlaskApp().db.Column('guest_access', FlaskApp().db.Enum(AccessType))

    def __init__(self, editor_access: AccessType, intern_access: AccessType, guest_access: AccessType) -> None:
        super(Editable).__init__()
        self.editor_access = editor_access
        self.guest_access = guest_access
        self.intern_access = intern_access

    def to_json(self) -> JSON:
        return super(Editable).to_json() | {
            "editor_access": self.editor_access.name,
            "guest_access": self.guest_access.name,
            "intern_access": self.intern_access.name
        }

    @staticmethod
    def get_by_id(id: int):
        return FlaskApp().request(PrivacySettings).filter_by(id=id).first()

    @property
    def editor_access(self) -> AccessType:
        return self._editor_access

    @editor_access.setter
    @Editable.on_edit
    def editor_access(self, new_access: AccessType) -> None:
        self._editor_access = new_access

    @property
    def intern_access(self) -> AccessType:
        return self._intern_access

    @intern_access.setter
    @Editable.on_edit
    def intern_access(self, new_access: AccessType) -> None:
        self._intern_access = new_access

    @property
    def guest_access(self) -> AccessType:
        return self._guest_access

    @guest_access.setter
    @Editable.on_edit
    def guest_access(self, new_access: AccessType) -> None:
        self._guest_access = new_access
