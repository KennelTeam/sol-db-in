#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from .api.actions import Actions
from .api.language import Language
from .api.login import Login
from .api.logout import Logout
from .api.settings import Settings
from .api.statistics import Statistics
from .api.users import Users
from .api.forms import Forms
from .api.form_page import FormPage
from .api.toponym_tree import ToponymTree
from .api.toponyms import Toponyms
from .api.answer_options import AnswerOptionsPage
from .api.all_answer_blocks import AllAnswerBlocks
from .api.answer_block import AnswerBlockPage
from .api.question_block import QuestionBlockPage
from .api.table import Table
from .api.tags import Tags
from .api.tag_types import TagTypes
from .api.form import FormSchema
from .api.all_toponyms import AllToponyms
from .api.questions import Questions

from .flask_app import FlaskApp

resources = [
    Login, Logout, Users, Forms, FormPage, Toponyms, ToponymTree, AnswerOptionsPage, AllAnswerBlocks, Language,
    AnswerBlockPage, QuestionBlockPage, Table, Tags, TagTypes, FormSchema, Questions, Actions, Statistics, Settings,
    AllToponyms
]

for resource in resources:
    FlaskApp().api.add_resource(resource, resource.route)
