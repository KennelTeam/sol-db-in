#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend import app
from backend.app.database import initialize_database
from cheroot.wsgi import Server, PathInfoDispatcher
from backend.constants import NUM_THREADS, PORT, MODE


def start_production_server():
    dispatcher = PathInfoDispatcher({'/': app.app_instance})
    server = Server(('0.0.0.0', PORT), dispatcher, numthreads=NUM_THREADS)
    try:
        print(f"the server is working at http://127.0.0.1:{PORT}")
        server.start()
    except KeyboardInterrupt:
        server.stop()


def start_development_server() -> None:
    app.app_instance.run(host='0.0.0.0', port=PORT, debug=True)


if __name__ == '__main__':
    initialize_database.initialize_database()
    if MODE == "dev":
        start_development_server()
    else:
        start_production_server()
