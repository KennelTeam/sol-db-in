#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from .api.login import Login
from .api.logout import Logout
from .api.register import Register
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

from .flask_app import FlaskApp


FlaskApp().api.add_resource(Login, '/login')
FlaskApp().api.add_resource(Register, '/register')
FlaskApp().api.add_resource(Logout, '/logout')
FlaskApp().api.add_resource(Forms, '/forms')
FlaskApp().api.add_resource(FormPage, '/form_page')
FlaskApp().api.add_resource(ToponymTree, '/toponym_tree')
FlaskApp().api.add_resource(Toponyms, '/toponyms')
FlaskApp().api.add_resource(AnswerOptionsPage, '/answer_options')
FlaskApp().api.add_resource(AllAnswerBlocks, '/all_answer_blocks')
FlaskApp().api.add_resource(AnswerBlockPage, '/answer_block')
FlaskApp().api.add_resource(QuestionBlockPage, '/question_block')
FlaskApp().api.add_resource(Table, '/table')
FlaskApp().api.add_resource(Tags, '/tags')
FlaskApp().api.add_resource(TagTypes, '/tag_type')
FlaskApp().api.add_resource(FormSchema, '/form')
