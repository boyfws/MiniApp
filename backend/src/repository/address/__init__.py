from sqlalchemy import text, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.orm.schemas import Region, City, District, Street
from src.repository import get_or_create_item


def get_point_str(location: str) -> str:
    return location.split(';')[1].split('(')[1].split(')')[0]

def get_coordinates(point_str: str) -> list[float]:
    return [float(x) for x in point_str.split()]

def get_house_string(house: str) -> str:
    return f"house = '{house}' AND " if house else ""


async def check_address_exists(
        session: AsyncSession,
        location: str,
        house: str,
        street_id: int,
) -> bool:
    """
    Check if an address with similar parameters already exists.
    """
    point_str = get_point_str(location)
    coordinates = get_coordinates(point_str)
    house_string = get_house_string(house)

    address_stmt = text(
        f"SELECT id FROM address "
        f"WHERE street_id = {street_id} AND "
        f"{house_string}"
        f"ST_Distance(location, ST_SetSRID(ST_MakePoint({coordinates[0]}, {coordinates[1]}), 4326)::geography) <= 0.05"
    )

    result = await session.execute(address_stmt)
    return result.scalar_one_or_none() is not None

async def _get_or_create_region(session: AsyncSession, region_name: str) -> int:
    return await get_or_create_item(
        session,
        lambda name: select(Region.id).where(Region.name == name),
        lambda name: insert(Region).values(name=name).returning(Region.id),
        region_name
    )

async def _get_or_create_city(session: AsyncSession, city_name: str, region_id: int) -> int:
    return await get_or_create_item(
        session,
        lambda city, reg_id: select(City.id).where(City.region_id == reg_id).where(City.name == city),
        lambda city, reg_id: insert(City).values(name=city, region_id=reg_id).returning(City.id),
        city_name,
        region_id
    )

async def _get_or_create_district(session: AsyncSession, district_name: str, city_id: int) -> int:
    return await get_or_create_item(
        session,
        lambda district, city: select(District.id).where(District.city_id == city).where(District.name == district),
        lambda district, city: insert(District).values(name=district, city_id=city).returning(District.id),
        district_name,
        city_id
    )

async def _get_or_create_street(session: AsyncSession, street_name: str, district_id: int) -> int:
    return await get_or_create_item(
        session,
        lambda street, district: select(Street.id).where(Street.district_id == district).where(
            Street.name == street),
        lambda street, district: insert(Street).values(name=street, district_id=district).returning(Street.id),
        street_name,
        district_id
    )