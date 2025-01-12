from typing import Optional

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint
from sqlalchemy import insert, select, text, cast, func, Select, Insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.dto.address import AddressDTO
from src.models.orm.schemas import Address
from src.repository import get_row
from src.repository.address import get_point_str, get_coordinates, \
    _get_or_create_region, _get_or_create_city, _get_or_create_district, _get_or_create_street, _get_address_data, \
    _get_street_data, _get_district_data, _get_city_data, _get_region_data
from src.repository.interface import TablesRepositoryInterface


class AddressRepo(TablesRepositoryInterface):

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
            lon, lat = get_coordinates(point_str)

            address_id = await self._get_address_id(session, street_id, model.house, lon, lat)

            if not address_id:
                return await get_row(
                    session,
                    self._get_insert_address_stmt(street_id, model.house, model.location)
                )
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

    @staticmethod
    def _get_address_stmt(street_id: int, house: str, lon: float, lat: float) -> Select:
        point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        distance = func.ST_Distance(Address.location, cast(point, Geography)).label("distance")
        stmt = (
            select(Address.id)
            .where(Address.street_id == street_id)
            .where(distance <= 0.05)
        )
        if house:
            stmt = stmt.where(Address.house == house)
        return stmt

    @staticmethod
    def _get_insert_address_stmt(street_id: int, house: str, location: str) -> Insert:
        return insert(Address).values(
            street_id=street_id,
            house=house,
            location=location
        ).returning(Address.id)

    async def _get_address_id(
            self,
            session: AsyncSession,
            street_id: int, house: str, lon: float, lat: float
    ) -> Optional[int]:
        address_id = await session.execute(self._get_address_stmt(street_id, house, lon, lat))
        return address_id.scalar_one_or_none()