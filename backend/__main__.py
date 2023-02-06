#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend import app
from backend.constants import MODE


if __name__ == '__main__':
    if MODE == "dev":
        app.FlaskApp().run_dev_server()  # type: ignore
    else:
        app.FlaskApp().run_prod_server()  # type: ignore
