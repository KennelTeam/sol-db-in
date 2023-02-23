#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import HTTPErrorCode, get_failure, get_request
from backend.app.database.toponym import Toponym


class Toponyms(Resource):
    @staticmethod
    @jwt_required()
    @get_request()
    def get():
        result = [
            root.to_json(with_children=True) for root in Toponym.get_roots()
        ]
        return Response({"roots": result}, 200)
