#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask_sqlalchemy import SQLAlchemy
from .. import app
from backend.config_loader import ConfigLoader
import os

engine = ConfigLoader.get_config("DB_ENGINE")

mode_prefix = "DEVELOP_" if ConfigLoader.get_config("MODE") == "dev" else "PRODUCTION_"

username = os.getenv(mode_prefix + "USER")
password = os.getenv(mode_prefix + "PASSWORD")
database = os.getenv(mode_prefix + "DATABASE_NAME")

url = f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'
charset = ConfigLoader.get_config("DB_CHARSET")

app.config['SQLALCHEMY_DATABASE_URI'] = f'{engine}://{username}:{password}@{url}/{database}?charset={charset}'
db: SQLAlchemy = SQLAlchemy(app)
