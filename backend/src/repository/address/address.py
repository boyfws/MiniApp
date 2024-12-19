from typing import no_type_check, Optional

from sqlalchemy import insert, delete, select, Row, text, exists

from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.models.orm.schemas import Address, City, District, Street, Region
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
            # TODO: сделать здесь код более чистым
            # найти айди региона, используя название
            region_search_stmt = select(Region.id).where(Region.name == model.region)
            region_search_result = await session.execute(region_search_stmt)
            region_search_row: Optional[Row[tuple[int]]] = region_search_result.first()
            if not region_search_row:
                region_stmt = insert(Region).values(name=model.region).returning(Region.id)
                region_result = await session.execute(region_stmt)
                region_row: Optional[Row[tuple[int]]] = region_result.first()
                if region_row is None: raise ValueError("No region ID returned from the database")
                region_id = int(region_row[0])
            else:
                region_id = int(region_search_row[0])

            # найти айди города, используя название
            city_search_stmt = select(City.id).where(City.name == model.city).where(City.region_id == region_id)
            city_search_result = await session.execute(city_search_stmt)
            city_search_row: Optional[Row[tuple[int]]] = city_search_result.first()
            if not city_search_row:  # если города нет в базе, то добавим
                city_stmt = insert(City).values(name=model.city, region_id=region_id).returning(City.id)
                city_result = await session.execute(city_stmt)
                city_row: Optional[Row[tuple[int]]] = city_result.first()
                if city_row is None: raise ValueError("No city ID returned from the database")
                city_id = int(city_row[0])
            else:
                city_id = int(city_search_row[0])

            # найти айди района, используя айди города и название
            district_search_stmt = select(District.id).where(District.city_id == city_id).where(
                District.name == model.district)
            district_search_result = await session.execute(district_search_stmt)
            district_search_row: Optional[Row[tuple[int]]] = district_search_result.first()
            if not district_search_row:  # если района данного города нет, то добавим
                district_stmt = insert(District).values(name=model.district, city_id=city_id).returning(District.id)
                district_result = await session.execute(district_stmt)
                district_row: Optional[Row[tuple[int]]] = district_result.first()
                if district_row is None: raise ValueError("No district ID returned from the database")
                district_id = int(district_row[0])
            else:
                district_id = int(district_search_row[0])

            # найти айди улицы, зная район
            street_search_stmt = select(Street.id).where(Street.district_id == district_id).where(
                Street.name == model.street)
            street_search_result = await session.execute(street_search_stmt)
            street_search_row = street_search_result.first()
            if not street_search_row:
                street_stmt = insert(Street).values(name=model.street, district_id=district_id).returning(Street.id)
                street_result = await session.execute(street_stmt)
                street_row: Optional[Row[tuple[int]]] = street_result.first()
                if street_row is None:
                    raise ValueError("No street ID returned from the database")
                street_id = int(street_row[0])
            else:
                street_id = street_search_row.id

            # проверка, что такой адрес существует
            address_exists = session.query(exists().where(
                Address.street_id == street_id,
                Address.house == model.house,
                Address.location == model.location
            )).scalar()

            if not address_exists:
                result = session.execute(
                    insert(Address).values(
                        street_id=street_id,
                        house=model.house,
                        location=model.location
                    ).returning(Address.id)
                )
                address_id = result.scalar()
            else:
                address_id = session.execute(
                    select(Address.id).where(Address.street_id == street_id).where(Address.house == model.house).where(
                        Address.location == model.location)
                )
            return AddressResult(id=address_id)
        
    async def get(self, address_id: int) -> AddressDTO:
        async with self.session_getter() as session:
            # address_stmt = select(Address.street_id, Address.house, Address.location).where(Address.id == address_id)
            address_stmt = f"SELECT street_id, house, ST_AsEWKT(location) AS location FROM address WHERE id == {address_id}"
            address_result = await session.execute(text(address_stmt))
            street_id, house, location = address_result.first()[0]
            
            # select street
            street_stmt = select(Street.name, Street.district_id).where(Street.id == street_id)
            street_result = await session.execute(street_stmt)
            street, district_id = street_result.first()[0]
            
            # select district
            district_stmt = select(District.name, District.city_id).where(District.id == district_id)
            district_result = await session.execute(district_stmt)
            district, city_id = district_result.first()[0]
            
            # select city
            city_stmt = select(City.name, City.region_id).where(City.id == city_id)
            city_result = await session.execute(city_stmt)
            city, region_id = city_result.first()[0]
            
            # select region
            region_stmt = select(Region.name).where(Region.id == region_id)
            region_result = await session.execute(region_stmt)
            region = region_result.first()[0]
            
            return AddressDTO(
                region=region, 
                city=city, 
                district=district,
                street=street, 
                house=house, 
                location=location
            )