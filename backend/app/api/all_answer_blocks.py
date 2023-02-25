#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request
from ..database import AnswerBlock


class AllAnswerBlocks(Resource):
    route: final(str) = '/all_answer_blocks'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return Response(json.dumps(AnswerBlock.get_all_blocks()), 200)
