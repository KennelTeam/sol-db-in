#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin
from .value_holder import ValueHolder


class Answer(EditableMixin, ValueHolder, db.Model):
    __tablename__ = 'answers'
    table_row = db.Column('table_row', db.Integer)
    question_id = db.Column('question_id', db.ForeignKey('questions.id'))
    leader_id = db.Column('leader_id', db.ForeignKey('leaders.id'), nullable=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'), nullable=True)
