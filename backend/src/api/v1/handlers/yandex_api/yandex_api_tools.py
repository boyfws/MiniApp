from typing import Optional, List

from .GeoSuggest import GeoSuggest, AddressPart
from .GeoCode import GeoCode, GeoJson
from .translation import get_rus_city
from .yandex_api_session import yandex_api_session
from fastapi import APIRouter, Query

geosuggest: GeoSuggest
geocoder: GeoCode

yandex_api_router = APIRouter(
    prefix="/YandexApi",
    tags=["YandexApi"]
)


class LocationNotFoundError(ValueError):
    pass


NUM_of_SUGGESTIONS = 10


#geocoder, geosuggest = None, None


async def prepare_classes_for_yandex_api():
    global geosuggest, geocoder
    geocoder = GeoCode(yandex_api_session.session)
    geosuggest = GeoSuggest(yandex_api_session.session)



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


@yandex_api_router.get("/get_city_translation/{city}")
async def get_translation(city: str) -> GeoJson | None:
    # translate to russian
    translated = get_rus_city(city)
    # use geocoder to get coordinates
    return await geocoder.get_coords_for_geosuggest_address(
        location=AddressPart(
            full_name=translated,
            city=translated,
            region=None,
            district=None,
            street=None,
            house=None
        )
    )

@yandex_api_router.get("/get_geojson_from_address_recommendation/")
async def get_geojson_from_address_recommendation(
    full_name: str = Query(..., description="Полный адрес"),
    city: str = Query(None, description="Город"),
    region: Optional[str] = Query(None, description="Регион"),
    street: Optional[str] = Query(None, description="Улица"),
    district: Optional[str] = Query(None, description="Район"),
    house: Optional[str] = Query(None, description="Дом"),
) -> Optional[GeoJson]:
    address_data = AddressPart(
        full_name=full_name,
        city=city,
        region=region,
        street=street,
        district=district,
        house=house
    )
    return await geocoder.get_coords_for_geosuggest_address(location=address_data)