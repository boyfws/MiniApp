from typing import Any

from src.app.app import App
from src.config import configuration
from src.api.v1 import router_v1
from dataclasses import asdict
from src.lifespan import lifespan


def main() -> Any:
    app: Any = App(host='localhost',
                   port=8000,
                   lifespan=lifespan,
                   **asdict(configuration.app)
                   ).included_cors().included_routers(routers=[router_v1])
    return app