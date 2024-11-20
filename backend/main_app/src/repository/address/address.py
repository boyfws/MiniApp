from typing import no_type_check

from sqlalchemy import insert, delete
from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.models.orm.schemas import Address, City, District, Street
from src.repository.interface import TablesRepositoryInterface


class AddressRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: AddressRequest
    ) -> AddressResult:
        async with self.session_getter() as session:
            stmt = delete(Address).where(Address.id == model.id)
            await session.execute(stmt)
            return AddressResult(id=model.id)

    @no_type_check
    async def add_address(
            self,
            model: AddressDTO
    ) -> AddressResult:
        async with self.session_getter() as session:
            city_stmt = insert(City).values(name=model.city).returning(City.id)
            city_id_row = await session.execute(city_stmt)
            city_id = int(city_id_row.first()[0])

            district_stmt = insert(District).values(name=model.district, city_id=city_id).returning(District.id)
            district_id_row = await session.execute(district_stmt)
            district_id = int(district_id_row.first()[0])

            street_stmt = insert(Street).values(name=model.street, district_id=district_id).returning(Street.id)
            street_id_row = await session.execute(street_stmt)
            street_id = int(street_id_row.first()[0])

            address_stmt = insert(Address).values(
                street_id=street_id,
                house=model.house,
                location=model.location
            ).returning(Address.id)
            address_id_row = await session.execute(address_stmt)
            address_id = int(address_id_row.first()[0])
            print("скрипт завершил работу")
            return AddressResult(id=address_id)