from fastapi import APIRouter

from src.api.v1.handlers.yandex_api import yandex_api_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(yandex_api_router)