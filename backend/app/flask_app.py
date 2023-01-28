#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved

from flask import Flask
from flask_restful import Api


app_instance = Flask(__name__)
api_instance = Api(app_instance)
