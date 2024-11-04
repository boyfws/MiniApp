from base import BaseTable, metadata
from sqlalchemy.orm import Mapped, mapped_column, as_declarative, relationship
import sqlalchemy as sa
from geoalchemy2.types import Geometry

class City(BaseTable):
    __tablename__ = "city"
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="house")

class District(BaseTable):
    __tablename__ = "district"
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="house")

class Street(BaseTable):
    __tablename__ = "street"
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="house")

class House(BaseTable):
    __tablename__ = "house"
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="house")


@as_declarative(metadata=metadata)
class Addresses(BaseTable):
    __tablename__ = "Address"
    city: Mapped["City"] = relationship(back_populates='address')
    city_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("city.id"))

    district: Mapped["District"] = relationship(back_populates='address')
    district_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("district.id"))

    street: Mapped["Street"] = relationship(back_populates='address')
    street_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("street.id"))

    house: Mapped["House"] = relationship(back_populates='address')
    house_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("house.id"))

    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("city_id", "district_id", "street_id", "house_id", name='address_id'),
    )

    address_for_user: Mapped["AddressesForUser"] = relationship(back_populates="address")
