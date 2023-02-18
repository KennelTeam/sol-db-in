#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import datetime

from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from typing import Set

from .error_codes import HTTPErrorCode
from backend.constants import DATETIME_FORMAT
from backend.app.database.form import Form, FormType, FormState
from backend.auxiliary.string_dt import string_to_datetime, datetime_to_string
from ..flask_app import FlaskApp


class Forms(Resource):
    @staticmethod
    @jwt_required()
    def get() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('form_type', type=str, location='json')
        parser.add_argument('answer_filters', type=list, location='json')
        parser.add_argument('name_substr', type=str, location='json', required=False, default='')

        arguments = parser.parse_args()
        ids = None
        for item in arguments['answer_filters']:
            if type(item) != dict:
                return Response({'error': HTTPErrorCode.INVALID_ARG_LOCATION}, 400)
            current_ids = Forms._solve_form_filter(item)
            if current_ids is None:
                return Response({'error': HTTPErrorCode.MISSING_ARGUMENT}, 400)
            if ids is None:
                ids = current_ids
            else:
                ids &= current_ids
        result = [form.to_json() for form in Form.get_by_ids(ids)]
        return Response({'forms': result}, 200)

    @staticmethod
    @jwt_required()
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=False, default=-1)
        parser.add_argument('state', type=str, location='json')
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('form_type', type=str, location='json')
        parser.add_argument('answers', type=list, location='json')

        content = parser.parse_args()
        if content['form_type'] not in FormType:
            return Response({'error': HTTPErrorCode.MISSING_ARGUMENT}, 400)
        form_type = FormType[content['form_type']]

        if content['state'] not in FormState:
            return Response({'error': HTTPErrorCode.MISSING_ARGUMENT}, 400)
        form_state = FormState[content['form_state']]

        if id == -1:
            form = Form(form_type, content['name'], form_state)
            FlaskApp().add_database_item(form)
        else:
            options = Form.get_by_ids({content['id']})
            if len(options) == 0:
                return Response({'error': HTTPErrorCode.WRONG_ID}, 404)
            form = options[0]
        for answer in content['answers']:
            if type(answer) != dict:
                return Response({'error': HTTPErrorCode.INVALID_ARG_TYPE}, 400)
            if 'question_id' not in answer or 'answers' not in answer:
                return Response({'error': HTTPErrorCode.INVALID_ARG_TYPE}, 400)
            if type(answer['answers']) != list:
                return Response({'error': HTTPErrorCode.INVALID_ARG_TYPE}, 400)
            for answer_item in answer['answers']:
                Forms._update_form_answer(form, answer_item)

    @staticmethod
    @jwt_required()
    def _solve_form_filter(filter: dict, name_substring: str) -> Set[int]:
        question_id = filter.get('question_id')
        if question_id is None:
            return None
        row_question_id = filter.get('row_question_id')
        exact_value = filter.get('exact_value')
        if type(exact_value) not in {bool, int, str}:
            return None
        min_value = filter.get('min_value')
        max_value = filter.get('max_value')

        if type(min_value) == str:
            min_value = string_to_datetime(min_value)
        if type(max_value) == str:
            max_value = string_to_datetime(max_value)

        substring = filter.get('substring')
        if type(substring) != str:
            return None

        return Form.filter(name_substr=name_substring, question_id=question_id, exact_value=exact_value,
                           min_value=min_value, max_value=max_value, substring=substring,
                           row_question_id=row_question_id)

    @staticmethod
    def _update_form_answer(form: Form, answer: dict) -> HTTPErrorCode:
        pass
