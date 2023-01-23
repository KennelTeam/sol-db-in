#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

from . import routes
from . import database
