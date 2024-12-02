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

import os
import shutil

def remove_pycache(path):
    for root, _, files in os.walk(path):
        for item in files:
            if item == '__pycache__':
                full_path = os.path.join(root, item)
                try:
                    shutil.rmtree(full_path)  # Удаление папки и ее содержимого
                    print(f"Удалена папка: {full_path}")
                except OSError as e:
                    print(f"Ошибка при удалении папки {full_path}: {e}")


if __name__ == "__main__":
    project_path = "."  # Текущая директория
    remove_pycache(project_path)