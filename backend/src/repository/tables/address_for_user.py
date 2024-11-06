from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from src.models.dto.address_for_user import AddressForUserRequest, AddressForUserResult, AddressForUserDTO
from src.models.orm.address.addresses_for_user import AddressesForUser
from src.repository.tables.interface import TablesRepositoryInterface


class AddressForUserRepo(TablesRepositoryInterface):

    def __init__(self, model: AddressesForUser):
        self.model: AddressesForUser = model

    async def delete(
            self,
            session: AsyncSession,
            model: AddressForUserRequest
    ) -> AddressForUserResult:
        await session.scalars(
            delete(self.model.__tablename__)
            .where(self.model.user_id == model.user_id)
            .where(self.model.address_id == model.address_id)
        )
        return ...

    async def update(
            self,
            session: AsyncSession,
            model: AddressForUserRequest
    ) -> AddressForUserResult:
        await session.scalars(
            insert(self.model.__tablename__)
            .values(**model.dict())
        )
        return ...

    async def get(
            self,
            session: AsyncSession,
            model: AddressForUserRequest
    ) -> AddressForUserDTO:
        await session.scalars(
            select(self.model)
            .where(self.model.user_id == model.user_id)
            .where(self.model.address_id == model.address_id)
        )
        return ...
