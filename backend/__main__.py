#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend import app
from backend.app.database import initialize_database
from cheroot.wsgi import Server, PathInfoDispatcher  # type: ignore[import]
from backend.config_loader import ConfigLoader


def start_production_server():
    dispatcher = PathInfoDispatcher({'/': app.app})
    server = Server(('0.0.0.0', ConfigLoader.get_config("PORT")), dispatcher,
                    numthreads=int(ConfigLoader.get_config("NUM_THREADS")))
    try:
        print(f"the server is working at http://127.0.0.1:{ConfigLoader.get_config('PORT')}")
        server.start()
    except KeyboardInterrupt:
        server.stop()


def start_development_server() -> None:
    app.app.run(host='0.0.0.0', port=ConfigLoader.get_config("PORT"), debug=True)


if __name__ == '__main__':
    initialize_database.initialize_database()
    if ConfigLoader.get_config("MODE") == "dev":
        start_development_server()
    else:
        start_production_server()
