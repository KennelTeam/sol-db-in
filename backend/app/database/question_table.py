#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin


class QuestionTable(EditableMixin, db.Model):
    __tablename__ = 'question_tables'
