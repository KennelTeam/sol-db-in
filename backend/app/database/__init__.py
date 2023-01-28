#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask_sqlalchemy import SQLAlchemy
from .. import app_instance
from backend.constants import DB_ENGINE, MODE, DB_CHARSET
import os


mode_prefix = "DEVELOP_" if MODE == "dev" else "PRODUCTION_"

username = os.getenv(mode_prefix + "USER")
password = os.getenv(mode_prefix + "PASSWORD")
database = os.getenv(mode_prefix + "DATABASE_NAME")

url = f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'

app_instance.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_ENGINE}://{username}:{password}@{url}/{database}?charset={DB_CHARSET}'
db: SQLAlchemy = SQLAlchemy(app_instance)
