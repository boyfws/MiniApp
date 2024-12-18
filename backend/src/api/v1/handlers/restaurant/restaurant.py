from fastapi import APIRouter, Depends

from src.models.dto.restaurant import RestaurantRequestFullModel, RestaurantResult, RestaurantRequestUsingID, \
    RestaurantRequestUsingOwner, RestaurantRequestUsingGeoPointAndName, Point, \
    RestaurantGeoSearch
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

@restaurant_router.delete("/delete_restaurant/{rest_id}")
async def delete_restaurant(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantResult:
    return await service.delete(RestaurantRequestUsingID(rest_id=rest_id))

@restaurant_router.patch("/update_restaurant/{rest_id}")
async def update_restaurant(
        rest_id: int,
        model: RestaurantRequestFullModel,
        service: RestaurantService = Depends(get_restaurant_service)
) -> None:
    await service.update(rest_id, model)

@restaurant_router.get("/get_by_id/{rest_id}")
async def get_restaurant_by_id(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> RestaurantRequestFullModel:
    return await service.get(RestaurantRequestUsingID(rest_id=rest_id))

@restaurant_router.get("/get_by_owner/{owner_id}")
async def get_restaurant_by_owner(
        owner_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantRequestFullModel]:
    return await service.get_by_owner(RestaurantRequestUsingOwner(owner_id=owner_id))

@restaurant_router.get("/get_by_geo/{lon}/{lat}/{user_id}")
async def get_restaurant_by_geo(
        lon: float,
        lat: float,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantGeoSearch]:
    return await service.get_by_geo(Point(lon=lon, lat=lat))

@restaurant_router.get("/get_by_geo_and_name/{lon}/{lat}/{name_pattern}/{user_id}")
async def get_restaurant_by_geo_and_name(
        lon: float,
        lat: float,
        name_pattern: str,
        user_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> list[RestaurantGeoSearch]:
    return await service.get_by_geo_and_name(RestaurantRequestUsingGeoPointAndName(point=Point(lon=lon, lat=lat), name_pattern=name_pattern))

@restaurant_router.get("/get_restaurant_name_by_id/{rest_id}")
async def get_restaurant_name_by_id(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> str:
    return await service.get_name(rest_id)

@restaurant_router.get("/get_restaurant_available_properties/{rest_id}")
async def get_restaurant_available_properties(
        rest_id: int,
        service: RestaurantService = Depends(get_restaurant_service)
) -> dict[str, bool]:
    return await service.get_available_properties(rest_id)

@restaurant_router.patch("/change_restaurant_property/{rest_id}/{key}/{value}")
async def change_restaurant_property(
        rest_id: int,
        key: str,
        value: str,
        service: RestaurantService = Depends(get_restaurant_service)
) -> None:
    await service.change_restaurant_property(rest_id, key, value)