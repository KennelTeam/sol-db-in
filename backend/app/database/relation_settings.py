#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from backend.auxiliary import JSON
from .editable import Editable
from .visualization_type import VisualizationType
from .relation_type import RelationType
from .form_type import FormType
from sqlalchemy import or_


class RelationSettings(Editable, FlaskApp().db.Model):
    __tablename__ = 'relation_settings'

    _relation_type = FlaskApp().db.Column('relation_type', FlaskApp().db.Enum(RelationType))

    _related_visualization_type = FlaskApp().db.Column('related_visualization_type',
                                                       FlaskApp().db.Enum(VisualizationType), nullable=True)
    _related_visualization_sorting = FlaskApp().db.Column('related_visualization_sorting',
                                                          FlaskApp().db.Integer, nullable=True)

    _export_forward_relation = FlaskApp().db.Column('export_forward_relation', FlaskApp().db.Boolean)
    _export_inverse_relation = FlaskApp().db.Column('export_inverse_relation', FlaskApp().db.Boolean)

    _forward_relation_sheet_name = FlaskApp().db.Column('forward_relation_sheet_name',
                                                        FlaskApp().db.Boolean, nullable=True)
    _inverse_relation_sheet_name = FlaskApp().db.Column('inverse_relation_sheet_name',
                                                        FlaskApp().db.Boolean, nullable=True)

    def __init__(self, relation_type: RelationType,
                 related_visualization_type: VisualizationType, related_visualization_sorting: int = 0,
                 export_forward_relation: bool = False, export_inverse_relation: bool = False,
                 forward_relation_sheet_name: str = None, inverse_relation_sheet_name: str = None) -> None:

        super(Editable).__init__()
        self._relation_type = relation_type
        self.related_visualization_type = related_visualization_type
        self.related_visualization_sorting = related_visualization_sorting

        self.export_forward_relation = export_forward_relation
        self.export_inverse_relation = export_inverse_relation
        self.forward_relation_sheet_name = forward_relation_sheet_name
        self.inverse_relation_sheet_name = inverse_relation_sheet_name

    def to_json(self) -> JSON:
        return super(Editable).to_json() | {
            'related_visualization_type': self.related_visualization_type,
            'related_visualization_sorting': self.related_visualization_sorting,
            'export_forward_relation': self.export_forward_relation,
            'export_inverse_relation': self.export_inverse_relation,
            'forward_relation_sheet_name': self.forward_relation_sheet_name,
            'inverse_relation_sheet_name': self.inverse_relation_sheet_name
        }

    @staticmethod
    def get_foreign_to_show_query(form: FormType):
        if form == FormType.LEADER:
            query = FlaskApp().request(RelationSettings).filter(
                    or_(RelationSettings._relation_type == RelationType.LEADER_TO_LEADER,
                        RelationSettings._relation_type == RelationType.PROJECT_TO_LEADER))
        else:
            query = FlaskApp().request(RelationSettings).filter(
                or_(RelationSettings._relation_type == RelationType.LEADER_TO_PROJECT,
                    RelationSettings._relation_type == RelationType.PROJECT_TO_PROJECT))
        return query.filter(RelationSettings._related_visualization_type != VisualizationType.NOTHING).with_entities(
            RelationSettings.id, RelationSettings._related_visualization_type
        )

    @staticmethod
    def get_by_id(id: int):
        return FlaskApp().request(RelationSettings).filter_by(id=id).first()

    @property
    def relation_type(self) -> RelationType:
        return self._relation_type

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
    def export_forward_relation(self) -> bool:
        return self._export_forward_relation

    @export_forward_relation.setter
    @Editable.on_edit
    def export_forward_relation(self, new_value: bool) -> None:
        self._export_forward_relation = new_value

    @property
    def export_inverse_relation(self) -> bool:
        return self._export_inverse_relation

    @export_inverse_relation.setter
    @Editable.on_edit
    def export_inverse_relation(self, value: bool) -> None:
        self._export_inverse_relation = value

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
