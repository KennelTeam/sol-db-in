#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from cheroot.wsgi import Server, PathInfoDispatcher
from backend.auxiliary.singleton import Singleton
from backend.constants import DB_ENGINE, MODE, DB_CHARSET, PORT, NUM_THREADS
import os


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
        self._app = Flask(__name__)
        self._configure_api()
        self._configure_db()

    def init_database(self) -> None:
        with self.app.app_context():
            self.db.create_all()
            self.db.session.commit()  # pylint: disable=no-member
            print("Database initialized")
        print("init finished")

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

    # This is needed for creating route decorator since python bans calls inside a decorator like:
    # @FlaskApp().app.route(...)
    # ----------^----------- this call raises a syntax error
    # So as a kind of dirty hack I created this static method
    # IDEA for future: maybe it's better to make all the properties above static methods instead
    @staticmethod
    def route(*args, **kwargs):
        return FlaskApp().app.route(*args, **kwargs)
