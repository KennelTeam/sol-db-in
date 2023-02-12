#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from sqlalchemy import func
from backend.app.flask_app import FlaskApp


class EditableIdHolder(FlaskApp().db.Model):
    __tablename__ = 'editable_id_holder'
    id = FlaskApp().db.Column('id', FlaskApp().db.Integer, primary_key=True, autoincrement=False)

    def __init__(self):
        obj = EditableIdHolder.query.order_by(EditableIdHolder.id.desc()).first()
        if obj is None:
            self.id = 0
        else:
            self.id = obj.id + 1
        FlaskApp().add_database_item(self)
