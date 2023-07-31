#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import os

from flask import send_from_directory

from backend.auxiliary.misc import get_sol_db_logger

from .api.actions import Actions
from .api.database_excel_export import DatabaseExcelExport
from .api.all_questions import AllQuestions
from .api.forms_lightweight import FormsLightweight
from .api.fullness_statistics import FullnessStatistics
from .api.language import Language
from .api.login import Login
from .api.logout import Logout
from .api.raw_db_excel_export import RawDbExcelExport
from .api.settings import Settings
from .api.statistics import Statistics
from .api.tags_statistics import TagsStatistics
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
from .api.questions_lightweight import QuestionsLightweight
from .api.all_tags import AllTags

from .flask_app import FlaskApp

resources = [
    Login, Logout, Users, Forms, FormPage, Toponyms, ToponymTree, AnswerOptionsPage, AllAnswerBlocks, Language,
    AnswerBlockPage, QuestionBlockPage, Table, Tags, TagTypes, FormSchema, Questions, Actions, Statistics, Settings,
    FormsLightweight, AllToponyms, FullnessStatistics, DatabaseExcelExport, AllQuestions, QuestionsLightweight, AllTags,
    TagsStatistics, RawDbExcelExport
]

for resource in resources:
    FlaskApp().api.add_resource(resource, "/api" + resource.route)


logger = get_sol_db_logger('flask-server')


@FlaskApp().app.route('/', defaults={'path': ''})
@FlaskApp().app.route('/<path:path>')
def serve(path):
    logger.debug('Sending a static file at path %s. Static folder is %s', path, FlaskApp().app.static_folder)
    if path != "" and os.path.exists(FlaskApp().app.static_folder + '/' + path):
        return send_from_directory(FlaskApp().app.static_folder, path)
    return send_from_directory(FlaskApp().app.static_folder, 'index.html')
