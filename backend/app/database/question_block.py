#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from typing import List, Tuple, TypeVar
import json
from backend.constants import MAX_BLOCK_NAME_SIZE, MAX_LANGUAGES_COUNT
from backend.auxiliary import JSON, TranslatedText
from backend.app.flask_app import FlaskApp
from .localization import localize
from .editable import Editable
from .form_type import FormType
from .question_table import QuestionTable
from .fixed_table import FixedTable
from .question import Question
from .formatting_settings import FormattingSettings

Table = TypeVar('Table', bound=FlaskApp().db.Model)


class QuestionBlock(Editable, FlaskApp().db.Model):
    __tablename__ = 'question_blocks'
    _form = FlaskApp().db.Column('form', FlaskApp().db.Enum(FormType))
    _name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_BLOCK_NAME_SIZE * MAX_LANGUAGES_COUNT))
    _sorting = FlaskApp().db.Column('sorting', FlaskApp().db.Integer)

    _cached = None

    def __init__(self, name: TranslatedText, form: FormType, sorting: int = 0):
        super().__init__()
        self.name = name
        self._form = form
        self.sorting = sorting

    def to_json(self, with_answers: bool = False, form_id: int = None) -> JSON:
        return super().to_json() | {
            'name': localize(self.name),
            'form': self.form.name,
            'sorting': self.sorting,
            'questions': self.get_questions(with_answers, form_id)
        }

    @staticmethod
    def upload_cache():
        QuestionBlock._cached = FlaskApp().request(QuestionBlock).all()

    @staticmethod
    def clear_cache():
        QuestionBlock._cached = None

    @staticmethod
    def get_by_id(id: int) -> 'QuestionBlock':
        if QuestionBlock._cached is not None:
            res = list(filter(lambda x: x.id == id, QuestionBlock._cached))
            return None if len(res) == 0 else res[0]
        return FlaskApp().request(QuestionBlock).filter_by(id=id).first()

    @property
    def form(self) -> FormType:
        return self._form

    @property
    def name(self) -> TranslatedText:
        return json.loads(self._name)

    @name.setter
    @Editable.on_edit
    def name(self, new_name: TranslatedText) -> str:
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
        if QuestionBlock._cached is not None:
            blocks = list(filter(lambda x: x._form == form, QuestionBlock._cached))  # pylint: disable=protected-access
        else:
            blocks = FlaskApp().request(QuestionBlock).filter_by(_form=form).all()
        return sorted(blocks, key=lambda x: x.sorting)

    def get_questions(self, with_answers=False, form_id: int = None) -> List[JSON]:
        free_questions: List[Tuple[JSON, int]] = [(
            {
                'type': 'question',
                'value': item[0].to_json(with_answers, form_id)
            }, item[1]) for item in self._get_free_questions()]

        table_questions: List[Tuple[JSON, int]] = [(
            {
                'type': 'table_question',
                'value': item.get_questions(with_answers, form_id)
            }, item.block_sorting) for item in self._get_table_questions()]

        fixed_table_questions: List[Tuple[JSON, int]] = [(
            {
                'type': 'fixed_table_question',
                'value': item.get_questions(with_answers, form_id)
            }, item.block_sorting) for item in self._get_fixed_table_questions()]

        total: List[Tuple[JSON, int]] = free_questions + table_questions + fixed_table_questions
        total.sort(key=lambda x: x[1])
        return [item[0] for item in total]

    def _get_free_questions(self) -> List[Tuple[Question, int]]:
        free_questions_formattings = FormattingSettings.filter_only_free_questions(
            FormattingSettings.query_from_block(self.id)
        )
        fqf_dict = {item.id: item for item in free_questions_formattings}
        free_questions = Question.get_all_with_formattings(free_questions_formattings)
        return [(question, fqf_dict[question.formatting_settings.id].block_sorting) for question in free_questions]

    def _get_table_questions(self) -> List[QuestionTable]:
        formattings = FormattingSettings.filter_only_table_questions(
            FormattingSettings.query_from_block(self.id)
        )
        table_ids = set(item.table_id for item in formattings)
        return QuestionTable.get_by_ids(table_ids)

    def _get_fixed_table_questions(self) -> List[FixedTable]:
        formattings = FormattingSettings.filter_only_fixed_table_questions(
            FormattingSettings.query_from_block(self.id)
        )
        fixed_table_ids = set(item.fixed_table_id for item in formattings)
        return FixedTable.get_by_ids(fixed_table_ids)
