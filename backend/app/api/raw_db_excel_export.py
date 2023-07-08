import os
from typing import Final

import pandas as pd
from flask import Response, send_from_directory
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from backend.app import FlaskApp
from backend.app.api.auxiliary import get_request
from backend.app.database.user import Role
from backend.constants import UPLOADS_DIRECTORY


class RawDbExcelExport(Resource):
    route: Final[str] = '/export/database'

    @staticmethod
    @jwt_required()
    @get_request(Role.ADMIN)
    def get() -> Response:
        file_name = 'database.xlsx'
        connection = FlaskApp().db.session.connection()
        with pd.ExcelWriter(os.path.join(UPLOADS_DIRECTORY, file_name), engine='xlsxwriter', engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            for table_name in FlaskApp().db.metadata.tables.keys():
                pd.read_sql_table(table_name, connection).to_excel(writer, sheet_name=table_name)

        return send_from_directory(directory=UPLOADS_DIRECTORY, path=file_name)
