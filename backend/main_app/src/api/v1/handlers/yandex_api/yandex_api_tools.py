from typing import Optional, List

from .GeoSuggest import GeoSuggest
from .GeoCode import GeoCode
from .yandex_api_session import yandex_api_session
from fastapi import APIRouter


yandex_api_router = APIRouter(
    prefix="/YandexApi",
    tags=["YandexApi"]
)


class LocationNotFoundError(ValueError):
    pass


NUM_of_SUGGESTIONS = 10

geocoder = GeoCode(yandex_api_session)
geosuggest = GeoSuggest(yandex_api_session)


@yandex_api_router.get("/get_rest_suggestion/")
async def get_suggestions(text: str, longitude: Optional[float] = None, latitude: Optional[float] = None):
    """
    Возвращает подсказки пользователю при вводе адреса
    """
    return await geosuggest.get_similar_locations(text=text,
                                                  number_of_suggestions=NUM_of_SUGGESTIONS,
                                                  longitude=longitude,
                                                  latitude=latitude)


#@yandex_api_router.get("/test/")
async def verificate_new_restaurant_address(
        city: str,
        street: str,
        house: str,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None):
    """
    Функция возвращает GeoJson для нового адреса нового ресторана
    """
    formated_address1 = f"Город {city}, {street}, дом {house}"
    location1 = await geosuggest.get_similar_locations(text=formated_address1,
                                                      number_of_suggestions=1,
                                                      longitude=longitude,
                                                      latitude=latitude)
    if len(location1) == 0:
        raise LocationNotFoundError("Не найдена походящая локация")

    ret_address_1 = await geocoder.get_coords_for_geosuggest_address(location1[0])

    if ret_address_1 is not None:
        return ret_address_1

    raise ValueError



