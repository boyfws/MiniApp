from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressForUserDTO, AddressesResponse, AllAddressesForUser
from src.repository.address.address_for_user import AddressForUserRepo


class AddressesForUserService:
    def __init__(self) -> None:
        self.repo = AddressForUserRepo()

    async def delete(self, model: AddressForUserDTO) -> AddressesResponse:
        async with get_session() as session:
            return await self.repo.delete(session, model)

    async def create(self, model: AddressForUserDTO) -> AddressesResponse:
        async with get_session() as session:
            return await self.repo.create(session, model)

    async def get_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> list[AddressesResponse]:
        async with get_session() as session:
            return await self.repo.get_all_user_addresses(session, model)

    async def drop_all_user_fav_restaurants(
            self,
            model: AllAddressesForUser
    ) -> AddressesResponse:
        async with get_session() as session:
            return await self.repo.drop_all_user_addresses(session, model)