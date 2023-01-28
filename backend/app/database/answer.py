#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from backend.config_loader import ConfigLoader
from typing import Any


class Answer(EditableMixin, db.Model):
    __tablename__ = 'answers'
    table_row = db.Column('table_row', db.Integer)
    question_id = db.Column('question_id', db.ForeignKey('questions.id'))
    leader_id = db.Column('leader_id', db.ForeignKey('leaders.id'), nullable=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'), nullable=True)
    int_value = db.Column('int_value', db.Integer, nullable=True)
    text_value = db.Column('text_value', db.Text(ConfigLoader.get_config("MAX_ANSWER_SIZE")), nullable=True)
    timestamp_value = db.Column('timestamp_value', db.DateTime, nullable=True)

    def __init__(self, question_id: int, value: Any, respondent_id: int, table_row=-1):
        pass


