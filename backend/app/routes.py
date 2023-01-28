#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from .flask_app import app_instance


@app_instance.route("/", methods=['GET'])
def hello_world():
    return 'Hello World!'
