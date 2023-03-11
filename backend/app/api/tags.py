#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, post_failure, get_request, post_request, get_class_item_by_id_request, \
    create_standard_reqparser, standard_text_object_update
from backend.app.database.tag import Tag
from backend.app.flask_app import FlaskApp
from ..database.user import Role


class Tags(Resource):
    route: Final[str] = '/tags'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return get_class_item_by_id_request(Tag)

    @staticmethod
    @jwt_required()
    @post_request(Role.EDITOR)
    def post() -> Response:
        parser = create_standard_reqparser()
        parser.add_argument('type_id', type=int, location='json', required=False, default=-1)
        parser.add_argument('parent_id', type=int, location='json', required=False, default=None)
        arguments = parser.parse_args()

        if arguments['parent_id'] is not None:
            if Tag.get_by_id(arguments['parent_id']) is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
        if arguments['id'] != -1:
            return standard_text_object_update(Tag, arguments)

        if arguments['type_id'] == -1:
            return post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        current = Tag(arguments['name'], arguments['type_id'], arguments['parent_id'])
        FlaskApp().add_database_item(current)
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)
