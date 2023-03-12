#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request
from backend.app.database.toponym import Toponym


class ToponymTree(Resource):
    route: Final[str] = '/toponym_tree'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        result = [
            root.to_json(with_children=True) for root in Toponym.get_roots()
        ]
        return Response(json.dumps({"roots": result}), 200)
