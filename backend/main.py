from src.app import App
from src.config import configuration
from src.api.v1 import router_v1
from dataclasses import asdict

def main():
    return App(host='localhost', port=8000, **asdict(configuration.app)) \
        .included_cors() \
        .included_routers(routers=[router_v1])


if __name__ == '__main__':
    main()