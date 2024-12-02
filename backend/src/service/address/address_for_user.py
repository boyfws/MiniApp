from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressForUserDTO, AddressesResponse, AllAddressesForUser
from src.repository.address.address_for_user import AddressForUserRepo


class AddressesForUserService:
    def __init__(self, session_getter=get_session) -> None:
        self.repo = AddressForUserRepo(session_getter)

    async def delete(self, model: AddressForUserDTO) -> AddressesResponse:
        return await self.repo.delete(model)

    async def create(self, model: AddressForUserDTO) -> AddressesResponse:
        return await self.repo.create(model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> list[AddressForUserDTO]:
        return await self.repo.get_all_user_addresses(model)

    async def drop_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> AddressesResponse:
        return await self.repo.drop_all_user_addresses(model)