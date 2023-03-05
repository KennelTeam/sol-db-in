#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from backend.constants import MAX_LOGIN_SIZE, MAX_FULLNAME_SIZE, MAX_COMMENT_SIZE
from backend.auxiliary import JSON
from backend.app.flask_app import FlaskApp
from .editable import Editable

from sqlalchemy.dialects.mysql import VARCHAR
from enum import Enum
from typing import List
import bcrypt


class Role(Enum):
    GUEST = 1
    INTERN = 2
    EDITOR = 3
    ADMIN = 4


class User(Editable, FlaskApp().db.Model):
    __tablename__ = 'users'
    _login = FlaskApp().db.Column('login', VARCHAR(MAX_LOGIN_SIZE), unique=True)
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_FULLNAME_SIZE))
    _comment = FlaskApp().db.Column('comment', FlaskApp().db.Text(MAX_COMMENT_SIZE))
    _password_hash = FlaskApp().db.Column('password', FlaskApp().db.Text(512 // 8))
    _role = FlaskApp().db.Column('role', FlaskApp().db.Enum(Role))

    current_ip: str = ''

    def __init__(self, login: str, name: str, comment: str, password: str, role: str) -> None:
        super().__init__()
        self.login = login
        self.name = name
        self.comment = comment
        self.password = password
        self.role = Role[role]

    def to_json(self) -> JSON:
        return super().to_json() | {
            'login': self.login,
            'name': self.name,
            'comment': self.comment,
            'role': self.role.name
        }

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    @Editable.on_edit
    def login(self, new_login: str) -> None:
        self._login = new_login

    # We do not actually store password, so accessing it returns nothing
    # IDEA: maybe it's better to raise an exception here
    @property
    def password(self) -> str:
        return ""

    # so in the actions database instead of storing passwords we store password_hashes in the password column
    # so for user it shows that the password was changed (when the hash was changed),
    # but it ensures security
    @password.setter
    @Editable.on_edit
    def password(self, new_password: str) -> str:
        self._password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode('utf-8')
        return self.password_hash

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @Editable.on_edit
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    @Editable.on_edit
    def comment(self, new_comment: str) -> None:
        self._comment = new_comment

    @property
    def role(self) -> Role:
        return Role(self._role)

    @role.setter
    @Editable.on_edit
    def role(self, new_role: Role) -> str:
        self._role = new_role
        return self._role.name

    def save_to_db(self) -> None:
        FlaskApp().add_database_item(self)
        FlaskApp().flush_to_database()

    def update(self, login: str = None, name: str = None, comment: str = None,
               password: str = None, role: Role = None) -> None:
        if login is not None:
            self.login = login
        if name is not None:
            self.name = name
        if comment is not None:
            self.comment = comment
        if password is not None:
            self.password = password
        if role is not None:
            self.role = role
        FlaskApp().flush_to_database()

    @staticmethod
    def get_by_login(login: str) -> 'User':
        return FlaskApp().request(User).filter_by(_login=login).first()

    @staticmethod
    def get_by_id(id: int) -> 'User':
        return FlaskApp().request(User).filter_by(id=id).first()

    @staticmethod
    def get_all_users() -> List['User']:
        return FlaskApp().request(User).all()

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def auth(self, login: str, password: str) -> 'User' | None:
        user = User.get_by_login(login)
        if not user or not self.check_password(password):
            return None
        return user
