from sqlalchemy import select, insert, delete

from src.models.dto.address_for_user import AddressForUserDTO
from src.models.orm.schemas import AddressesForUser
from src.repository.interface import TablesRepositoryInterface


class AddressForUserRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: AddressForUserDTO
    ) -> None:
        async with self.session_getter() as session:
            stmt = (
                delete(AddressesForUser)
                .where(AddressesForUser.user_id == model.user_id)
                .where(AddressesForUser.address_id == model.address_id)
            )
            await session.execute(stmt)

    async def create(
            self,
            user_id: int,
            address_id: int
    ) -> None:
        async with self.session_getter() as session:

            address_exists = await session.execute(
                select(AddressesForUser)
                .where(AddressesForUser.user_id == user_id)
                .where(AddressesForUser.address_id == address_id)
            )
            address_exists_result = address_exists.scalar_one_or_none()

            if not address_exists_result:
                stmt = insert(AddressesForUser).values(user_id=user_id, address_id=address_id)
                await session.execute(stmt)


    async def get_all_user_addresses(
            self,
            user_id: int
    ) -> list[AddressForUserDTO]:
        async with self.session_getter() as session:
            stmt = select(AddressesForUser.user_id, AddressesForUser.address_id).where(AddressesForUser.user_id == user_id)
            addresses = await session.execute(stmt)
            return [
                AddressForUserDTO.model_validate(address, from_attributes=True) for address in addresses.all()
            ]

    async def drop_all_user_addresses(
            self,
            user_id: int
    ) -> None:
        async with self.session_getter() as session:
            stmt = delete(AddressesForUser).where(AddressesForUser.user_id == user_id)
            await session.execute(stmt)
