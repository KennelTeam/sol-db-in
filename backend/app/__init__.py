#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from . import routes
from .flask_app import FlaskApp
import backend.app.database

FlaskApp().init_database()
