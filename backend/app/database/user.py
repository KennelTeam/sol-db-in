#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_LOGIN_SIZE, MAX_FULLNAME_SIZE, MAX_COMMENT_SIZE, SALT_SIZE
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR
import random
import string
import hashlib
from enum import Enum
from typing import Dict, Any


class Role(Enum):
    UNAUTHORIZED = 0
    GUEST = 1
    INTERN = 2
    EDITOR = 3
    ADMIN = 4


class User(EditableMixin, db.Model):
    __tablename__ = 'users'
    login = db.Column('login', VARCHAR(MAX_LOGIN_SIZE), unique=True)
    name = db.Column('name', db.Text(MAX_FULLNAME_SIZE))
    comment = db.Column('comment', db.Text(MAX_COMMENT_SIZE))

    # expected to use SHA-512
    password_hash = db.Column('password_hash', db.Text(512 // 8))

    password_salt = db.Column('password_salt', db.Text(SALT_SIZE))
    role = db.Column('role', db.Enum(Role))

    current_ip: str = ""

    @staticmethod
    def _generate_salt() -> str:
        alphabet: str = string.ascii_letters + string.digits
        return "".join(random.choices(alphabet, k=SALT_SIZE))

    @staticmethod
    def _generate_password_hash(password: str, salt: str) -> str:
        password += salt
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def __init__(self, login: str, name: str, comment: str, password: str, role: Role) -> None:
        self.login = login
        self.name = name
        self.comment = comment
        self.password_salt = User._generate_salt()
        self.password_hash = User._generate_password_hash(password, self.password_salt)
        self.role = role
        super(EditableMixin).__init__(self.__dict__)

    def check_password(self, password) -> bool:
        return self.password_hash == User._generate_password_hash(password, self.password_salt)

    def to_json(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def get_by_login(login: str) -> 'User':
        return User.query.filter_by(login=login).first()

    @staticmethod
    def auth(login: str, password: str) -> Role:
        user = User.get_by_login(login)
        if user is None:
            return Role.UNAUTHORIZED
        if not user.check_password(password):
            return Role.UNAUTHORIZED
        return Role(user.role)
