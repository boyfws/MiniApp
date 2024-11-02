from base import BaseTable, metadata
from sqlalchemy.orm import Mapped, mapped_column, as_declarative
import sqlalchemy as sa
from geoalchemy2.types import Geometry

class City(BaseTable):
    __tablename__ = "city"
    name: Mapped[str]

class District(BaseTable):
    __tablename__ = "district"
    name: Mapped[str]

class Street(BaseTable):
    __tablename__ = "street"
    name: Mapped[str]

class House(BaseTable):
    __tablename__ = "house"
    name: Mapped[str]


@as_declarative(metadata=metadata)
class Addresses(BaseTable):
    __tablename__ = "Address"
    city: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("city.id"))
    district: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("district.id"))
    street: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("street.id"))
    house: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("house.id"))
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("city", "district", "street", "house", name='address_for_user_id'),
    )
