#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

from flask import Flask
from flask_restful import Api  # type: ignore[import]


app = Flask(__name__)
api = Api(app)

from . import routes
from . import database
from .database import db

with app.app_context():
    db.create_all()
    db.session.commit()
    print("Database initialized")

print("init finished")
