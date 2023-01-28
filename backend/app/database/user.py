#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.config_loader import ConfigLoader
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR
import random
import string
import hashlib
from enum import Enum


class Role(Enum):
    UNAUTHORIZED = 0
    GUEST = 1
    INTERN = 2
    EDITOR = 3
    ADMIN = 4


class User(EditableMixin, db.Model):
    __tablename__ = 'users'
    login = db.Column('login', VARCHAR(ConfigLoader.get_config("MAX_LOGIN_SIZE")), unique=True)
    name = db.Column('name', db.Text(ConfigLoader.get_config("MAX_FULLNAME_SIZE")))
    comment = db.Column('comment', db.Text(ConfigLoader.get_config("MAX_COMMENT_SIZE")))

    # expected to use SHA-512
    password_hash = db.Column('password_hash', db.Text(512 // 8))

    # the length of salt is just made up
    password_salt = db.Column('password_salt', db.Text(ConfigLoader.get_config("SALT_SIZE")))
    role = db.Column('role', db.Integer)

    @staticmethod
    def __generate_salt():
        alphabet: str = string.ascii_letters + string.digits
        size = ConfigLoader.get_config("SALT_SIZE")
        return "".join(random.choices(alphabet, k=size))

    @staticmethod
    def __generate_password_hash(password: str, salt: str):
        password += salt
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def __init__(self, login: str, name: str, comment: str, password: str, role: Role):
        self.login = login
        self.name = name
        self.comment = comment
        self.password_salt = User.__generate_salt()
        self.password_hash = User.__generate_password_hash(password, self.password_salt)
        self.role = role.value
