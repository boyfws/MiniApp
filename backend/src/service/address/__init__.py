from src.repository.address.address import AddressRepo
from .address import AddressService
from .address_for_user import AddressesForUserService
from ...api.v1.handlers.yandex_api.GeoCode import GeoJson
from ...models.dto.address import AddressDTO


def get_address_service() -> AddressService:
    return AddressService(repo=AddressRepo())

def get_address_for_user_service() -> AddressesForUserService:
    return AddressesForUserService()

def transform_to_dto(model: GeoJson) -> AddressDTO:
    props = model.get("properties")
    coordinates = model.get("geometry").get("coordinates")
    location = f"SRID=4326;POINT({coordinates[0]} {coordinates[1]})"
    result = AddressDTO(
        location=location,
        region=props.get('region'),
        city=props.get('street'),
        district=props.get('district'),
        street=props.get('street'),
        house=props.get('house')
    )
    return result



__all__ = [
    "get_address_service", "AddressService",
    "get_address_for_user_service", "AddressesForUserService",
    "transform_to_dto"
]