#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin


class FormattingSettings(EditableMixin, db.Model):
    __tablename__ = 'formatting_settings'

    block_sorting = db.Column('block_sorting', db.Integer)
    table_column = db.Column('table_column', db.Integer, nullable=True)
    table_row = db.Column('table_row', db.Integer, nullable=True)
    block_id = db.Column('block_id', db.ForeignKey('question_blocks.id'), nullable=True, default=None)
    table_id = db.Column('table_id', db.ForeignKey('question_tables.id'), nullable=True, default=None)
    fixed_table_id = db.Column('fixed_table_id', db.ForeignKey('fixed_tables.id'), nullable=True, default=None)
