#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from .flask_app import FlaskApp


@FlaskApp().app.route("/", methods=['GET'])
def hello_world():
    return 'Hello World!'
