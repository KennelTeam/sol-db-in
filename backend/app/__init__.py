#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from . import routes
from .flask_app import FlaskApp
from .database.tables import *

FlaskApp().init_database()
