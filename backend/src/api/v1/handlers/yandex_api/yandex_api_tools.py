from typing import Optional, List

from .GeoSuggest import GeoSuggest, AddressPart
from .GeoCode import GeoCode, GeoJson
# from .translation import get_rus_city
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




#geocoder, geosuggest = None, None


async def prepare_classes_for_yandex_api():
    global geosuggest, geocoder
    geocoder = GeoCode(yandex_api_session.session)
    geosuggest = GeoSuggest(yandex_api_session.session)



@yandex_api_router.get(
    "/get_address_suggestion/",
    summary="Получить предложение адреса"
)
async def get_suggestions(
        text: str,
        lon: Optional[float] = None,
        lat: Optional[float] = None
) -> list[AddressPart]:
    """
    Принимает введенный пользователем частичный адрес, а также координаты.
    Возвращает подсказки пользователю при вводе адреса в виде списка частичных адресов.

    Пример ответа:
    ```
    {
        city: "Москва",
        region: "Москва",
        street: null,
        district: null,
        house: null
    }
    ```
    """
    return await geosuggest.get_similar_locations(
        text=text,
        number_of_suggestions=5,
        longitude=lon,
        latitude=lat
    )


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
    location1 = await geosuggest.get_similar_locations(
        text=formated_address1,
        number_of_suggestions=1,
        longitude=longitude,
        latitude=latitude
    )
    if len(location1) == 0:
        raise LocationNotFoundError("Не найдена походящая локация")

    ret_address_1 = await geocoder.get_coords_for_geosuggest_address(location1[0])

    if ret_address_1 is not None:
        return ret_address_1

    raise ValueError


# @yandex_api_router.get(
#     "/get_city_translation/{city}",
#     summary="Получить перевод названия города"
# )
# async def get_translation(city: str) -> Optional[GeoJson]:
#     """
#     Получить перевод названия города. Принимает в путь url название города на русском.
#     Возвращает GeoJson с переведенным адресом.
#
#     Пример ответа:
#     ```
#     {
#         "type": "Feature",
#         "geometry": {
#             "type": "Point",
#             "coordinates": [
#                 37.552687,
#                 55.777013
#             ]
#         },
#         "properties": {
#             "city": "Москва",
#             "region": null,
#             "street": null,
#             "district": null,
#             "house": null
#         }
#     }
#     ```
#     """
#     # translate to russian
#     translated = get_rus_city(city)
#     # use geocoder to get coordinates
#     return await geocoder.get_coords_for_geosuggest_address(
#         location=AddressPart(
#             full_name=translated,
#             city=translated,
#             region=None,
#             district=None,
#             street=None,
#             house=None
#         )
#     )

@yandex_api_router.get(
    "/get_geojson_from_address_recommendation/",
    summary="Получить GeoJson из адреса"
)
async def get_geojson_from_address_recommendation(
    full_name: str = Query(..., description="Полный адрес"),
    city: str = Query(None, description="Город"),
    region: Optional[str] = Query(None, description="Регион"),
    street: Optional[str] = Query(None, description="Улица"),
    district: Optional[str] = Query(None, description="Район"),
    house: Optional[str] = Query(None, description="Дом"),
) -> GeoJson:
    """
    Получить GeoJson из адреса. Принимает в параметры запроса все свойства адреса.
    Делает запрос в ГеоКодер Яндекса, после чего получает координаты адреса и преобразует в GeoJson.

    Пример ответа:
    ```
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                37.552687,
                55.777013
            ]
        },
        "properties": {
            "city": "Москва",
            "region": None,
            "street": "улица Поликарпова",
            "district": None,
            "house": "8"
        }
    }
    ```
    """
    address_data = AddressPart(
        full_name=full_name,
        city=city,
        region=region,
        street=street,
        district=district,
        house=house
    )
    return await geocoder.get_coords_for_geosuggest_address(location=address_data)

@yandex_api_router.get(
    "/get_address_from_coords/{lon}/{lat}",
    summary="Получить адрес из координат"
)
async def get_address_from_coords(
        lon: float,
        lat: float,
) -> GeoJson:
    """
    Получить адрес из координат. Принимает в путь url широту и долготу адреса.
    Вернет полный GeoJson адреса.

    Пример ответа:
    ```
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                37.552687,
                55.777013
            ]
        },
        "properties": {
            "city": "Москва",
            "region": None,
            "street": "улица Поликарпова",
            "district": None,
            "house": "8"
        }
    }
    ```
    """
    return await geocoder.get_address_for_coordinates(lon, lat)
