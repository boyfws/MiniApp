from fastapi import APIRouter

from src.api.v1.handlers.category.category import category_router
from src.api.v1.handlers.category.favourite import fav_category_router
from src.api.v1.handlers.restaurant.favourite import fav_restaurant_router
from src.api.v1.handlers.yandex_api import yandex_api_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(yandex_api_router)
router_v1.include_router(category_router)
router_v1.include_router(fav_category_router)
router_v1.include_router(fav_restaurant_router)