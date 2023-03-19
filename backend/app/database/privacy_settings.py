#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Set

from backend.app.flask_app import FlaskApp
from .editable import Editable
from enum import Enum

from ...auxiliary import JSON


class AccessType(Enum):
    CAN_NOTHING = 1
    CAN_SEE = 2
    CAN_EDIT = 3

    @staticmethod
    def items() -> Set[str]:
        return set(AccessType.__members__.keys())


class PrivacySettings(Editable, FlaskApp().db.Model):
    __tablename__ = 'privacy_settings'
    _editor_access = FlaskApp().db.Column('editor_access', FlaskApp().db.Enum(AccessType))
    _intern_access = FlaskApp().db.Column('intern_access', FlaskApp().db.Enum(AccessType))
    _guest_access = FlaskApp().db.Column('guest_access', FlaskApp().db.Enum(AccessType))

    _cached = None

    def __init__(self, editor_access: AccessType, intern_access: AccessType, guest_access: AccessType) -> None:
        super().__init__()
        self.editor_access = editor_access
        self.guest_access = guest_access
        self.intern_access = intern_access

    def to_json(self) -> JSON:
        return super().to_json() | {
            "editor_access": self.editor_access.name,
            "guest_access": self.guest_access.name,
            "intern_access": self.intern_access.name
        }

    def copy(self, other: 'PrivacySettings') -> None:
        self.editor_access = other.editor_access
        self.guest_access = other.guest_access
        self.intern_access = other.intern_access

    @staticmethod
    def upload_cache():
        PrivacySettings._cached = FlaskApp().request(PrivacySettings).all()

    @staticmethod
    def clear_cache():
        PrivacySettings._cached = None

    @staticmethod
    def json_format() -> JSON:
        return {
            "editor_access": AccessType,
            "guest_access": AccessType,
            "intern_access": AccessType
        }

    @staticmethod
    def get_by_id(id: int):
        if PrivacySettings._cached is not None:
            result = list(filter(lambda x: x.id == id, PrivacySettings._cached))
            return None if len(result) == 0 else result[0]
        return FlaskApp().request(PrivacySettings).filter_by(id=id).first()

    @property
    def editor_access(self) -> AccessType:
        return self._editor_access

    @editor_access.setter
    @Editable.on_edit
    def editor_access(self, new_access: AccessType) -> str:
        self._editor_access = new_access
        return self._editor_access.name

    @property
    def intern_access(self) -> AccessType:
        return self._intern_access

    @intern_access.setter
    @Editable.on_edit
    def intern_access(self, new_access: AccessType) -> str:
        self._intern_access = new_access
        return self._intern_access.name

    @property
    def guest_access(self) -> AccessType:
        return self._guest_access

    @guest_access.setter
    @Editable.on_edit
    def guest_access(self, new_access: AccessType) -> str:
        self._guest_access = new_access
        return self._guest_access.name
