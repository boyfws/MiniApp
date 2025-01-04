from sqlalchemy import text

def get_point_str(location: str) -> str:
    return location.split(';')[1].split('(')[1].split(')')[0]

def get_coordinates(point_str: str) -> list[float]:
    return [float(x) for x in point_str.split()]

def get_house_string(house: str) -> str:
    return f"house = '{house}' AND " if house else ""


async def check_address_exists(session, location: str, house: str, street_id: int) -> bool:
    point_str = get_point_str(location)
    coordinates = get_coordinates(point_str)
    house_string = get_house_string(house)
    address_exists = await session.execute(
        text(
            f"SELECT EXISTS ("
            f"SELECT 1 FROM address "
            f"WHERE street_id = {street_id} AND "
            f"{house_string}"
            f"ST_Distance(location, ST_SetSRID(ST_MakePoint({coordinates[0]}, {coordinates[1]}), 4326)::geography) <= 0.05"
            f")"
        )
    )
    address_exists_result = address_exists.first()
    return bool(int(address_exists_result[0]))