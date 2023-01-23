#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.

import app
from cheroot.wsgi import Server, PathInfoDispatcher
import config_loader


def start_production_server():
    dispatcher = PathInfoDispatcher({'/': app.app})
    server = Server(('0.0.0.0', config_loader.get_config("PORT")), dispatcher,
                    numthreads=int(config_loader.get_config("NUM_THREADS")))
    try:
        print(f"the server is working at http://127.0.0.1:{config_loader.get_config('PORT')}")
        server.start()
    except KeyboardInterrupt:
        server.stop()


def start_development_server():
    app.app.run(host='0.0.0.0', port=config_loader.get_config("PORT"), debug=True)


if __name__ == '__main__':
    if config_loader.get_config("MODE") == "dev":
        start_development_server()
    else:
        start_production_server()
