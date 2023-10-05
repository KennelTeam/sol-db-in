import json
import os
from typing import Final

import pandas as pd
from flask import send_from_directory, Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from pandas import DataFrame

from backend.app.flask_app import FlaskApp
from backend.app.api.auxiliary import get_request
from backend.app.database import Answer, Form, Question, QuestionBlock, FormattingSettings, Toponym, AnswerOption, \
    RelationSettings, TagToAnswer, Tag
from backend.app.database.form_type import FormType
from backend.app.database.localization import localize
from backend.app.database.question_type import QuestionType
from backend.app.database.user import Role, User
from backend.constants import UPLOADS_DIRECTORY


class DatabaseExcelExport(Resource):
    route: Final[str] = '/export/forms'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        leaders_answers_df, leaders_tags = DatabaseExcelExport._get_all_answers_df(form_type=FormType.LEADER)
        projects_answers_df, projects_tags = DatabaseExcelExport._get_all_answers_df(form_type=FormType.PROJECT)

        leaders_export_df = DatabaseExcelExport._export_form(FormType.LEADER, leaders_answers_df.copy())
        projects_export_df = DatabaseExcelExport._export_form(FormType.PROJECT, projects_answers_df.copy())

        leaders_tags_export_df = DatabaseExcelExport._export_form(FormType.LEADER, leaders_tags.copy())
        projects_tags_export_df = DatabaseExcelExport._export_form(FormType.PROJECT, projects_tags.copy())

        relation_sheets_df = leaders_answers_df[['forward_relation_sheet_name', 'block_id']].groupby('forward_relation_sheet_name').first().reset_index()
        file_name = 'forms.xlsx'
        with pd.ExcelWriter(os.path.join(UPLOADS_DIRECTORY, file_name), engine='xlsxwriter', engine_kwargs={'options': {'strings_to_urls': False}}) as writer:  # pylint: disable=abstract-class-instantiated
            leaders_export_df.to_excel(writer, sheet_name='leaders')
            projects_export_df.to_excel(writer, sheet_name='projects')

            leaders_tags_export_df.to_excel(writer, sheet_name='leaders_tags')
            projects_tags_export_df.to_excel(writer, sheet_name='projects_tags')

            DatabaseExcelExport._export_tags_sheet().to_excel(writer, sheet_name='tags')
            for _, relation_sheet in relation_sheets_df.iterrows():
                DatabaseExcelExport._export_relations(relation_sheet['block_id'], leaders_answers_df.copy()).to_excel(
                    writer, sheet_name=relation_sheet['forward_relation_sheet_name'])

        return send_from_directory(directory=UPLOADS_DIRECTORY, path=file_name)

    @staticmethod
    def _get_all_answers_df(form_type: FormType) -> [DataFrame, DataFrame]:
        connection = FlaskApp().db.session.connection()

        answers_query = FlaskApp().request(Answer).filter(Answer._form_id.in_(Form.get_all_ids(form_type=form_type)))  # pylint: disable=protected-access
        questions_query = FlaskApp().request(Question).filter_by(_form_type=form_type)
        questions_blocks_query = FlaskApp().request(QuestionBlock).filter_by(_form=form_type)
        formatting_settings_query = FlaskApp().request(FormattingSettings)
        all_forms_query = FlaskApp().request(Form)
        users_query = FlaskApp().request(User)
        toponyms_query = Toponym.query
        answer_options_query = FlaskApp().request(AnswerOption)
        relation_settings_query = FlaskApp().request(RelationSettings)
        tags_query = TagToAnswer.query

        answers_df = pd.read_sql_query(answers_query.statement, connection)
        questions_df = pd.read_sql_query(questions_query.statement, connection)
        questions_blocks_df = pd.read_sql_query(questions_blocks_query.statement, connection)
        formatting_settings_df = pd.read_sql_query(formatting_settings_query.statement, connection)
        all_forms_df = pd.read_sql_query(all_forms_query.statement, connection)
        users_df = pd.read_sql_query(users_query.statement, connection)
        toponyms_df = pd.read_sql_query(toponyms_query.statement, connection)
        answer_options_df = pd.read_sql_query(answer_options_query.statement, connection)
        relation_settings_df = pd.read_sql_query(relation_settings_query.statement, connection)
        tags_df = pd.read_sql_query(tags_query.statement, connection)

        questions_df['localized_text'] = questions_df.apply(lambda row: localize(json.loads(row['text'])), axis=1)
        answer_options_df['localized_answer_option'] = answer_options_df.apply(lambda row: localize(json.loads(row['name'])), axis=1)

        questions_df_copy = questions_df[['id', 'localized_text']]
        questions_df_copy.rename(columns={'localized_text': 'localized_text_2'}, inplace=True)
        answers_df.rename(columns={'table_row': 'answer_table_row'}, inplace=True)
        users_df.rename(columns={'name': 'user_name'}, inplace=True)
        toponyms_df.rename(columns={'name': 'toponym_name'}, inplace=True)
        all_forms_df.rename(columns={'name': 'related_form_name'}, inplace=True)

        answers_df["row_question_id"] = answers_df["row_question_id"].astype('float64')
        answer_options_df["id"] = answer_options_df["id"].astype('float64')

        answers_df_copy = answers_df.copy()

        answers_df = questions_df.merge(answers_df, left_on='id', right_on='question_id'
        ).merge(formatting_settings_df, left_on='formatting_settings', right_on='id'
        ).merge(questions_df_copy, left_on='row_question_id', right_on='id', how='left'
        ).merge(questions_blocks_df, left_on='block_id', right_on='id', how='left'
        ).merge(users_df, left_on='value_int', right_on='id', how='left'
        ).merge(toponyms_df, left_on='value_int', right_on='id', how='left')

        answers_df = answers_df.merge(answer_options_df, left_on='value_int', right_on='id', how='left')
        relation_settings_df["id"] = relation_settings_df["id"].astype("float64")

        answers_df["relation_settings"] = answers_df["relation_settings"].astype("float64")
        answers_df = answers_df.merge(relation_settings_df, left_on='relation_settings', right_on='id', how='left')

        all_forms_df["id"] = all_forms_df["id"].astype("float64")
        answers_df = answers_df.merge(all_forms_df, left_on='value_int', right_on='id', how='left')

        answers_df['localized_text'].loc[answers_df['localized_text_2'].notna()] += ' [' + answers_df['localized_text_2'] + ']'

        answers_df['export_value'] = answers_df['value_text']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.USER] = answers_df['user_name']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.LOCATION] = answers_df['toponym_name']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.NUMBER] = answers_df['value_int'].astype('Int64')
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.CHECKBOX] = answers_df['localized_answer_option']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.MULTIPLE_CHOICE] = answers_df['localized_answer_option']
        answers_df['export_value'].loc[answers_df['question_type'] == QuestionType.RELATION] = answers_df['related_form_name']

        answers_df_copy = answers_df_copy.merge(tags_df, left_on='id', right_on='answer_id')
        answers_df_copy = questions_df.merge(answers_df_copy, left_on='id', right_on='question_id'
        ).merge(formatting_settings_df, left_on='formatting_settings', right_on='id'
        ).merge(questions_df_copy, left_on='row_question_id', right_on='id', how='left'
        ).merge(questions_blocks_df, left_on='block_id', right_on='id', how='left'
        ).merge(users_df, left_on='value_int', right_on='id', how='left'
        ).merge(toponyms_df, left_on='value_int', right_on='id', how='left')
        answers_df_copy['export_value'] = answers_df_copy['tag_id']

        return answers_df, answers_df_copy

    @staticmethod
    def _export_tags_sheet() -> DataFrame:
        tags_query = FlaskApp().request(Tag)
        tags_df = pd.read_sql_query(tags_query.statement, FlaskApp().db.session.connection())
        print(tags_df)
        tags_df["parent_id"] = tags_df.apply(lambda row: -1 if row["parent_id"] != row['parent_id'] else row["parent_id"], axis=1)
        tags_df['text'] = tags_df.apply(lambda row: localize(json.loads(row['text'])), axis=1)
        print(tags_df)
        tags_copy1 = tags_df.copy().drop(["deleted", "create_timestamp", "type_id"], axis=1)
        tags_copy2 = tags_df.copy().drop(["deleted", "create_timestamp", "type_id"], axis=1)
        tags_copy3 = tags_df.copy().drop(["deleted", "create_timestamp", "type_id"], axis=1)

        tags_df.set_index('id')
        tags_df = tags_df.merge(tags_copy1, left_on='parent_id', right_on='id'
                    ).merge(tags_copy2, left_on='parent_id_y', right_on='id'
                    )
        tags_df = tags_df.merge(tags_copy3, left_on='parent_id', right_on='id')
        return tags_df

    @staticmethod
    def _export_form(form_type: FormType, answers_df: DataFrame) -> DataFrame:
        forms_query = FlaskApp().request(Form).filter_by(_form_type=form_type)
        forms_df = pd.read_sql_query(forms_query.statement, FlaskApp().db.session.connection())
        answers_df['export_value'].loc[answers_df['table_id'].notna()] = answers_df['answer_table_row'].astype('Int64').astype(str) + '. ' + answers_df['export_value'].astype(str)

        cross_table = pd.crosstab(answers_df['form_id'], answers_df['localized_text'], values=answers_df['export_value'],
                                  aggfunc=lambda export_value: ', '.join(sorted(map(str, export_value))))

        sorting_df = answers_df[['localized_text', 'block_sorting', 'sorting']].drop_duplicates(subset='localized_text')
        sorting_df.sort_values(['sorting', 'block_sorting'], inplace=True)
        cross_table = cross_table.reindex(columns=sorting_df['localized_text'])

        cross_table = pd.merge(forms_df[['id', 'name', 'state', 'deleted']], cross_table, left_on='id', right_on='form_id', how='left')
        cross_table['state'] = cross_table.apply(lambda row: row['state'].name, axis=1)
        cross_table['deleted'] = cross_table['deleted'].astype('Int64')
        cross_table.set_index('id', inplace=True)

        return cross_table

    @staticmethod
    def _export_relations(recommendations_block_id: int, answers_df: DataFrame) -> DataFrame:
        forms_query = FlaskApp().request(Form).filter_by(_form_type=FormType.LEADER)
        forms_df = pd.read_sql_query(forms_query.statement, FlaskApp().db.session.connection())

        answers_df = answers_df[answers_df['block_id'] == recommendations_block_id]

        answers_df['id'] = answers_df['form_id'] + 0.1 * answers_df['answer_table_row']
        cross_table = pd.crosstab(answers_df['id'], answers_df['localized_text'], values=answers_df['export_value'], aggfunc='first')
        cross_table.index = cross_table.index.astype(str)

        sorting_df = answers_df[['localized_text', 'sorting']].drop_duplicates(subset='localized_text')
        sorting_df.sort_values('sorting', inplace=True)
        cross_table = cross_table.reindex(columns=sorting_df['localized_text'])

        cross_table['recommender_id'] = list(map(lambda x: int(x.split('.')[0]), cross_table.index.values))
        cross_table = pd.merge(forms_df[['id', 'name']], cross_table, left_on='id', right_on='recommender_id')
        cross_table.drop('recommender_id', axis=1, inplace=True)
        cross_table.rename(columns={'name': 'Recommender'}, inplace=True)
        cross_table.set_index('id', inplace=True)

        return cross_table
