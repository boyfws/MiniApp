from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.v1.handlers.yandex_api import close_yandex_api_session


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await close_yandex_api_session()
