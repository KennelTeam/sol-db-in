#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from .auxiliary import get_request, post_request, get_class_item_by_id_request, \
    create_standard_reqparser, standard_text_object_update
from backend.app.flask_app import FlaskApp
from ..database import TagType
from ..database.user import Role
from ...constants import ALL_LANGUAGES_TAG


class TagTypes(Resource):
    route: Final[str] = '/tag_type'

    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        old_lang = current_user.selected_language
        current_user.selected_language = ALL_LANGUAGES_TAG
        result = get_class_item_by_id_request(TagType)
        current_user.selected_language = old_lang
        return result

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

