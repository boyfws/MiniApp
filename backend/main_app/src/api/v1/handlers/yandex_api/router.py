from fastapi import APIRouter


yandex_api_router = APIRouter(
    prefix="/YandexApi",
    tags=["YandexApi"]
)