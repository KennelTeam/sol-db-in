#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from backend.app.flask_app import FlaskApp
from backend.auxiliary.types import JSON
from typing import List


# I decided not to use Editable base class, because it's too easy to add and delete tags to answers
# Too easy to use the schema of saving changes and deleted/not deleted objects
class TagToAnswer(FlaskApp().db.Model):
    __tablename__ = 'tag_to_answer'
    _id = FlaskApp().db.Column('id', FlaskApp().db.Integer, primary_key=True, unique=True)
    _tag_id = FlaskApp().db.Column('tag_id', FlaskApp().db.ForeignKey('tags.id'), nullable=False)
    _answer_id = FlaskApp().db.Column('answer_id', FlaskApp().db.ForeignKey('answers.id'), nullable=False)

    def __init__(self, tag_id: int, answer_id: int):
        self._tag_id = tag_id
        self._answer_id = answer_id

    def to_json(self) -> JSON:
        return {
            'id': self.id,
            'tag_id': self.tag_id,
            'answer_id': self.answer_id
        }

    @staticmethod
    def count_tag_usage(tag_id: int) -> int:
        return TagToAnswer.query.filter_by(_tag_id=tag_id).count()

    @staticmethod
    def get_answers_tags(answer_id: int) -> List[JSON]:
        tags = TagToAnswer.query.filter_by(_answer_id=answer_id)
        tags = tags.all()
        return [item.tag_id for item in tags]

    @staticmethod
    def get_answers_tag_ids(answer_id: int) -> List[int]:
        return [item['id'] for item in TagToAnswer.get_answers_tags(answer_id)]

    @staticmethod
    def add_tag(tag_id: int, answer_id: int) -> 'TagToAnswer':
        item = TagToAnswer.query.filter_by(_tag_id=tag_id, _answer_id=answer_id).first()
        if item is None:
            item = TagToAnswer(tag_id, answer_id)
            FlaskApp().add_database_item(item)
            return item
        return item

    @staticmethod
    def remove_tag(tag_id: int, answer_id: int):
        TagToAnswer.query.filter_by(_tag_id=tag_id, _answer_id=answer_id).delete()

    @property
    def tag_id(self):
        return self._tag_id

    @property
    def answer_id(self):
        return self._answer_id

    @property
    def id(self):
        return self._id
