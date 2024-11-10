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
        # result = await session.scalars(
        #     delete(Address)
        #     .where(Address.id == model.id)
        #     # .returning(Address.id)
        # )
        return AddressResult() #.model_validate(result, from_attributes=True)

    @staticmethod
    async def add_address(
            session: AsyncSession,
            model: AddressDTO
    ) -> AddressResult:
        # city_id = await session.scalars(
        #     insert(City)
        #     .values(**{"name": model.city})
        #     # .returning(City.id)
        # )
        # district_id = await session.scalars(
        #     insert(District)
        #     .values(**{"name": model.district})
        #     # .returning(District.id)
        # )
        # street_id = await session.scalars(
        #     insert(Street)
        #     .values(**{"name": model.street})
        # )
        # address_id = await session.scalars(
        #     insert(Address)
        #     .values(**{
        #         "city_id": city_id,
        #         "district_id": district_id,
        #         "street_id": street_id,
        #         "house": model.house,
        #         "location": model.location
        #     })
        #     # .returning(Address.id)
        # )
        return AddressResult() # AddressResult.model_validate(address_id, from_attributes=True)