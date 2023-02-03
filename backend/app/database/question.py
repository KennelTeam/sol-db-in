#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_QUESTION_TEXT_SIZE, MAX_LANGUAGES_COUNT, MAX_COMMENT_SIZE, \
    SOURCE_QUESTION_ID, ANSWER_ROW_QUESTION_ID
from backend.app.flask_app import FlaskApp
from .editable import Editable
from typing import Dict, Any, List, Tuple
import json
from .formatting_settings import FormattingSettings
from .privacy_settings import PrivacySettings
from .relation_settings import RelationSettings
from .answer import Answer
from .question_type import QuestionType


class Question(Editable, FlaskApp().db.Model):
    __tablename__ = 'questions'
    _text = FlaskApp().db.Column('text', FlaskApp().db.Text(MAX_QUESTION_TEXT_SIZE * MAX_LANGUAGES_COUNT))
    _question_type = FlaskApp().db.Column('question_type', FlaskApp().db.Enum(QuestionType))
    _comment = FlaskApp().db.Column('comment', FlaskApp().db.Text(MAX_COMMENT_SIZE * MAX_LANGUAGES_COUNT))
    _answer_block_id = FlaskApp().db.Column('answer_block_id', FlaskApp().db.ForeignKey('answer_blocks.id'), nullable=True)
    _tag_type_id = FlaskApp().db.Column('tag_type_id', FlaskApp().db.ForeignKey('tag_types.id'), nullable=True)
    _formatting_settings = FlaskApp().db.Column('formatting_settings', FlaskApp().db.ForeignKey('formatting_settings.id'))
    _privacy_settings = FlaskApp().db.Column('privacy_settings', FlaskApp().db.ForeignKey('privacy_settings.id'))
    _relation_settings = FlaskApp().db.Column('relation_settings', FlaskApp().db.ForeignKey('relation_settings.id'), nullable=True)

    def __init__(self, texts: Dict[str, str], question_type: QuestionType, comment: Dict[str, str], answer_block_id: int,
                 tag_type_id: int):

        super(Editable).__init__()
        self.text = texts
        self._question_type = question_type
        self.comment = comment
        self.answer_block_id = answer_block_id
        self.tag_type_id = tag_type_id

    def prepare_my_table(self, inverse_relation=False):
        if self.question_type is not QuestionType.RELATION:
            raise Exception("Could not prepare a table for non-relational question")
        if not inverse_relation and not self.relation_settings.export_forward_relation:
            return []
        if inverse_relation and not self.relation_settings.export_inverse_relation:
            return []
        if self.formatting_settings.table_id is None:
            return [{str(self.id): item.to_json()} for item in Answer.filter(question_id=self.id)]

        formattings = FormattingSettings.get_from_question_table(self.formatting_settings.table_id)
        format_ids = [formatting.id for formatting in formattings]
        my_table = FlaskApp().request(Question).filter(Question._formatting_settings.in_(format_ids)).all()
        result = Question._order_answers(my_table)

        return {
            'questions': [item.to_json() for item in my_table],
            'answers': result
        }

    @staticmethod
    def _order_answers(my_table: List['Question']) -> Dict[Tuple[int, int], Dict[str, Dict[str, Any]]]:
        result = {}
        for question in my_table:
            answers = Answer.filter(question_id=question.id)
            for answer in answers:
                key = (answer.table_row, answer.form_id)
                if key not in result.keys():
                    result[key] = {}
                result[key][str(answer.question_id)] = answer.to_json()

        for key in result.keys():
            result[key][SOURCE_QUESTION_ID] = key[1]
            result[key][ANSWER_ROW_QUESTION_ID] = key[0]
        return result

    @staticmethod
    def get_by_id(id: int) -> 'Question':
        result = Question.get_by_ids([id])
        return None if len(result) == 0 else result[0]

    @staticmethod
    def get_by_ids(ids: List[int]) -> List['Question']:
        return FlaskApp().request(Question).filter(Question.id.in_(ids)).all()

    @staticmethod
    def get_all_with_formattings(formattings: List['FormattingSettings']) -> List['Question']:
        return FlaskApp().request(Question).filter(Question._formatting_settings.in_(
            [item.id for item in formattings]
        )).all()

    @staticmethod
    def get_by_text(text: str) -> List['Question']:
        return FlaskApp().request(Question).filter(Question.text.like(f"%{text}%")).all()

    def to_json(self, with_answers=False, form_id: int = None) -> Dict[str, Any]:
        result = super(Editable).to_json() | {
            'text': self.text,
            'question_type': self.question_type,
            'comment': self.comment,
            'answer_block_id': self.answer_block_id,
            'formatting_settings': self.formatting_settings,
            'privacy_settings': self.privacy_settings,
            'relation_settings': self.relation_settings
        }
        if with_answers:
            answers = Answer.filter(self.id, form_id=form_id)
            jsons = [answer.to_json() for answer in answers]
            result.update({
                'answers': sorted(jsons, key=lambda x: x['table_row'])
            })
        return result

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
        if self.question_type != QuestionType.RELATION:
            return None
        return RelationSettings.get_by_id(self._relation_settings)

    @relation_settings.setter
    @Editable.on_edit
    def relation_settings(self, new_relation_settings: RelationSettings) -> int:
        if self.question_type != QuestionType.RELATION:
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
    def question_type(self) -> QuestionType:
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

