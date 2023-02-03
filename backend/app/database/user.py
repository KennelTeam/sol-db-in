#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_LOGIN_SIZE, MAX_FULLNAME_SIZE, MAX_COMMENT_SIZE, SALT_SIZE
from backend.app.flask_app import FlaskApp
from .editable import Editable
from sqlalchemy.dialects.mysql import VARCHAR
import random
import string
import hashlib
from enum import Enum
from typing import Dict, Any, List


class Role(Enum):
    UNAUTHORIZED = 0
    GUEST = 1
    INTERN = 2
    EDITOR = 3
    ADMIN = 4


class User(Editable, FlaskApp().db.Model):
    __tablename__ = 'users'
    _login = FlaskApp().db.Column('login', VARCHAR(MAX_LOGIN_SIZE), unique=True)
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_FULLNAME_SIZE))
    _comment = FlaskApp().db.Column('comment', FlaskApp().db.Text(MAX_COMMENT_SIZE))

    # expected to use SHA-512
    _password_hash = FlaskApp().db.Column('password', FlaskApp().db.Text(512 // 8))

    _password_salt = FlaskApp().db.Column('password_salt', FlaskApp().db.Text(SALT_SIZE))
    _role = FlaskApp().db.Column('role', FlaskApp().db.Enum(Role))

    current_ip: str = ""

    @staticmethod
    def _generate_salt() -> str:
        alphabet: str = string.ascii_letters + string.digits
        return "".join(random.choices(alphabet, k=SALT_SIZE))

    def _generate_password_hash(self, password: str) -> str:
        password += self._password_salt
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def __init__(self, login: str, name: str, comment: str, password: str, role: Role) -> None:
        super(Editable).__init__()
        self.login = login
        self.name = name
        self.comment = comment
        self._password_salt = User._generate_salt()
        self.password = password
        self.role = role

    def check_password(self, password) -> bool:
        return self._password_hash == self._generate_password_hash(password)

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'login': self.login,
            'name': self.name,
            'comment': self.comment,
            'role': self.role
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
        self._password_hash = self._generate_password_hash(new_password)
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
        self.name = new_name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    @Editable.on_edit
    def comment(self, new_comment: str) -> None:
        self._comment = new_comment

    @property
    def role(self) -> Role:
        return self._role

    @role.setter
    @Editable.on_edit
    def role(self, new_role: Role) -> None:
        self._role = new_role

    @staticmethod
    def get_by_login(login: str) -> 'User':
        return FlaskApp().request(User).filter_by(login=login).first()

    @staticmethod
    def get_all_users() -> List['User']:
        return FlaskApp().request(User).all()

    @staticmethod
    def auth(login: str, password: str) -> Role:
        user = User.get_by_login(login)
        if user is None:
            return Role.UNAUTHORIZED
        if not user.check_password(password):
            return Role.UNAUTHORIZED
        return Role(user.role)
