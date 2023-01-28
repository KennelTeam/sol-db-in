from . import db
from .. import app_instance


def initialize_database():
    with app_instance.app_context():
        db.create_all()
        db.session.commit()  # pylint: disable=no-member
        print("Database initialized")

    print("init finished")
