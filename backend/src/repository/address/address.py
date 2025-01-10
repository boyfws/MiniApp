from sqlalchemy import insert, delete, select, text

from src.models.dto.address import AddressDTO, AddressRequest
from src.models.orm.schemas import Address
from src.repository import get_row
from src.repository.address import check_address_exists, get_point_str, get_coordinates, get_house_string, \
    _get_or_create_region, _get_or_create_city, _get_or_create_district, _get_or_create_street, _get_address_data, \
    _get_street_data, _get_district_data, _get_city_data, _get_region_data
from src.repository.interface import TablesRepositoryInterface


class AddressRepo(TablesRepositoryInterface):

    async def delete(
            self,
            model: AddressRequest
    ) -> None:
        async with self.session_getter() as session:
            stmt = delete(Address).where(Address.id == model.id)
            await session.execute(stmt)

    async def add_address(
            self,
            model: AddressDTO
    ) -> int:
        async with self.session_getter() as session:
            region_id = await _get_or_create_region(session, model.region)
            city_id = await _get_or_create_city(session, model.city, region_id)
            district_id = await _get_or_create_district(session, model.district, city_id)
            street_id = await _get_or_create_street(session, model.street, district_id)

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
                address_stmt = text(
                    f"SELECT id FROM address "
                    f"WHERE street_id = {street_id} AND "
                    f"{house_string}"
                    f"ST_Distance(location, ST_SetSRID(ST_MakePoint({coordinates[0]}, {coordinates[1]}), 4326)::geography) <= 0.05"
                )
                address_id = await get_row(session, address_stmt)

            return address_id
        
    async def get(self, address_id: int) -> AddressDTO:
        async with self.session_getter() as session:
            address_data = await _get_address_data(session, address_id)
            street_data = await _get_street_data(session, address_data.street_id)
            district_data = await _get_district_data(session, street_data.district_id)
            city_data = await _get_city_data(session, district_data.city_id)
            region_data = await _get_region_data(session, city_data.region_id)

            return AddressDTO(
                region=region_data.name,
                city=city_data.name,
                district=district_data.name,
                street=street_data.name,
                house=str(address_data.house),
                location=address_data.location
            )