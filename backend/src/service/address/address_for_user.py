from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressForUserDTO, AddressesResponse, AllAddressesForUser
from src.repository.address.address_for_user import AddressForUserRepo
from src.repository.address.address import AddressRepo
from src.models.dto.address import AddressDTO


class AddressesForUserService:
    def __init__(self, session_getter=get_session) -> None:
        self.address_repo = AddressRepo(session_getter)
        self.repo = AddressForUserRepo(session_getter)

    async def delete(self, model: AddressForUserDTO) -> AddressesResponse:
        return await self.repo.delete(model)

    async def create(self, model: AddressForUserDTO) -> AddressesResponse:
        return await self.repo.create(model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> list[AddressDTO]:
        addresses = await self.repo.get_all_user_addresses(model)
        addresses_geo = []
        # теперь надо для каждого адреса сделать запрос и получить пропертис
        for address in addresses:
            addresses_geo.append(self.address_repo.get(address.address_id))
            
        return addresses_geo

    async def drop_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> AddressesResponse:
        return await self.repo.drop_all_user_addresses(model)