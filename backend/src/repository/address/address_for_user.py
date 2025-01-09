from sqlalchemy import select, insert, delete, text
from src.models.dto.address_for_user import AddressesResponse, AddressForUserDTO, AllAddressesForUser
from src.models.orm.schemas import AddressesForUser
from src.repository.interface import TablesRepositoryInterface
from src.repository.user import UserRepo


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
            user_id: int,
            address_id: int
    ) -> AddressesResponse:
        async with self.session_getter() as session:

            # если юзера раньше не было в базе, то добавим
            user_repo = UserRepo(session_getter=self.session_getter)
            is_user = await user_repo.is_user(user_id)
            if not is_user:
                await user_repo.create_user(user_id)

            address_exists = await session.execute(
                select(AddressesForUser)
                .where(AddressesForUser.user_id == user_id)
                .where(AddressesForUser.address_id == address_id)
            )
            address_exists_result = address_exists.scalar_one_or_none()

            if not address_exists_result:
                stmt = insert(AddressesForUser).values(user_id=user_id, address_id=address_id)
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
