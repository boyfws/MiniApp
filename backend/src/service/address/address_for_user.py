from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressForUserDTO, DeleteAddressForUser
from src.repository.address import get_point_str, get_coordinates
from src.repository.address.address_for_user import AddressForUserRepo
from src.repository.address.address import AddressRepo
from src.models.dto.address import AddressDTO, GeoJson


class AddressesForUserService:
    def __init__(self, session_getter=get_session) -> None:
        self.address_repo = AddressRepo(session_getter)
        self.repo = AddressForUserRepo(session_getter)

    async def delete(self, model: DeleteAddressForUser) -> None:
        address_id = await self.address_repo.add_address(self._extract_address(model))
        await self.repo.delete(AddressForUserDTO(address_id=address_id, user_id=model.user_id))

    async def create(self, user_id: int, model: AddressDTO) -> None:
        address_id = await self.address_repo.add_address(model)
        await self.repo.create(user_id, address_id)

    async def get_all_user_addresses(self, user_id: int) -> list[GeoJson]:
        addresses = await self.repo.get_all_user_addresses(user_id)
        return await self._transform_addresses(addresses)

    async def drop_all_user_fav_restaurants(self, user_id: int) -> None:
        await self.repo.drop_all_user_addresses(user_id)

    @staticmethod
    def _extract_address(model: DeleteAddressForUser) -> AddressDTO:
        address = model.model_dump()
        del address['user_id']
        return AddressDTO.model_validate(address, from_attributes=True)

    async def _get_addresses_dto(self, addresses: list[AddressForUserDTO]) -> list[AddressDTO]:
        return [await self.address_repo.get(address.address_id) for address in addresses]

    @staticmethod
    def _make_geojson(coordinates, properties) -> GeoJson:
        return GeoJson.model_validate({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            },
            "properties": properties
        })

    def _get_geojson(self, address: AddressDTO) -> GeoJson:
        point_str = get_point_str(address.location)
        coordinates = get_coordinates(point_str)
        properties = {
            key: value for key, value in address.model_dump().items() if key != "location"
        }
        return self._make_geojson(coordinates, properties)

    async def _transform_addresses(self, addresses: list[AddressForUserDTO]) -> list[GeoJson]:
        addresses = await self._get_addresses_dto(addresses)
        return [self._get_geojson(address) for address in addresses]
