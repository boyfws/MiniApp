from sqlalchemy import select, insert, delete

from src.database.sql_session import get_session
from src.models.dto.address_for_user import AddressesResponse, AddressForUserDTO, AllAddressesForUser
from src.models.orm.schemas import AddressesForUser


class AddressForUserRepo:

    async def delete(
            self,
            model: AddressForUserDTO
    ) -> AddressesResponse:
        async with get_session() as session:
            stmt = (
                delete(AddressesForUser)
                .where(AddressesForUser.user_id == model.user_id)
                .where(AddressesForUser.address_id == model.address_id)
            )
            await session.execute(stmt)
            return AddressesResponse()

    async def create(
            self,
            model: AddressForUserDTO,
    ) -> AddressesResponse:
        async with get_session() as session:
            stmt = insert(AddressesForUser).values(**model.dict())
            await session.execute(stmt)
            return AddressesResponse()

    async def get_all_user_addresses(
            self,
            model: AllAddressesForUser
    ) -> list[AddressesResponse]:
        async with get_session() as session:
            stmt = select(AddressesForUser.address_id).where(AddressesForUser.user_id == model.user_id)
            addresses = await session.execute(stmt)
            return [
                AddressesResponse.model_validate(address, from_attributes=True) for address in addresses.all()
            ]

    async def drop_all_user_addresses(
            self,
            model: AllAddressesForUser
    ) -> AddressesResponse:
        async with get_session() as session:
            stmt = delete(AddressesResponse).where(AddressesForUser.user_id == model.user_id)
            await session.execute(stmt)
            return AddressesResponse()
