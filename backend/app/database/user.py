#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.config_loader import ConfigLoader
from . import db
from .editable_mixin import EditableMixin
from sqlalchemy.dialects.mysql import VARCHAR


roles = {
    'unauthorized': 0,
    'guest': 1,
    'intern': 2,
    'editor': 3,
    'admin': 4
}


class User(EditableMixin, db.Model):
    __tablename__ = 'users'
    login = db.Column('login', db.Text(ConfigLoader.get_config("MAX_LOGIN_SIZE")))
    login_hash = db.Column('login_hash', VARCHAR(512//8), unique=True)
    name = db.Column('name', db.Text(ConfigLoader.get_config("MAX_FULLNAME_SIZE")))
    comment = db.Column('comment', db.Text(ConfigLoader.get_config("MAX_COMMENT_SIZE")))

    # expected to use SHA-512
    password_hash = db.Column('password_hash', db.Text(512 // 8))

    # the length of salt is just made up
    password_salt = db.Column('password_salt', db.Text(32))
    role = db.Column('role', db.Integer)

    # it is supposed that jwt refresh token is smaller than 512 bytes
    jwt_refresh = db.Column('jwt_refresh', db.Text(512))
