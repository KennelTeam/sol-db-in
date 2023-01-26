#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from .editable_mixin import EditableMixin


visualization_types = {
    'Full': 1,
    'Names only': 2
}


class RelationSettings(EditableMixin, db.Model):
    __tablename__ = 'relation_settings'

    show_in_related = db.Column('show_in_related', db.Boolean, nullable=True)

    related_visualization_type = db.Column('related_visualization_type', db.Integer, nullable=True)
    related_visualization_sorting = db.Column('related_visualization_sorting', db.Integer, nullable=True)

    export_forward_relation = db.Column('export_forward_relation', db.Boolean)
    export_inverse_relation = db.Column('export_inverse_relation', db.Boolean)

    forward_relation_sheet_name = db.Column('forward_relation_sheet_name', db.Boolean)
    inverse_relation_sheet_name = db.Column('inverse_relation_sheet_name', db.Boolean)
