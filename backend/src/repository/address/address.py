from sqlalchemy import insert, delete, select, text

from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.models.orm.schemas import Address, City, District, Street, Region
from src.repository import get_item_from_stmt, get_row
from src.repository.address import check_address_exists, get_point_str, get_coordinates, get_house_string
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
            # найти айди региона, используя название
            region_search_stmt = select(Region.id).where(Region.name == model.region)
            region_stmt = insert(Region).values(name=model.region).returning(Region.id)
            region_id = await get_item_from_stmt(session, region_search_stmt, region_stmt)

            # найти айди города, используя название
            city_search_stmt = select(City.id).where(City.region_id == region_id).where(City.name == model.city)
            city_stmt = insert(City).values(name=model.city, region_id=region_id).returning(City.id)
            city_id = await get_item_from_stmt(session, city_search_stmt, city_stmt)

            # найти айди района, используя айди города и название
            district_search_stmt = select(District.id).where(District.city_id == city_id).where(
                District.name == model.district)
            district_stmt = insert(District).values(name=model.district, city_id=city_id).returning(District.id)
            district_id = await get_item_from_stmt(session, district_search_stmt, district_stmt)

            # найти айди улицы, используя район
            street_search_stmt = select(Street.id).where(Street.district_id == district_id).where(
                Street.name == model.street)
            street_stmt = insert(Street).values(name=model.street, district_id=district_id).returning(Street.id)
            street_id = await get_item_from_stmt(session, street_search_stmt, street_stmt)

            point_str = get_point_str(model.location)
            coordinates = get_coordinates(point_str)
            house_string = get_house_string(model.house)
            exist_flag = await check_address_exists(session, model.location, model.house, street_id)

            if not exist_flag:
                address_insert_stmt = insert(Address).values(
                        street_id=street_id,
                        house=model.house,
                        location=model.location
                    ).returning(Address.id)
                address_id = await get_row(session, address_insert_stmt)
            else:
                address_stmt = (
                    f"SELECT id FROM address "
                    f"WHERE street_id = {street_id} AND "
                    f"{house_string}"
                    f"ST_Distance(location, ST_SetSRID(ST_MakePoint({coordinates[0]}, {coordinates[1]}), 4326)::geography) <= 0.05"
                )
                address_id = await get_row(session, text(address_stmt))
            return AddressResult(id=address_id)
        
    async def get(self, address_id: int) -> AddressDTO:
        async with self.session_getter() as session:
            # address_stmt = select(Address.street_id, Address.house, Address.location).where(Address.id == address_id)
            address_stmt = f"SELECT street_id, house, ST_AsEWKT(location) AS location FROM address WHERE id = {address_id}::BIGINT"
            address_result = await session.execute(text(address_stmt))
            address_row = address_result.first()
            street_id, house, location = address_row.street_id, address_row.house, address_row.location
            
            # select street
            street_stmt = select(Street.name, Street.district_id).where(Street.id == street_id)
            street_result = await session.execute(street_stmt)
            street, district_id = street_result.first()
            
            # select district
            district_stmt = select(District.name, District.city_id).where(District.id == district_id)
            district_result = await session.execute(district_stmt)
            district, city_id = district_result.first()
            
            # select city
            city_stmt = select(City.name, City.region_id).where(City.id == city_id)
            city_result = await session.execute(city_stmt)
            city, region_id = city_result.first()
            
            # select region
            region_stmt = select(Region.name).where(Region.id == region_id)
            region_result = await session.execute(region_stmt)
            region = region_result.first()[0]
            
            return AddressDTO(
                region=region, 
                city=city, 
                district=district,
                street=street, 
                house=str(house),
                location=location
            )
