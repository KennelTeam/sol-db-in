#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from typing import Final

from .auxiliary import get_request
from backend.app.database.tag import Tag
from .. import FlaskApp


class AllTags(Resource):
    route: Final[str] = '/all_tags'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        tags = FlaskApp().request(Tag).all()

        result = [t.to_json() for t in tags]
        return Response(json.dumps({'data':result}), 200)
