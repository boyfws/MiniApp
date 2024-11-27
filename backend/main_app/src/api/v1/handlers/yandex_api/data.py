import aiohttp
from fastapi import HTTPException
from typing import Dict, Optional, List, no_type_check
from typing_extensions import TypedDict
from src.config import configuration

from fastapi import APIRouter

yandex_api_router = APIRouter(
    prefix="/YandexApi",
    tags=["YandexApi"]
)

# Определение типа для геометрии
class Geometry(TypedDict):
    type: str
    coordinates: List[float]


# Определение типа для свойств
class Properties(TypedDict):
    street: Optional[str]
    house: Optional[str]
    district: Optional[str]
    city: str


# Определение типа для GeoJson
class GeoJson(TypedDict):
    type: str
    geometry: Geometry
    properties: Properties


class AddressPart(TypedDict):
    full_name: str
    city: Optional[str]
    street: Optional[str]
    district: Optional[str]
    house: Optional[str]


class CoordinatesError(ValueError):
    pass


class LocationNotFoundError(ValueError):
    pass


@no_type_check
@yandex_api_router.get("/get_similar_locations/", response_model=List[AddressPart])
async def get_similar_locations(
        text: str,
        number_of_suggestions: int,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
) -> List[AddressPart]:
    url = "https://suggest-maps.yandex.ru/v1/suggest"
    params: Dict[str, int | Optional[str]] = {
        "apikey": configuration.yandex_api.TOKEN_FOR_GEOSUGGEST,
        "text": text,
        "lang": "ru",
        "bbox": "19.6390,41.1886,180.0,81.8574",
        "strict_bounds": 1,
        "results": number_of_suggestions,
        "highlight": 0,
        "print_address": 1,
        "types": "house,street,district,locality",
    }
    if longitude is not None and latitude is not None:
        params["ull"] = f"{longitude},{longitude}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=response.text())

            data = await response.json()

            if "results" not in data:
                return []

            convertion_dict: Dict[str, str] = {
                "LOCALITY": "city",
                "STREET": "street",
                "DISTRICT": "district",
                "HOUSE": "house"
            }

            return [
                {"full_name": el["address"]["formatted_address"]} |
                {convertion_dict[el2["kind"][0]]: el2["name"] for el2 in el["address"]["component"][::-1] if
                # Разворачиваем список компонентов,
                # так как могут вернуться два компонента с одинаковым kind тот, что выше - более приортетеный по name
                 el2["kind"][0] in convertion_dict}
                for el in data["results"]
            ]


# noinspection PyTypedDict
@no_type_check
@yandex_api_router.get("/get_coords_for_ceratin_location/")
async def get_coords_for_ceratin_location(location: AddressPart) -> GeoJson:
    url: str = "https://geocode-maps.yandex.ru/1.x"
    params: Dict[str, int | Optional[str]] = {"apikey": configuration.yandex_api.TOKEN_FOR_GEOCODER,
                                    "lang": "ru_RU",
                                    "rspn": 1,
                                    "format": "json",
                                    "bbox": "19.642090,41.185017~180.0,81.857361",
                                    "results": 1,
                                    "geocode": location["full_name"]}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            responded_data = await response.json()
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="something went wrong")

            responded_point_data = responded_data['response']["GeoObjectCollection"]["featureMember"][0]['GeoObject']
            responded_point_adress = responded_point_data["metaDataProperty"]["GeocoderMetaData"]["Address"][
                "Components"]

            convertion_dict: Dict[str, str] = {
                "locality": "city",
                "street": "street",
                "district": "district",
                "house": "house"
            }
            for el in responded_point_adress:
                if el["kind"] in convertion_dict:
                    conv_key = convertion_dict[el["kind"]]
                    if conv_key in location and location[conv_key] != el["name"]:
                        raise CoordinatesError(f"Api не нашел подходящего адреса")

            x, y = tuple(float(el) for el in responded_point_data["Point"]["pos"].split(" "))

            return {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [x, y]},
                "properties": {key: location[key] for key in location if key != "full_name"}
            }


#@main_app.get("blabla")
@no_type_check
async def get_suggestions(text: str, longitude: Optional[float] = None, latitude: Optional[float] = None) -> List[AddressPart]:
    """
    Возвращает подсказки пользоавтелю при вводе адреса
    """
    try:
        return await get_similar_locations(text, 3, longitude, latitude)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


### !!! Catch-и будем прописывать на более высоком уровне
# Данная функция будет использоваться при верификации новго реста
@no_type_check
@yandex_api_router.get('/verificte_new_restaurant_adress/')
async def verificte_new_restaurant_adress(
        city: str,
        street: str, house: str,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None) -> GeoJson:
    """
    Функция возвращет GeoJson для нового адреса нвого ресторана
    """
    formated_address = f"Город {city}, {street}, дом {house}"
    arg = await get_similar_locations(formated_address, 1, longitude, latitude)

    if len(arg) == 0:
        raise LocationNotFoundError("Не найдена походящая локация")

    return await get_coords_for_ceratin_location(arg[0])


