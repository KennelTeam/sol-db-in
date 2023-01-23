import app
from cheroot.wsgi import Server, PathInfoDispatcher
import config_loader


if __name__ == '__main__':
    dispatcher = PathInfoDispatcher({'/': app.app})
    server = Server(('0.0.0.0', config_loader.get_config("PORT")), dispatcher,
                    numthreads=int(config_loader.get_config("NUM_THREADS")))
    try:
        print(f"the server is working at http://127.0.0.1:{config_loader.get_config('PORT')}")
        server.start()
    except KeyboardInterrupt:
        server.stop()
