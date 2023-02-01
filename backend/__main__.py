#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from backend.constants import MODE


if __name__ == '__main__':
    FlaskApp().init_database()
    if MODE == "dev":
        FlaskApp().run_dev_server()
    else:
        FlaskApp().run_prod_server()
