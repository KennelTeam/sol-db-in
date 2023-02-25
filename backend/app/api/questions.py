#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from typing import Tuple, final
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from .auxiliary import HTTPErrorCode, get_request, post_request, post_failure, check_json_format, \
    get_class_item_by_id_request
from backend.app.flask_app import FlaskApp
from backend.app.database import Question, QuestionBlock, QuestionTable, RelationSettings, PrivacySettings, FixedTable
from backend.app.database.question_type import QuestionType
from backend.app.database.answer_block import AnswerBlock
from backend.app.database.formatting_settings import FormattingSettings
from backend.app.database.user import Role
from backend.auxiliary import JSON


class Questions(Resource):
    route: final(str) = '/question'

    @staticmethod
    @jwt_required()
    @get_request()
    def get() -> Response:
        return get_class_item_by_id_request(Question)

    @staticmethod
    @jwt_required()
    @post_request(Role.ADMIN)
    def post() -> Response:
        arguments = Questions._parse_request()
        fail_consistency = Questions._check_arguments_consistency(arguments)
        if fail_consistency is not None:
            return fail_consistency

        formatting_settings, privacy_settings, relation_settings, fail_response = \
            Questions._construct_settings_objects(arguments)
        if fail_response is not None:
            return fail_response

        if arguments['id'] != -1:
            current = Questions._update_existing_question(arguments, formatting_settings, privacy_settings,
                                                          relation_settings)
            if current is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 400)
        else:
            current = Questions._construct_question(arguments, formatting_settings, privacy_settings, relation_settings)
        FlaskApp().flush_to_database()
        return Response(current.id, 200)

    @staticmethod
    def _construct_settings_objects(arguments: JSON) -> \
            Tuple[FormattingSettings | None, PrivacySettings | None, RelationSettings | None, Response | None]:
        formatting_settings, fail_response = Questions._parse_formatting_settings(arguments['formatting_settings'])
        if fail_response is not None:
            return None, None, None, fail_response
        privacy_settings, fail_response = Questions._parse_privacy_settings(arguments['privacy_settings'])
        if fail_response is not None:
            return None, None, None, fail_response
        relation_settings = None
        if arguments['relation_settings'] is not None:
            if arguments['question_type'] != QuestionType.RELATION:
                return None, None, None, post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
            relation_settings, fail_response = Questions._parse_relation_settings(arguments['relation_settings'])
            if fail_response is not None:
                return None, None, None, fail_response
        elif arguments['question_type'] == QuestionType.RELATION:
            return None, None, None, post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
        return formatting_settings, privacy_settings, relation_settings, None

    @staticmethod
    def _update_existing_question(arguments: JSON, formatting_settings: FormattingSettings,
                                  privacy_settings: PrivacySettings,
                                  relation_settings: RelationSettings) -> Question | None:

        current = Question.get_by_id(arguments['id'])
        if current is None:
            return None
        current.privacy_settings.copy(privacy_settings)
        current.formatting_settings.copy(formatting_settings)
        if current.question_type == QuestionType.RELATION:
            current.relation_settings.copy(relation_settings)
        current.text = arguments['text']
        current.short_text = arguments['short_text']
        current.comment = arguments['comment']
        current.related_question_id = arguments['related_question_id']
        return current

    @staticmethod
    def _construct_question(arguments: JSON, formatting_settings: FormattingSettings, privacy_settings: PrivacySettings,
                            relation_settings: RelationSettings) -> Question:
        current = Question(arguments['text'], arguments['short_text'], arguments['question_type'],
                           arguments['comment'], arguments['answer_block_id'], arguments['tag_type_id'],
                           arguments['form_type'], arguments['related_question_id'])
        current.privacy_settings = privacy_settings
        current.formatting_settings = formatting_settings
        if relation_settings is not None:
            current.relation_settings = relation_settings
            FlaskApp().add_database_item(relation_settings)
        FlaskApp().add_database_item(privacy_settings)
        FlaskApp().add_database_item(formatting_settings)
        FlaskApp().add_database_item(current)
        return current

    @staticmethod
    def _check_arguments_consistency(arguments: JSON) -> Response | None:
        if arguments['question_type'] not in QuestionType:
            return post_failure(HTTPErrorCode.INVALID_ARG_FORMAT, 400)
        arguments['question_type'] = QuestionType[arguments['question_type']]
        if arguments['related_question_id'] is not None:
            if Question.get_by_id(arguments['related_question_id']) is None:
                return post_failure(HTTPErrorCode.WRONG_ID, 404)
        if AnswerBlock.get_by_id(arguments['answer_block_id']) is None:
            return post_failure(HTTPErrorCode.WRONG_ID, 404)
        return None

    @staticmethod
    def _parse_relation_settings(relation_json: JSON) -> Tuple[RelationSettings | None, Response | None]:
        res = check_json_format(relation_json, RelationSettings.json_format())
        if res != HTTPErrorCode.SUCCESS:
            return None, post_failure(res, 400)
        return RelationSettings(**relation_json), None

    @staticmethod
    def _parse_privacy_settings(privacy_json: JSON) -> Tuple[PrivacySettings | None, Response | None]:
        res = check_json_format(privacy_json, PrivacySettings.json_format())
        if res != HTTPErrorCode.SUCCESS:
            return None, post_failure(res, 400)
        return PrivacySettings(**privacy_json), None

    @staticmethod
    def _parse_formatting_settings(formatting_json: JSON) -> Tuple[FormattingSettings | None, Response | None]:
        res = check_json_format(formatting_json, FormattingSettings.json_format())
        if res != HTTPErrorCode.SUCCESS:
            return None, post_failure(res, 400)
        block_sorting = formatting_json['block_sorting']
        block_id = formatting_json['block_id']
        show_on_main_page = formatting_json['show_on_main_page']
        if QuestionBlock.get_by_id(block_id) is None:
            return None, post_failure(HTTPErrorCode.WRONG_ID, 404)
        table_id, table_column, fail_response = Questions._parse_table_info(formatting_json)
        if fail_response is not None:
            return None, fail_response
        table_row = None
        fixed_table_id = None
        if 'fixed_table_id' in formatting_json and formatting_json['fixed_table_id'] is not None:
            fixed_table_id = formatting_json['fixed_table_id']
            if FixedTable.get_by_id(fixed_table_id) is None:
                return None, post_failure(HTTPErrorCode.WRONG_ID, 404)
            if 'table_row' not in formatting_json or type(formatting_json['table_row']) != int:
                return None, post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
            table_row = formatting_json['table_row']

        return FormattingSettings(block_sorting, block_id, table_row, table_id, table_column,
                                  show_on_main_page, fixed_table_id), None

    @staticmethod
    def _parse_table_info(formatting_json: JSON) -> Tuple[int | None, int | None, Response | None]:
        table_id = None
        table_column = None
        if 'table_id' in formatting_json and formatting_json['table_id'] is not None:
            table_id = formatting_json['table_id']
            if QuestionTable.get_by_id(table_id) is None:
                return None, None, post_failure(HTTPErrorCode.WRONG_ID, 404)
            if 'table_column' not in formatting_json or type(formatting_json['table_column']) != int:
                return None, None, post_failure(HTTPErrorCode.MISSING_ARGUMENT, 400)
            table_column = formatting_json['table_column']
            if 'fixed_table_id' in formatting_json and formatting_json['fixed_table'] is not None:
                return None, None, post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
            if 'table_row' in formatting_json and formatting_json['table_row'] is not None:
                return None, None, post_failure(HTTPErrorCode.CONFLICTING_ARGUMENTS, 400)
        return table_id, table_column, None

    @staticmethod
    def _parse_request() -> JSON:
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='json', required=False, default=-1)
        parser.add_argument('question_type', type=str, location='json', required=True)
        parser.add_argument('related_question_id', type=int, location='json', required=False, default=None)
        parser.add_argument('answer_block_id', type=int, location='json', required=False, default=None)
        parser.add_argument('deleted', type=bool, location='json', required=False, default=False)

        parser.add_argument('comment', type=dict, location='json', required=True)
        parser.add_argument('text', type=dict, location='json', required=True)
        parser.add_argument('short_text', type=dict, location='json', required=True)

        parser.add_argument('formatting_settings', type=dict, location='json', required=True)
        parser.add_argument('privacy_settings', type=dict, location='json', required=True)
        parser.add_argument('relation_settings', type=dict, location='json', required=False, default=None)

        arguments = parser.parse_args()
        return arguments

