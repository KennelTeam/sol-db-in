#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request
from backend.app.database.toponym import Toponym


class AllToponyms(Resource):
    route: Final[str] = '/all_toponyms'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        results = [item.to_json() for item in Toponym.get_all()]
        return Response(json.dumps(results), 200)
