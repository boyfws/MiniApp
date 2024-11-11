from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete

from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.models.orm.schemas import Address, City, District, Street


class AddressRepo:

    @staticmethod
    async def delete(
            session: AsyncSession,
            model: AddressRequest
    ) -> AddressResult:
        stmt = delete(Address).where(Address.id == model.id)
        await session.execute(stmt)
        return AddressResult(id=model.id)

    @staticmethod
    async def add_address(
            session: AsyncSession,
            model: AddressDTO
    ) -> AddressResult:
        city_stmt = insert(City).values(name=model.city).returning(City.id)
        city_id = await session.execute(city_stmt)

        district_stmt = insert(District).values(name=model.district).returning(District.id)
        district_id = await session.execute(district_stmt)

        street_stmt = insert(Street).values(name=model.street)
        street_id = await session.execute(street_stmt)

        address_stmt = insert(Address).values(
            city_id=city_id,
            district_id=district_id,
            street_id=street_id,
            house=model.house
        ).returning(Address.id)
        address_id = await session.execute(address_stmt)
        return AddressResult.model_validate(address_id.first(), from_attributes=True)