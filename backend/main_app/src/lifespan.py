from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.v1.handlers.yandex_api import (close_yandex_api_session,
                                            open_yandex_api_session,
                                            prepare_classes_for_yandex_api)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_yandex_api_session()
    await prepare_classes_for_yandex_api()
    yield
    await close_yandex_api_session()
