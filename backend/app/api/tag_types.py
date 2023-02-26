#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request, post_request, get_class_item_by_id_request, \
    create_standard_reqparser, standard_text_object_update
from backend.app.flask_app import FlaskApp
from ..database import TagType
from ..database.user import Role


class TagTypes(Resource):
    route: final(str) = '/tag_type'

    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        return get_class_item_by_id_request(TagType)

    @staticmethod
    @jwt_required()
    @post_request(Role.EDITOR)
    def post():
        parser = create_standard_reqparser()
        arguments = parser.parse_args()

        if arguments['id'] != -1:
            return standard_text_object_update(TagType, arguments)

        current = TagType(arguments['name'])
        FlaskApp().add_database_item(current)
        FlaskApp().flush_to_database()
        return Response(str(current.id), 200)

