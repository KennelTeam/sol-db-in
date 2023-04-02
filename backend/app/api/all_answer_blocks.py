#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json
from typing import Final

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from .auxiliary import get_request
from ..flask_app import FlaskApp
from ..database import AnswerBlock
from ...constants import ALL_LANGUAGES_TAG


class AllAnswerBlocks(Resource):
    route: Final[str] = '/all_answer_blocks'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        FlaskApp().set_language(ALL_LANGUAGES_TAG)
        result = Response(json.dumps(AnswerBlock.get_all_blocks()), 200)
        return result
