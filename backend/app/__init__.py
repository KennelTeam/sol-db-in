#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from .flask_app import FlaskApp
import backend.app.database
from . import routes
from . import jwt_setup

FlaskApp().init_database()

client = FlaskApp().app.test_client()
