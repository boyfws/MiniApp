from typing import no_type_check, Optional

from sqlalchemy import insert, delete, select, Row
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def add_address(
            self,
            model: AddressDTO
    ) -> AddressResult:
        async with self.session_getter() as session:

            # найти айди города, используя название
            city_search_stmt = select(City.id).where(City.name == model.city)
            city_search_result = await session.execute(city_search_stmt)
            city_search_row: Optional[Row[tuple[int]]] = city_search_result.first()
            if not city_search_row: # если города нет в базе, то добавим
                city_stmt = insert(City).values(name=model.city).returning(City.id)
                city_result = await session.execute(city_stmt)
                city_row: Optional[Row[tuple[int]]] = city_result.first()
                if city_row is None: raise ValueError("No city ID returned from the database")
                city_id = int(city_row[0])
            else:
                city_id = int(city_search_row[0])

            # найти айди района, используя айди города и название
            district_search_stmt = select(District.id).where(District.city_id == city_id).where(District.name == model.district)
            district_search_result = await session.execute(district_search_stmt)
            district_search_row: Optional[Row[tuple[int]]] = district_search_result.first()
            if not district_search_row: # если района данного города нет, то добавим
                district_stmt = insert(District).values(name=model.district, city_id=city_id).returning(District.id)
                district_result = await session.execute(district_stmt)
                district_row: Optional[Row[tuple[int]]] = district_result.first()
                if district_row is None: raise ValueError("No district ID returned from the database")
                district_id = int(district_row[0])
            else:
                district_id = int(district_search_row[0])

            # найти айди улицы, зная район
            street_search_stmt = select(Street.id).where(Street.district_id == district_id).where(Street.name == model.street)
            street_search_result = await session.execute(street_search_stmt)
            street_search_row = street_search_result.first()
            if not street_search_row:
                street_stmt = insert(Street).values(name=model.street, district_id=district_id).returning(Street.id)
                street_result = await session.execute(street_stmt)
                street_row: Optional[Row[tuple[int]]] = street_result.first()
                if street_row is None:
                    raise ValueError("No street ID returned from the database")
                street_id = int(street_row[0])
            else: street_id = street_search_row.id

            address_stmt = insert(Address).values(
                street_id=street_id,
                house=model.house,
                location=model.location
            ).returning(Address.id)
            address_id_result = await session.execute(address_stmt)
            address_row: Optional[Row[tuple[int]]] = address_id_result.first()
            if not address_row: raise ValueError("No address id returned from the database")
            address_id = int(address_row[0])
            return AddressResult(id=address_id)