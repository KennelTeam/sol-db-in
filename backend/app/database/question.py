#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_QUESTION_TEXT_SIZE, MAX_LANGUAGES_COUNT, MAX_COMMENT_SIZE
from . import db
from .editable import Editable
from enum import Enum
from typing import Dict, Any, List
import json
from .formatting_settings import FormattingSettings
from .privacy_settings import PrivacySettings
from .relation_settings import RelationSettings


class Type(Enum):
    DATE = 1
    USER = 2
    LONG_TEXT = 3
    SHORT_TEXT = 4
    MULTIPLE_CHOICE = 5
    CHECKBOX = 6
    LOCATION = 7
    NUMBER = 8
    BOOLEAN = 9
    RELATION = 10


class Question(Editable, db.Model):
    __tablename__ = 'questions'
    _text = db.Column('text', db.Text(MAX_QUESTION_TEXT_SIZE * MAX_LANGUAGES_COUNT))
    _question_type = db.Column('question_type', db.Enum(Type))
    _comment = db.Column('comment', db.Text(MAX_COMMENT_SIZE * MAX_LANGUAGES_COUNT))
    _answer_block_id = db.Column('answer_block_id', db.ForeignKey('answer_blocks.id'), nullable=True)
    _tag_type_id = db.Column('tag_type_id', db.ForeignKey('tag_types.id'), nullable=True)
    _show_on_main_page = db.Column('show_on_main_page', db.Boolean)
    _formatting_settings = db.Column('formatting_settings', db.ForeignKey('formatting_settings.id'))
    _privacy_settings = db.Column('privacy_settings', db.ForeignKey('privacy_settings.id'))
    _relation_settings = db.Column('relation_settings', db.ForeignKey('relation_settings.id'), nullable=True)

    def __init__(self, texts: Dict[str, str], question_type: Type, comment: Dict[str, str], answer_block_id: int,
                 tag_type_id: int, show_on_main_page: bool):

        super(Editable).__init__()
        self.text = texts
        self._question_type = question_type
        self.comment = comment
        self.answer_block_id = answer_block_id
        self.tag_type_id = tag_type_id
        self.show_on_main_page = show_on_main_page

    @staticmethod
    def get_by_id(id: int) -> 'Question':
        result = Question.get_by_ids([id])
        return None if len(result) == 0 else result[0]

    @staticmethod
    def get_by_ids(ids: List[int]) -> List['Question']:
        return Question.query.filter(Question.id.in_(ids)).all()

    @staticmethod
    def get_all_with_formattings(formattings: List['FormattingSettings']) -> List['Question']:
        return Question.query.filter(Question._formatting_settings.in_(
            [item.id for item in formattings]
        )).all()

    @staticmethod
    def get_by_text(text: str) -> 'Question':
        return Question.query.filter(Question.text.like(f"%{text}%")).all()

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'text': self.text,
            'question_type': self.question_type,
            'comment': self.comment,
            'answer_block_id': self.answer_block_id,
            'show_on_main_page': self.show_on_main_page,
            'formatting_settings': self.formatting_settings,
            'privacy_settings': self.privacy_settings,
            'relation_settings': self.relation_settings
        }

    @property
    def formatting_settings(self) -> FormattingSettings:
        return FormattingSettings.get_by_id(self._formatting_settings)

    @formatting_settings.setter
    @Editable.on_edit
    def formatting_settings(self, new_formatting: FormattingSettings) -> int:
        self._formatting_settings = new_formatting.id
        return self._formatting_settings

    @property
    def privacy_settings(self) -> PrivacySettings:
        return PrivacySettings.get_by_id(self._privacy_settings)

    @privacy_settings.setter
    @Editable.on_edit
    def privacy_settings(self, new_privacy: PrivacySettings) -> int:
        self._privacy_settings = new_privacy.id
        return self._privacy_settings

    @property
    def relation_settings(self) -> RelationSettings:
        if self.question_type != Type.RELATION:
            return None
        return RelationSettings.get_by_id(self._relation_settings)

    @relation_settings.setter
    @Editable.on_edit
    def relation_settings(self, new_relation_settings: RelationSettings) -> int:
        if self.question_type != Type.RELATION:
            raise Exception("Trying to set a relation settings to non-relational question!")
        self._relation_settings = new_relation_settings.id
        return self._relation_settings

    @property
    def text(self) -> Dict[str, str]:
        return json.loads(self._text)

    @text.setter
    @Editable.on_edit
    def text(self, new_texts: Dict[str, str]) -> str:
        self._text = json.dumps(new_texts)
        return self._text

    @property
    def question_type(self) -> Type:
        return self._question_type

    @property
    def comment(self) -> Dict[str, str]:
        return json.loads(self._comment)

    @comment.setter
    @Editable.on_edit
    def comment(self, new_comments: Dict[str, str]) -> str:
        self._comment = json.dumps(new_comments)
        return self._comment

    @property
    def answer_block_id(self) -> int:
        return self._answer_block_id

    @answer_block_id.setter
    @Editable.on_edit
    def answer_block_id(self, new_id: int) -> None:
        self._answer_block_id = new_id

    @property
    def tag_type_id(self) -> int:
        return self._tag_type_id

    @tag_type_id.setter
    @Editable.on_edit
    def tag_type_id(self, new_id: int) -> None:
        self._tag_type_id = new_id

    @property
    def show_on_main_page(self) -> bool:
        return self._show_on_main_page

    @show_on_main_page.setter
    @Editable.on_edit
    def show_on_main_page(self, value: bool) -> None:
        self._show_on_main_page = value
