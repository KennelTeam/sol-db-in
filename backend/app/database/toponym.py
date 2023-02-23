#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from backend.constants import MAX_TOPONYM_SIZE
from backend.auxiliary import JSON
from typing import List


class Toponym(FlaskApp().db.Model):
    __tablename__ = 'toponyms'
    id = FlaskApp().db.Column('id', FlaskApp().db.Integer, primary_key=True, unique=True)
    name = FlaskApp().db.Column('name', FlaskApp().db.Text(MAX_TOPONYM_SIZE))
    parent_id = FlaskApp().db.Column('parent_id', FlaskApp().db.ForeignKey('toponyms.id'), nullable=True, default=None)

    @staticmethod
    def get_all() -> List['Toponym']:
        return Toponym.query.all()

    @staticmethod
    def get_by_name(name: str) -> 'Toponym':
        return Toponym.query.filter_by(name=name).first()

    @staticmethod
    def get_by_id(id: int) -> 'Toponym':
        return Toponym.query.filter_by(id=id).first()

    def __init__(self, name: str, parent_name: str = None) -> None:
        parent = Toponym.get_by_name(parent_name)
        if parent is not None:
            self.parent_id = parent.id
        self.name = name

    @staticmethod
    def get_roots() -> List['Toponym']:
        return Toponym.query.filter_by(parent_id=None).all()

    def to_json(self, with_children: bool = False) -> JSON:
        result = {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id
        }
        if with_children:
            children = Toponym.query.filter_by(parent_id=self.id).all()
            result['children'] = [item.to_json(with_children=True) for item in children]
        return result

    def get_ancestors(self) -> List['Toponym']:
        result = [self]
        current = self.parent_id

        # not sure about correctness of this check: int NULL value might be 0 - IDK
        while current is not None:
            node = Toponym.query.filter_by(id=current).first()
            result.append(node)
            current = node.parent_id
        return result

    @staticmethod
    def search_by_name(name_substring: str) -> List['Toponym']:
        return Toponym.query.filter(Toponym.name.like(f"%{name_substring}%")).all()
