from . import db
from .. import app


def initialize_database():
    with app.app_context():
        db.create_all()
        db.session.commit()  # pylint: disable=no-member
        print("Database initialized")

    print("init finished")
