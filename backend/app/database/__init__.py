#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask_sqlalchemy import SQLAlchemy
from .. import app
from backend import config_loader
import os


engine = config_loader.get_config("DB_ENGINE")

mode_prefix = "DEVELOP_" if config_loader.get_config("MODE") == "dev" else "PRODUCTION_"

username = os.getenv(mode_prefix + "USER")
password = os.getenv(mode_prefix + "PASSWORD")
database = os.getenv(mode_prefix + "DATABASE")

url = f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'
charset = config_loader.get_config("DB_CHARSET")

app.config['SQLALCHEMY_DATABASE_URI'] = f'{engine}://{username}:{password}@{url}?charset={charset}'
db = SQLAlchemy(app)
