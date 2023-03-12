#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import json
from typing import List, Tuple

from backend.app.flask_app import FlaskApp
from backend.auxiliary import JSON, TranslatedText
from backend.constants import MAX_SHORT_QUESTION_SIZE, MAX_LANGUAGES_COUNT
from .editable import Editable
from .visualization_type import VisualizationType
from .form_type import FormType


class RelationSettings(Editable, FlaskApp().db.Model):
    __tablename__ = 'relation_settings'

    _relation_type = FlaskApp().db.Column('relation_type', FlaskApp().db.Enum(FormType))

    _related_visualization_type = FlaskApp().db.Column('related_visualization_type',
                                                       FlaskApp().db.Enum(VisualizationType), nullable=True)
    _related_visualization_sorting = FlaskApp().db.Column('related_visualization_sorting',
                                                          FlaskApp().db.Integer, nullable=True)

    _forward_relation_sheet_name = FlaskApp().db.Column('forward_relation_sheet_name',
                                                        FlaskApp().db.Boolean, nullable=True)
    _inverse_relation_sheet_name = FlaskApp().db.Column('inverse_relation_sheet_name',
                                                        FlaskApp().db.Boolean, nullable=True)
    _main_page_count_title = FlaskApp().db.Column('main_page_count_title',
                                                  FlaskApp().db.Text(MAX_SHORT_QUESTION_SIZE * MAX_LANGUAGES_COUNT),
                                                  nullable=True)
    _inverse_main_page_count_title = FlaskApp().db.Column(
        'inverse_main_page_count_title',
        FlaskApp().db.Text(MAX_SHORT_QUESTION_SIZE * MAX_LANGUAGES_COUNT),
        nullable=True)

    def __init__(self, relation_type: FormType,
                 related_visualization_type: VisualizationType, related_visualization_sorting: int = 0,
                 main_page_count_title: TranslatedText = None, inverse_main_page_count_title: TranslatedText = None,
                 forward_relation_sheet_name: str = None, inverse_relation_sheet_name: str = None) -> None:

        super().__init__()
        self._relation_type = relation_type
        self.related_visualization_type = related_visualization_type
        self.related_visualization_sorting = related_visualization_sorting

        self.main_page_count_title = main_page_count_title
        self.inverse_main_page_count_title = inverse_main_page_count_title
        self.forward_relation_sheet_name = forward_relation_sheet_name
        self.inverse_relation_sheet_name = inverse_relation_sheet_name

    def to_json(self) -> JSON:
        return super().to_json() | {
            'relation_type': self.relation_type,
            'related_visualization_type': self.related_visualization_type,
            'related_visualization_sorting': self.related_visualization_sorting,
            'forward_relation_sheet_name': self.forward_relation_sheet_name,
            'inverse_relation_sheet_name': self.inverse_relation_sheet_name,
            'main_page_count_title': self.main_page_count_title,
            'inverse_main_page_count_title': self.inverse_main_page_count_title
        }

    def copy(self, other: 'RelationSettings') -> None:
        self.related_visualization_type = other.related_visualization_type
        self.related_visualization_sorting = other.related_visualization_sorting
        self.main_page_count_title = other.main_page_count_title
        self.inverse_main_page_count_title = other.inverse_main_page_count_title
        self.forward_relation_sheet_name = other.forward_relation_sheet_name
        self.inverse_relation_sheet_name = other.inverse_relation_sheet_name

    @staticmethod
    def json_format() -> JSON:
        return {
            'relation_type': FormType,
            'related_visualization_type': VisualizationType,
            'related_visualization_sorting': VisualizationType,
            'forward_relation_sheet_name': {str, None},
            'inverse_relation_sheet_name': {str, None},
            'main_page_count_title': {dict, None},
            'inverse_main_page_count_title': {dict, None}
        }

    @staticmethod
    def get_main_page_count_presented() -> Tuple[List[int], List[int]]:
        forward_query = FlaskApp().request(RelationSettings).filter(RelationSettings._main_page_count_title is not None)
        forward_query = forward_query.with_entities(RelationSettings.id)
        forward = [item.id for item in forward_query.all()]

        inverse_query = FlaskApp().request(RelationSettings)\
            .filter(RelationSettings._inverse_main_page_count_title is not None).with_entities(RelationSettings.id)
        inverse = [item.id for item in inverse_query.all()]
        return forward, inverse

    @staticmethod
    def get_foreign_to_show_query(form: FormType):
        query = FlaskApp().request(RelationSettings).filter(RelationSettings._relation_type == form)
        return query.filter(RelationSettings._related_visualization_type != VisualizationType.NOTHING).with_entities(
            RelationSettings.id, RelationSettings._related_visualization_type
        )

    @staticmethod
    def get_by_id(id: int):
        return FlaskApp().request(RelationSettings).filter_by(id=id).first()

    @property
    def relation_type(self) -> FormType:
        return self._relation_type

    @property
    def main_page_count_title(self) -> TranslatedText:
        return json.loads(self._main_page_count_title)

    @main_page_count_title.setter
    @Editable.on_edit
    def main_page_count_title(self, new_value: TranslatedText) -> str:
        self._main_page_count_title = json.dumps(new_value)
        return self._main_page_count_title

    @property
    def inverse_main_page_count_title(self) -> TranslatedText:
        return json.loads(self._inverse_main_page_count_title)

    @inverse_main_page_count_title.setter
    @Editable.on_edit
    def inverse_main_page_count_title(self, new_value: TranslatedText) -> str:
        self._inverse_main_page_count_title = json.dumps(new_value)
        return self._inverse_main_page_count_title

    @property
    def related_visualization_type(self) -> VisualizationType:
        return self._related_visualization_type

    @related_visualization_type.setter
    @Editable.on_edit
    def related_visualization_type(self, new_type: VisualizationType) -> None:
        self._related_visualization_type = new_type

    @property
    def related_visualization_sorting(self) -> int:
        return self._related_visualization_sorting

    @related_visualization_sorting.setter
    @Editable.on_edit
    def related_visualization_sorting(self, new_sorting: int) -> None:
        self._related_visualization_sorting = new_sorting

    @property
    def forward_relation_sheet_name(self) -> str:
        return self._forward_relation_sheet_name

    @forward_relation_sheet_name.setter
    @Editable.on_edit
    def forward_relation_sheet_name(self, new_name: str) -> None:
        self._forward_relation_sheet_name = new_name

    @property
    def inverse_relation_sheet_name(self) -> str:
        return self._inverse_relation_sheet_name

    @inverse_relation_sheet_name.setter
    @Editable.on_edit
    def inverse_relation_sheet_name(self, new_name: str) -> None:
        self._inverse_relation_sheet_name = new_name
