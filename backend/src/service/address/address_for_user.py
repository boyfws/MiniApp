from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressForUserDTO, AllAddressesForUser, \
    DeleteAddressForUser
from src.repository.address.address_for_user import AddressForUserRepo
from src.repository.address.address import AddressRepo
from src.models.dto.address import AddressDTO


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

    async def get_all_user_addresses(
            self,
            model: AllAddressesForUser
    ) -> list[AddressDTO]:
        addresses = await self.repo.get_all_user_addresses(model)
        addresses_geo = []
        # теперь надо для каждого адреса сделать запрос и получить пропертис
        for address in addresses:
            addresses_geo.append(await self.address_repo.get(address.address_id))
        return addresses_geo

    async def drop_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> None:
        await self.repo.drop_all_user_addresses(model)

    @staticmethod
    def _extract_address(model: DeleteAddressForUser) -> AddressDTO:
        address = model.model_dump()
        del address['user_id']
        return AddressDTO.model_validate(address, from_attributes=True)