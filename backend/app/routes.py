#  Copyright (c) 2020-2020-2023. KennelTeam.
#  All rights reserved.

from app import app


@app.route("/", methods=['GET'])
def hello_world():
    return 'Hello World!'
