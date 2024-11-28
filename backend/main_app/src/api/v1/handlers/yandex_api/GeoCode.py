import aiohttp
from typing import Dict, List, Optional, TypedDict
from src.config import configuration

from .GeoSuggest import AddressPart, AddressProperties


class Geometry(TypedDict):
    type: str
    coordinates: List[float]


class GeoJson(TypedDict):
    type: str
    geometry: Geometry
    properties: AddressProperties


class GeoCode:
    def __init__(self, session: aiohttp.ClientSession):
        self.session: aiohttp.ClientSession = session
        self.url: str = "https://geocode-maps.yandex.ru/1.x"
        self.def_params_for_get_coord_for_loc: Dict[str, int | str] = {
            "apikey": configuration.yandex_api.TOKEN_FOR_GEOCODER,
            "lang": "ru_RU",
            "rspn": 1,
            "format": "json",
            "bbox": "19.642090,41.185017~180.0,81.857361",
        }
        self.verif_dict_for_get_coord_for_loc: Dict[str, str] = {
                "locality": "city",
                "street": "street",
                "district": "district",
                "house": "house"
            }

    def _verification_for_get_coord_for_loc(self,
                                           formated_address_dict: dict,
                                           address_given: AddressPart) -> bool:
        """
        Проверяет найденный адрес на совпадение с переданным
        Возвращает True если адресы не  совпадают и False в противном случае
        """
        for el in formated_address_dict:
            obj_type = el["kind"]
            if obj_type in self.verif_dict_for_get_coord_for_loc:
                conv_key = self.verif_dict_for_get_coord_for_loc[obj_type]
                if address_given.get(conv_key, el["name"]) != el["name"]:
                    return True
        return False

    async def get_coords_for_geosuggest_address(self, location: AddressPart) -> GeoJson | None:
        params = self.def_params_for_get_coord_for_loc | {
            "geocode": location["full_name"],
            "results": 1
        }

        async with self.session.get(self.url, params=params) as response:
            if response.status != 200:
                return None

            responded_data = await response.json()

            try:
                responded_point_data = responded_data['response']["GeoObjectCollection"]["featureMember"][0]['GeoObject']
                responded_point_address = responded_point_data["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
            except KeyError:
                return None

            if self._verification_for_get_coord_for_loc(responded_point_address,
                                                     location):
                return None

            x, y = tuple(float(el) for el in responded_point_data["Point"]["pos"].split(" "))

            return {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [x, y]},
                "properties": {key: location[key] for key in location if key != "full_name"}
            }