#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from config_loader import get_config
from . import db
from .editable_mixin import EditableMixin


types = {
    'Date': 1,
    'User': 2,
    'Long text': 3,
    'Short text': 4,
    'Multiple-choice': 5,
    'Checkbox': 6,
    'Location': 7,
    'Number': 8,
    'Relation': 9
}


class Question(EditableMixin, db.Model):
    __tablename__ = 'questions'
    text = db.Column('text', db.Text(get_config("MAX_QUESTION_TEXT_SIZE") * get_config("MAX_LANGUAGES_COUNT")))
    question_type = db.Column('question_type', db.Integer)
    comment = db.Column('comment', db.Text(get_config("MAX_COMMENT_SIZE") * get_config("MAX_LANGUAGES_COUNT")))
    answer_block_id = db.Column('answer_block_id', db.ForeignKey('answer_blocks.id'), nullable=True)
    tag_type_id = db.Column('tag_type_id', db.ForeignKey('tag_types.id'), nullable=True)
    show_on_main_page = db.Column('show_on_main_page', db.Boolean)
    formatting_settings = db.Column('formatting_settings', db.ForeignKey('formatting_settings.id'))
    relation_settings = db.Column('relation_settings', db.ForeignKey('relation_settings.id'), nullable=True)
