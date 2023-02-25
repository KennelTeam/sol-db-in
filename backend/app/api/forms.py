#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import json

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from typing import Set, List

from .auxiliary import HTTPErrorCode, get_failure, post_failure, check_json_format, get_request, post_request
from backend.app.database.form import Form, FormType, FormState
from backend.app.database.answer import Answer
from backend.app.database.tag_to_answer import TagToAnswer
from backend.app.database.tag import Tag
from backend.auxiliary.string_dt import string_to_datetime
from backend.auxiliary.types import JSON
from backend.app.database import Question
from backend.app.database.question import AnswerType
from backend.app.database.auxiliary import prettify_answer
from backend.app.database.question_type import QuestionType
from backend.app.flask_app import FlaskApp
from backend.constants import NAME_COLUMN_NAME


class Forms(Resource):
    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('form_type', type=str, location='json')
        parser.add_argument('answer_filters', type=list, location='json')
        parser.add_argument('name_substr', type=str, location='json', required=False, default='')

        arguments = parser.parse_args()
        ids = Form.get_all_ids()
        for item in arguments['answer_filters']:
            if type(item) != dict:
                return get_failure(HTTPErrorCode.INVALID_ARG_LOCATION, 400)
            current_ids = Forms._solve_form_filter(item, arguments['name_substr'])
            if current_ids is None:
                return get_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
            ids &= current_ids
        forms = Form.get_by_ids(ids)
        question_ids = Question.get_only_main_page(FormType[arguments['form_type']])

        result = Forms._prepare_table(forms, question_ids)
        return Response(json.dumps({'table': result}), 200)

    @staticmethod
    @jwt_required()
    @post_request()
    def post() -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=False, default=-1)
        parser.add_argument('state', type=str, location='json')
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('form_type', type=str, location='json')
        parser.add_argument('answers', type=list, location='json')
        parser.add_argument('deleted', type=bool, location='json', required=False, default=False)

        content = parser.parse_args()

        if content['form_type'] not in FormType:
            return post_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        form_type = FormType[content['form_type']]

        if content['state'] not in FormState:
            return post_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        form_state = FormState[content['state']]
        return Forms._update_form_data(content, form_state, form_type, content['deleted'])

    @staticmethod
    def _prepare_table(forms: List[Form], question_ids: List[JSON]) -> List[JSON]:
        name_column = {
            'column_name': NAME_COLUMN_NAME,
            'values': [
                {
                    "answers": [{
                        'type': QuestionType.RELATION.name,
                        'id': item.id,
                        'value': item.name
                    }]
                } for item in forms
            ]
        }

        result = [name_column]
        for item in question_ids:
            q_type = item['type']
            question = item['question']
            answers = []
            for form in forms:
                answers.append(
                    Forms._get_forms_answer_prettified(form.id, question.id, q_type)
                )
            result.append({
                'column_name': question.short_text,
                'values': answers
            })

        return result

    @staticmethod
    def _get_forms_answer_prettified(form_id: int, question_id: int, q_type: AnswerType):
        ans_object = {"answers": []}
        if q_type == AnswerType.FORWARD_COUNT:
            ans_object["answers"].append({
                'type': QuestionType.NUMBER.name,
                'value': Answer.count_forms_answers(form_id, question_id)
            })
        elif q_type == AnswerType.INVERSE_COUNT:
            ans_object["answers"].append({
                'type': QuestionType.NUMBER.name,
                'value': Answer.count_inverse_answers(form_id, question_id)
            })
        else:
            form_answers = Answer.get_form_answers(form_id, question_id)
            ans_object["answers"] = [
                prettify_answer(answer) for answer in form_answers
            ]
        return ans_object

    @staticmethod
    def _solve_form_filter(filter: JSON, name_substring: str) -> Set[int]:
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
    def _update_form_data(content: JSON, form_state: FormState, form_type: FormType, deleted: bool) -> Response:
        if content['id'] == -1:
            form = Form(form_type, content['name'], form_state)
            FlaskApp().add_database_item(form)
            FlaskApp().flush_to_database()
        else:
            options = Form.get_by_ids({content['id']})
            if len(options) == 0:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
            form = options[0]
            form.deleted = deleted
        for answer in content['answers']:
            status = Forms._check_answer_object_correctness(answer)
            if status != HTTPErrorCode.SUCCESS:
                return post_failure(status, 400)
            for answer_item in answer['answers']:
                status = Forms._update_form_answer(form, answer_item)
                if status != HTTPErrorCode.SUCCESS:
                    return post_failure(status, 400)

        FlaskApp().flush_to_database()
        return Response(response=form.id, status=200)

    @staticmethod
    def _check_answer_object_correctness(answer: JSON) -> HTTPErrorCode:
        if type(answer) != dict:
            return HTTPErrorCode.INVALID_ARG_TYPE
        if 'question_id' not in answer or 'answers' not in answer:
            return HTTPErrorCode.INVALID_ARG_TYPE
        if type(answer['answers']) != list:
            return HTTPErrorCode.INVALID_ARG_TYPE
        return HTTPErrorCode.SUCCESS

    @staticmethod
    def _update_form_answer(form: Form, answer: JSON) -> HTTPErrorCode:
        check_status = check_json_format(answer, Answer.json_format())
        if check_status != HTTPErrorCode.SUCCESS:
            return check_status
        if 'form_id' in answer and answer['form_id'] != form.id:
            return HTTPErrorCode.CONFLICTING_ARGUMENTS
        if 'id' in answer and answer['id'] > 0:
            if type(answer['id']) != int:
                return HTTPErrorCode.INVALID_ARG_TYPE
            current_ans = Answer.get_by_id(answer['id'])
            if current_ans is None:
                return HTTPErrorCode.WRONG_ID
            if current_ans.form_id != form.id or answer['row_question_id'] != current_ans.row_question_id \
                    or answer['question_id'] != current_ans.question_id:
                return HTTPErrorCode.CONFLICTING_ARGUMENTS
            current_ans.value = answer['value']
            current_ans.table_row = answer['table_row']
        else:
            current_ans = Answer(answer['question_id'], form.id, answer['value'],
                                 answer['table_row'], answer['row_question_id'])
            FlaskApp().add_database_item(current_ans)
        return Forms._update_answer_tags(current_ans.id, answer['tags'])

    @staticmethod
    def _update_answer_tags(answer_id: int, tags: List[JSON]) -> HTTPErrorCode:
        tags_set = set()
        for tag in tags:
            status = check_json_format(tag, {'id': int})
            if status != HTTPErrorCode.SUCCESS:
                return status
            if Tag.get_by_id(tag['id']) is None:
                return HTTPErrorCode.WRONG_ID
            tags.append(tag['id'])
        old_tag_ids = TagToAnswer.get_answers_tag_ids(answer_id)
        for tag_id in old_tag_ids:
            if tag_id not in tags_set:
                TagToAnswer.remove_tag(tag_id, answer_id)
            else:
                tags_set.remove(tag_id)
        for new_tag in tags_set:
            TagToAnswer.add_tag(new_tag, answer_id)
        return HTTPErrorCode.SUCCESS
