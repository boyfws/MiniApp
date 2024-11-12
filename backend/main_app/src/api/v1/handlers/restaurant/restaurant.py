from fastapi import APIRouter, Depends

from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPoint, RestaurantRequestUsingGeoPointAndName
from src.service.restaurant import get_restaurant_service, RestaurantService

restaurant_router = APIRouter(
    prefix="/Restaurant",
    tags=["Restaurant"]
)

@restaurant_router.post("/create_restaurant/")
async def create_restaurant(
        model: RestaurantRequestFullModel,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantResult:
    return await service.create(model)

@restaurant_router.delete("/delete_restaurant/")
async def delete_restaurant(
        model: RestaurantRequestUsingID,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantResult:
    return await service.delete(model)

@restaurant_router.patch("/update_restaurant/")
async def update_restaurant(
        model: RestaurantRequestFullModel,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantResult:
    return await service.update(model)

@restaurant_router.get("/get_by_id/")
async def get_restaurant_by_id(
        model: RestaurantRequestUsingID,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantRequestFullModel:
    return await service.get(model)

@restaurant_router.get("/get_by_owner/")
async def get_restaurant_by_owner(
        model: RestaurantRequestUsingOwner,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantRequestFullModel]:
    return await service.get_by_owner(model)

@restaurant_router.get("/get_by_geo/")
async def get_restaurant_by_geo(
        model: RestaurantRequestUsingGeoPoint,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantRequestFullModel]:
    return await service.get_by_geo(model)

@restaurant_router.get("/get_by_geo_and_name/")
async def get_restaurant_by_geo_and_name(
        model: RestaurantRequestUsingGeoPointAndName,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantRequestFullModel]:
    return await service.get_by_geo_and_name(model)
