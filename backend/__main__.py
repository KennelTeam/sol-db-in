#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import sys
from backend import app
from backend.constants import MODE
from backend.app.database.import_toponyms import import_toponyms

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--import_toponyms":
            import_toponyms()
            sys.exit()
        else:
            print(f"Unknown argument {sys.argv[1]}")
    if MODE == "dev":
        app.FlaskApp().run_dev_server()  # type: ignore
    else:
        app.FlaskApp().run_prod_server()  # type: ignore
