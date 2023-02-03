#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.constants import MAX_BLOCK_NAME_SIZE, MAX_LANGUAGES_COUNT
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .form_type import FormType
from typing import Dict, Any, List, Tuple, TypeVar
from .question_table import QuestionTable
from .fixed_table import FixedTable
from .question import Question
from .formatting_settings import FormattingSettings
import json

Table = TypeVar('Table', bound=FlaskApp().db.Model)


class QuestionBlock(Editable, FlaskApp().db.Model):
    __tablename__ = 'question_blocks'
    _form = FlaskApp().db.Column('form', FlaskApp().db.Enum(FormType))
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_BLOCK_NAME_SIZE * MAX_LANGUAGES_COUNT))
    _sorting = FlaskApp().db.Column('sorting', FlaskApp().db.Integer)

    def __init__(self, name: Dict[str, str], form: FormType, sorting: int = 0):
        super(Editable).__init__()
        self.name = name
        self._form = form
        self.sorting = sorting

    def to_json(self) -> Dict[str, Any]:
        return super(Editable).to_json() | {
            'name': self.name,
            'form': self.form,
            'sorting': self.sorting,
            'questions': self.get_questions()
        }

    @property
    def form(self) -> FormType:
        return self._form

    @property
    def name(self) -> Dict[str, str]:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: Dict[str, str]) -> str:
        self._name = json.dumps(new_name)
        return self._name

    @property
    def sorting(self) -> int:
        return self._sorting

    @sorting.setter
    @Editable.on_edit
    def sorting(self, new_value: int):
        self._sorting = new_value

    @staticmethod
    def get_form(form: FormType) -> List['QuestionBlock']:
        blocks = QuestionBlock.query.filter_by(_form=form).all()
        return sorted(blocks, key=lambda x: x.sorting)

    def get_questions(self, with_answers=False, form_id: int = None, short_form: bool = False) -> List[Any]:
        free_questions: List[Tuple[Dict[str, Any], int]] = [(
            {
                'type': 'question',
                'value': item[0].to_json()
            }, item[1]) for item in self._get_free_questions(short_form)]

        table_questions: List[Tuple[Dict[str, Any], int]] = [(
            {
                'type': 'table_question',
                'value': item.get_questions(with_answers, form_id)
            }, item.block_sorting) for item in self._get_table_questions()]

        fixed_table_questions: List[Tuple[Dict[str, Any], int]] = [(
            {
                'type': 'fixed_table_question',
                'value': item.get_questions(with_answers, form_id)
            }, item.block_sorting) for item in self._get_fixed_table_questions()]

        total: List[Tuple[Dict[str, Any], int]] = free_questions + table_questions + fixed_table_questions
        total.sort(key=lambda x: x[1])
        return [item[0] for item in total]

    def _get_free_questions(self, short_form: bool) -> List[Tuple[Question, int]]:
        free_questions_formattings = FormattingSettings.filter_only_free_questions(
            FormattingSettings.query_from_block(self.id), short_form=short_form
        )
        # fqf = free questions formattings values
        fqf_dict = {item.id: item for item in free_questions_formattings}
        free_questions = Question.get_all_with_formattings(free_questions_formattings)
        return [(question, fqf_dict[question.formatting_settings].block_sorting) for question in free_questions]

    def _get_table_questions(self) -> List[QuestionTable]:
        formattings = FormattingSettings.filter_only_table_questions(
            FormattingSettings.query_from_block(self.id)
        )
        table_ids = set(item.table_id for item in formattings)
        return QuestionTable.get_by_ids(table_ids)

    def _get_fixed_table_questions(self) -> List[FixedTable]:
        formattings = FormattingSettings.filter_only_fixed_table(
            FormattingSettings.query_from_block(self.id)
        )
        fixed_table_ids = set(item.fixed_table_id for item in formattings)
        return FixedTable.get_by_ids(fixed_table_ids)
