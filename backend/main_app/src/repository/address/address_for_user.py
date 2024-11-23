from sqlalchemy import select, insert, delete
from src.models.dto.address_for_user import AddressesResponse, AddressForUserDTO, AllAddressesForUser
from src.models.orm.schemas import AddressesForUser
from src.repository.interface import TablesRepositoryInterface


class AddressForUserRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: AddressForUserDTO
    ) -> AddressesResponse:
        async with self.session_getter() as session:
            stmt = (
                delete(AddressesForUser)
                .where(AddressesForUser.user_id == model.user_id)
                .where(AddressesForUser.address_id == model.address_id)
            )
            await session.execute(stmt)
            return AddressesResponse(status=200)

    async def create(
            self,
            model: AddressForUserDTO,
    ) -> AddressesResponse:
        async with self.session_getter() as session:
            stmt = insert(AddressesForUser).values(**model.dict())
            await session.execute(stmt)
            return AddressesResponse(status=200)

    async def get_all_user_addresses(
            self,
            model: AllAddressesForUser
    ) -> list[AddressForUserDTO]:
        async with self.session_getter() as session:
            stmt = select(AddressesForUser.user_id, AddressesForUser.address_id).where(AddressesForUser.user_id == model.user_id)
            addresses = await session.execute(stmt)
            return [
                AddressForUserDTO.model_validate(address, from_attributes=True) for address in addresses.all()
            ]

    async def drop_all_user_addresses(
            self,
            model: AllAddressesForUser
    ) -> AddressesResponse:
        async with self.session_getter() as session:
            stmt = delete(AddressesForUser).where(AddressesForUser.user_id == model.user_id)
            await session.execute(stmt)
            return AddressesResponse(status=200)
