#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import os
from pathlib import Path

from sqlalchemy import NullPool
from sqlalchemy.orm import Query
from flask import Flask, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from cheroot.wsgi import Server, PathInfoDispatcher
from backend.auxiliary.singleton import Singleton
from backend.constants import DB_ENGINE, MODE, DB_CHARSET, PORT, NUM_THREADS, REQUEST_CONTEXT_USE_DELETED_ITEMS, \
    DEFAULT_LANGUAGE
from flask_cors import CORS


class FlaskApp(metaclass=Singleton):
    _app: Flask = None
    _api: Api = None
    _db: SQLAlchemy = None

    def _configure_db(self) -> None:
        mode_prefix = "DEVELOP_" if MODE == "dev" else "PRODUCTION_"

        username = os.getenv(mode_prefix + "USER")
        password = os.getenv(mode_prefix + "PASSWORD")
        database = os.getenv(mode_prefix + "DATABASE_NAME")

        url = f'{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'

        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'{DB_ENGINE}://{username}:{password}@{url}/{database}?charset={DB_CHARSET}'

        self._db = SQLAlchemy(self.app)

    def _configure_api(self) -> None:
        self._api = Api(self.app)

    def __init__(self):
        self._app = Flask(__name__, static_folder='../../frontend/build')
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'poolclass': NullPool,
        }
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        Path(os.path.join(self.app.root_path, self.app.config['UPLOAD_FOLDER'])).mkdir(exist_ok=True)
        CORS(self.app, supports_credentials=True)
        self._configure_api()
        self._configure_db()

    def init_database(self) -> None:
        with self.app.app_context():
            self.db.create_all()
            self.db.session.commit()  # pylint: disable=no-member
            print("Database initialized")
        print("init finished")

    # Request query from editable table
    # I thought to place it in the Editable class, but then realized that calls will be like:
    # TableClassName.request(TableClassName).filter(...)... - very strange
    # Calls like FlaskApp().request(TableClassName).filter(...)... - seem more understandable
    def request(self, table) -> Query:
        if 'dev_variables' in g and g.dev_variables.get(REQUEST_CONTEXT_USE_DELETED_ITEMS, None):
            return table.query
        return table.query.filter_by(_deleted=False)

    def run_dev_server(self) -> None:
        self.app.run(host='0.0.0.0', port=PORT, debug=True)

    def run_prod_server(self) -> None:
        dispatcher = PathInfoDispatcher({'/': self.app})
        server = Server(('0.0.0.0', PORT), dispatcher, numthreads=NUM_THREADS)
        try:
            print(f"the server is working at http://127.0.0.1:{PORT}")
            server.start()
        except KeyboardInterrupt:
            server.stop()

    @property
    def app(self) -> Flask:
        return self._app

    @property
    def api(self) -> Api:
        return self._api

    @property
    def db(self) -> SQLAlchemy:
        return self._db

    def use_deleted_items_in_this_request(self):
        if 'dev_variables' not in g:
            g.dev_variables = {}
        g.dev_variables[REQUEST_CONTEXT_USE_DELETED_ITEMS] = True

    def set_language(self, lang: str):
        if 'dev_variables' not in g:
            g.dev_variables = {}
        g.dev_variables['language'] = lang

    def get_language(self) -> str:
        if 'dev_variables' not in g:
            g.dev_variables = {}
            return DEFAULT_LANGUAGE
        return g.dev_variables['language']

    def add_database_item(self, item):
        return self.db.session.add(item)

    def flush_to_database(self):
        return self.db.session.commit()


# https://stackoverflow.com/questions/22256862/flask-how-to-store-and-retrieve-a-value-bound-to-the-request
@FlaskApp().app.after_request
def pre_request_callbacks(response):
    # clear the dev variables associated with current request
    values = g.get('dev_variables', {})
    values.clear()

    return response
