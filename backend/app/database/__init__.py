#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask_sqlalchemy import SQLAlchemy
from .. import app
import config_loader
import os

engine = config_loader.get_config("DB_ENGINE")

mode_prefix = "DEVELOP_" if config_loader.get_config("MODE") == "dev" else "PRODUCTION_"

username = os.getenv(mode_prefix + "USER")
password = os.getenv(mode_prefix + "PASSWORD")
database = os.getenv(mode_prefix + "DATABASE_NAME")

url = f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'
charset = config_loader.get_config("DB_CHARSET")

app.config['SQLALCHEMY_DATABASE_URI'] = f'{engine}://{username}:{password}@{url}/{database}?charset={charset}'
db = SQLAlchemy(app)

from .answer import Answer
from .answer_block import AnswerBlock
from .answer_option import AnswerOption
from .fixed_table import FixedTable
from .formatting_settings import FormattingSettings
from .leader import Leader
from .project import Project
from .question import Question
from .question_block import QuestionBlock
from .question_table import QuestionTable
from .relation_settings import RelationSettings
from .tag import Tag
from .tag_type import TagType
from .toponym import Toponym
from .user import User
