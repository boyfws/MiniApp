import aiohttp
from typing import Optional, Dict, TypedDict, List
from src.config import configuration


class AddressProperties(TypedDict):
    city: str
    region: Optional[str]
    street: Optional[str]
    district: Optional[str]
    house: Optional[str]


class AddressPart(AddressProperties):
    full_name: str



class GeoSuggest:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session: aiohttp.ClientSession = session
        self.url: str = "https://suggest-maps.yandex.ru/v1/suggest"
        self.def_params_for_sim_loc:  Dict[str, int | str] = {
            "apikey": configuration.yandex_api.TOKEN_FOR_GEOSUGGEST,
            "lang": "ru",
            "bbox": "19.6390,41.1886,180.0,81.8574",
            "strict_bounds": 1,
            "highlight": 0,
            "print_address": 1,
            "types": "house,street,district,province,locality",
        }
        self.conv_dict_for_sim_loc: Dict[str, str] = {
            "LOCALITY": "city",
            "STREET": "street",
            "DISTRICT": "district",
            "HOUSE": "house",
            "PROVINCE": "region"
        }

    async def get_similar_locations(self,
                                    text: str,
                                    number_of_suggestions: int,
                                    longitude: Optional[float] = None,
                                    latitude: Optional[float] = None) -> List[AddressPart]:
        params = self.def_params_for_sim_loc | {
            "text": text,
            "results": number_of_suggestions,
        }
        if longitude is not None and latitude is not None:
            params["ull"] = f"{longitude},{longitude}"

        async with self.session.get(self.url, params=params) as response:
            if response.status != 200:
                return []

        data = await response.json()

        if "results" not in data:
            return []
        try:
            return [
                {
                    "full_name": el["address"]["formatted_address"]
                } |
                {
                    self.conv_dict_for_sim_loc[el2["kind"][0]]: el2["name"]
                    for el2 in el["address"]["component"][::-1]
                    # Разворачиваем список компонентов,
                    # так как могут вернуться два компонента с одинаковым kind тот,
                    # что выше - более приоритетный по name
                    if el2["kind"][0] in self.conv_dict_for_sim_loc
                }
                for el in data["results"]
            ]
        except KeyError:
            return []
