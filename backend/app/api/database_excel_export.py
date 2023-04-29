import json
import os
from typing import Final

import numpy as np
import pandas as pd
from flask import send_from_directory
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from pandas import DataFrame

from backend.app import FlaskApp
from backend.app.api.auxiliary import get_request
from backend.app.database import Answer, Form, Question, QuestionBlock, FormattingSettings, Toponym, AnswerOption, \
    RelationSettings
from backend.app.database.form_type import FormType
from backend.app.database.localization import localize
from backend.app.database.question_type import QuestionType
from backend.app.database.user import Role, User


class DatabaseExcelExport(Resource):
    route: Final[str] = '/export/forms'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get():
        leaders_export_df = DatabaseExcelExport.export_form(form_type=FormType.LEADER)
        projects_export_df = DatabaseExcelExport.export_form(form_type=FormType.PROJECT)

        uploads_path = os.path.join(FlaskApp().app.root_path, FlaskApp().app.config['UPLOAD_FOLDER'])
        file_name = 'forms.xlsx'
        with pd.ExcelWriter(os.path.join(os.path.join(uploads_path, file_name))) as writer:
            leaders_export_df.to_excel(writer, sheet_name='leaders')
            projects_export_df.to_excel(writer, sheet_name='projects')

        return send_from_directory(directory=uploads_path, path=file_name)

    @staticmethod
    def export_form(form_type: FormType) -> DataFrame:
        connection = FlaskApp().db.session.connection()

        answers_query = FlaskApp().request(Answer).filter(Answer._form_id.in_(Form.get_all_ids(form_type=form_type)))
        questions_query = FlaskApp().request(Question).filter_by(_form_type=form_type)
        questions_blocks_query = FlaskApp().request(QuestionBlock).filter_by(_form=form_type)
        formatting_settings_query = FlaskApp().request(FormattingSettings)
        forms_query = FlaskApp().request(Form).filter_by(_form_type=form_type)
        all_forms_query = FlaskApp().request(Form)
        users_query = FlaskApp().request(User)
        toponyms_query = Toponym.query
        answer_options_query = FlaskApp().request(AnswerOption)
        relation_settings_query = FlaskApp().request(RelationSettings)

        answers_df = pd.read_sql_query(answers_query.statement, connection)
        questions_df = pd.read_sql_query(questions_query.statement, connection)
        questions_blocks_df = pd.read_sql_query(questions_blocks_query.statement, connection)
        formatting_settings_df = pd.read_sql_query(formatting_settings_query.statement, connection)
        forms_df = pd.read_sql_query(forms_query.statement, connection)
        all_forms_df = pd.read_sql_query(all_forms_query.statement, connection)
        users_df = pd.read_sql_query(users_query.statement, connection)
        toponyms_df = pd.read_sql_query(toponyms_query.statement, connection)
        answer_options_df = pd.read_sql_query(answer_options_query.statement, connection)
        relation_settings_df = pd.read_sql_query(relation_settings_query.statement, connection)

        questions_df['localized_text'] = questions_df.apply(lambda row: localize(json.loads(row['text'])), axis=1)
        answer_options_df['localized_answer_option'] = answer_options_df.apply(lambda row: localize(json.loads(row['name'])), axis=1)

        questions_df_copy = questions_df[['id', 'localized_text']]
        questions_df_copy.rename(columns={'localized_text': 'localized_text_2'}, inplace=True)
        answers_df.rename(columns={'table_row': 'answer_table_row'}, inplace=True)
        users_df.rename(columns={'name': 'user_name'}, inplace=True)
        toponyms_df.rename(columns={'name': 'toponym_name'}, inplace=True)
        all_forms_df.rename(columns={'name': 'related_form_name'}, inplace=True)

        answers_df = questions_df.merge(answers_df,left_on='id', right_on='question_id'
        ).merge(formatting_settings_df, left_on='formatting_settings', right_on='id'
        ).merge(questions_df_copy, left_on='row_question_id', right_on='id', how='left'
        ).merge(questions_blocks_df, left_on='block_id', right_on='id', how='left'
        ).merge(users_df, left_on='value_int', right_on='id', how='left'
        ).merge(toponyms_df, left_on='value_int', right_on='id', how='left'
        ).merge(answer_options_df, left_on='value_int', right_on='id', how='left'
        ).merge(relation_settings_df, left_on='relation_settings', right_on='id', how='left'
        ).merge(all_forms_df, left_on='value_int', right_on='id', how='left')

        answers_df['localized_text'].loc[answers_df['localized_text_2'].notna()] += ' [' + answers_df['localized_text_2'] + ']'
        answers_df['localized_text'].loc[answers_df['table_id'].notna()] += ' [' + answers_df['answer_table_row'].astype('Int64').astype(str) + ']'

        answers_df['export_value'] = answers_df['value_text']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.USER] = answers_df['user_name']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.LOCATION] = answers_df['toponym_name']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.NUMBER] = answers_df['value_int'].astype('Int64')
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.CHECKBOX] = answers_df['localized_answer_option']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.MULTIPLE_CHOICE] = answers_df['localized_answer_option']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.RELATION] = answers_df['related_form_name']

        cross_table = pd.crosstab(answers_df['form_id'], answers_df['localized_text'],values=answers_df['export_value'], aggfunc=lambda x: ', '.join(map(str, x)))

        sorting_df = answers_df[['localized_text', 'block_sorting', 'sorting']].drop_duplicates(subset='localized_text')
        sorting_df.sort_values(['sorting', 'block_sorting'], inplace=True)
        cross_table = cross_table.reindex(columns=sorting_df['localized_text'])

        cross_table = pd.merge(forms_df[['id', 'name', 'state', 'deleted']], cross_table, left_on='id', right_on='form_id', how='left')
        cross_table['state'] = cross_table.apply(lambda row: row['state'].name, axis=1)
        cross_table['deleted'] = cross_table['deleted'].astype('Int64')

        cross_table.set_index('id', inplace=True)

        return cross_table
