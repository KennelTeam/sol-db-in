#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import sqlalchemy.orm

from backend.constants import MAX_BLOCK_NAME_SIZE, MAX_LANGUAGES_COUNT
from . import db
from .editable import Editable
from .form_type import FormType
from typing import Dict, Any, List, Tuple, TypeVar
from .question_table import QuestionTable, QuestionTable_T
from .fixed_table import FixedTable, FixedTable_T
from .question import Question
from .formatting_settings import FormattingSettings
from .form import Form
import json

Table = TypeVar('Table', bound=db.Model)


class QuestionBlock(Editable, db.Model):
    __tablename__ = 'question_blocks'
    _form = db.Column('form', db.Enum(FormType))
    _name = db.Column('name', db.Text(MAX_BLOCK_NAME_SIZE * MAX_LANGUAGES_COUNT))
    _sorting = db.Column('sorting', db.Integer)

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
    def get_form(form: Form) -> List[Dict[str, Any]]:
        blocks = QuestionBlock.query.filter_by(_form=form).all()
        return sorted(blocks, key=lambda x: x.sorting)

    def get_questions(self) -> List[Any]:
        free_questions: List[Tuple[Dict[str, Any], int]] = [({'type': 'question', 'value': item[0]},
                                                             item[1]) for item in self._get_free_questions()]

        table_questions: List[Tuple[Dict[str, Any], int]] = [({'type': 'table_question', 'value': item[0]},
                                                              item[1]) for item in self._get_table_questions()]

        fixed_table_questions: List[Tuple[Dict[str, Any], int]] = [({'type': 'fixed_table_question', 'value': item[0]},
                                                                item[1]) for item in self._get_fixed_table_questions()]

        total: List[Tuple[Dict[str, Any], int]] = free_questions + table_questions + fixed_table_questions
        total.sort(key=lambda x: x[1])
        return [item[0] for item in total]

    def _get_free_questions(self) -> List[Tuple[Question, int]]:
        free_questions_formattings = FormattingSettings.filter_only_free_questions(
            FormattingSettings.query_from_block(self.id)
        )
        # fqf = free questions formattings values
        fqf_dict = {item.id: item for item in free_questions_formattings}
        free_questions = Question.get_all_with_formattings(free_questions_formattings)
        return [(question, fqf_dict[question.formatting_settings].block_sorting) for question in free_questions]

    def _get_table_questions(self) -> List[Tuple[QuestionTable_T, int]]:
        formattings = FormattingSettings.filter_only_table_questions(
            FormattingSettings.query_from_block(self.id)
        )
        table_ids = set(item.table_id for item in formattings)
        tables = QuestionTable.get_by_ids(table_ids)
        return [(item.get_questions(), item.block_sorting) for item in tables]

    def _get_fixed_table_questions(self) -> List[Tuple[FixedTable_T, int]]:
        formattings = FormattingSettings.filter_only_fixed_table(
            FormattingSettings.query_from_block(self.id)
        )
        fixed_table_ids = set(item.fixed_table_id for item in formattings)
        tables = FixedTable.get_by_ids(fixed_table_ids)
        return [(item.get_questions(), item.block_sorting) for item in tables]
