#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from enum import Enum

from sqlalchemy.orm import Query
from typing import List
import json
from backend.constants import MAX_QUESTION_TEXT_SIZE, MAX_LANGUAGES_COUNT, MAX_COMMENT_SIZE, \
    SOURCE_QUESTION_ID, ANSWER_ROW_QUESTION_ID, MAX_SHORT_QUESTION_SIZE
from backend.auxiliary import JSON, TranslatedText, LogicException
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .form_type import FormType
from .formatting_settings import FormattingSettings
from .privacy_settings import PrivacySettings
from .relation_settings import RelationSettings
from .answer import Answer
from .question_type import QuestionType


class AnswerType(Enum):
    VALUE = 1
    FORWARD_COUNT = 2
    INVERSE_COUNT = 3
    REFERENCE = 4


class Question(Editable, FlaskApp().db.Model):
    __tablename__ = 'questions'
    _text = FlaskApp().db.Column('text', FlaskApp().db.Text(MAX_QUESTION_TEXT_SIZE * MAX_LANGUAGES_COUNT))
    _short_text = FlaskApp().db.Column('short_text', FlaskApp().db.Text(MAX_SHORT_QUESTION_SIZE * MAX_LANGUAGES_COUNT))
    _question_type = FlaskApp().db.Column('question_type', FlaskApp().db.Enum(QuestionType))
    _comment = FlaskApp().db.Column('comment', FlaskApp().db.Text(MAX_COMMENT_SIZE * MAX_LANGUAGES_COUNT))
    _answer_block_id = FlaskApp().db.Column('answer_block_id',
                                            FlaskApp().db.ForeignKey('answer_blocks.id'), nullable=True)

    _tag_type_id = FlaskApp().db.Column('tag_type_id', FlaskApp().db.ForeignKey('tag_types.id'), nullable=True)
    _formatting_settings = FlaskApp().db.Column('formatting_settings',
                                                FlaskApp().db.ForeignKey('formatting_settings.id'))

    _privacy_settings = FlaskApp().db.Column('privacy_settings', FlaskApp().db.ForeignKey('privacy_settings.id'))
    _relation_settings = FlaskApp().db.Column('relation_settings',
                                              FlaskApp().db.ForeignKey('relation_settings.id'), nullable=True)

    _related_question_id = FlaskApp().db.Column('related_question_id', FlaskApp().db.Integer, nullable=True)

    _form_type = FlaskApp().db.Column('form_type', FlaskApp().db.Enum(FormType))

    def __init__(self, texts: TranslatedText, short_texts: TranslatedText, question_type: QuestionType,
                 comment: TranslatedText, answer_block_id: int, tag_type_id: int, form_type: str,
                 related_question_id: int = None):

        super().__init__()
        self.text = texts
        self.short_text = short_texts
        self._question_type = question_type
        self.comment = comment
        self.answer_block_id = answer_block_id
        self.tag_type_id = tag_type_id
        self.related_question_id = related_question_id
        self.form_type = FormType[form_type]

    def prepare_my_table(self, inverse_relation=False) -> JSON:
        if self.question_type is not QuestionType.RELATION:
            raise LogicException("Could not prepare a table for non-relational question")
        if not inverse_relation and not self.relation_settings.export_forward_relation:
            return None
        if inverse_relation and not self.relation_settings.export_inverse_relation:
            return None
        if self.formatting_settings.table_id is None:
            return {
                "questions": [self.to_json()],
                "answers": [{str(self.id): item.to_json()} for item in Answer.filter(question_id=self.id)]
            }

        formattings = FormattingSettings.get_from_question_table(self.formatting_settings.table_id)
        format_ids = [formatting.id for formatting in formattings]
        my_table = FlaskApp().request(Question).filter(Question._formatting_settings.in_(format_ids)).all()
        result = Question._order_answers(my_table)

        return {
            'questions': [item.to_json() for item in my_table],
            'answers': result
        }

    @staticmethod
    def filter_by_answer_block(answer_block_id: int) -> Query:
        return FlaskApp().request(Question).filter_by(_answer_block_id=answer_block_id)

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
    def get_all_with_relation_settings(relation_settings: List[int]) -> List['Question']:
        return FlaskApp().request(Question).filter(Question._relation_settings.in_(
            relation_settings
        )).all()

    @staticmethod
    def get_by_text(text: str) -> List['Question']:
        return FlaskApp().request(Question).filter(Question.text.like(f"%{text}%")).all()

    @staticmethod
    def get_only_main_page(form_type: FormType) -> List[JSON]:
        formattings = FormattingSettings.get_main_page()
        questions = Question.get_all_with_formattings(formattings)
        counted_relations = RelationSettings.get_main_page_count_presented()
        counted_questions_forward = Question.get_all_with_relation_settings(counted_relations[0])
        counted_questions_inverse = Question.get_all_with_relation_settings(counted_relations[1])

        def form_type_filter(q: Question) -> bool:
            return q.form_type == form_type

        questions = filter(form_type_filter, questions)
        counted_questions_inverse = filter(form_type_filter, counted_questions_inverse)
        counted_questions_forward = filter(form_type_filter, counted_questions_forward)

        result = [{
            'type': AnswerType.VALUE,
            'question': item
        } for item in questions] + [{
            'type': AnswerType.FORWARD_COUNT,
            'question': item
        } for item in counted_questions_forward] + [{
            'type': AnswerType.INVERSE_COUNT,
            'question': item
        } for item in counted_questions_inverse]

        return result

    def to_json(self, with_answers=False, form_id: int = None) -> JSON:
        result = super().to_json() | {
            'text': self.text,
            'short_text': self.short_text,
            'question_type': self.question_type.name,
            'comment': self.comment,
            'answer_block_id': self.answer_block_id,
            'formatting_settings': self.formatting_settings.to_json(),
            'privacy_settings': self.privacy_settings.to_json(),
            'relation_settings': self.relation_settings.to_json(),
            'related_question_id': self.related_question_id,
            'form_type': self.form_type
        }
        if with_answers:
            answers = Answer.filter(self.id, form_id=form_id)
            related_answers = Answer.filter(self.related_question_id, form_id=form_id)
            jsons = [answer.to_json() for answer in answers + related_answers]
            result.update({
                'answers': sorted(jsons, key=lambda x: x['table_row'])
            })
        return result

    @staticmethod
    def _order_answers(my_table: List['Question']) -> List[JSON]:
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
        return list(result.values())

    @property
    def form_type(self) -> FormType:
        return self._form_type

    @form_type.setter
    @Editable.on_edit
    def form_type(self, form_type: FormType) -> None:
        self._form_type = form_type

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
            raise LogicException("Trying to set a relation settings to non-relational question!")
        self._relation_settings = new_relation_settings.id
        return self._relation_settings

    @property
    def related_question_id(self) -> int:
        return self._related_question_id

    @related_question_id.setter
    @Editable.on_edit
    def related_question_id(self, new_id: int):
        self._related_question_id = new_id

    @property
    def short_text(self) -> TranslatedText:
        return json.loads(self._short_text)

    @short_text.setter
    @Editable.on_edit
    def short_text(self, new_texts: TranslatedText) -> str:
        self._short_text = json.dumps(new_texts)
        return self._short_text

    @property
    def text(self) -> TranslatedText:
        return json.loads(self._text)

    @text.setter
    @Editable.on_edit
    def text(self, new_texts: TranslatedText) -> str:
        self._text = json.dumps(new_texts)
        return self._text

    @property
    def question_type(self) -> QuestionType:
        return self._question_type

    @property
    def comment(self) -> TranslatedText:
        return json.loads(self._comment)

    @comment.setter
    @Editable.on_edit
    def comment(self, new_comments: TranslatedText) -> str:
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
