from .. import BaseTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from geoalchemy2.types import Geometry

from src.models.orm.address.addresses_for_user import AddressesForUser


class City(BaseTable):
    __tablename__ = "city"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, nullable=False)
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="city")

class District(BaseTable):
    __tablename__ = "district"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, nullable=False)
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="district")

class Street(BaseTable):
    __tablename__ = "street"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, nullable=False)
    name: Mapped[str]
    address: Mapped["Addresses"] = relationship(back_populates="street")

class Addresses(BaseTable):
    __tablename__ = "Address"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, nullable=False, autoincrement=True)
    city: Mapped["City"] = relationship(back_populates='address')
    city_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("city.id"))

    district: Mapped["District"] = relationship(back_populates='address')
    district_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("district.id"))

    street: Mapped["Street"] = relationship(back_populates='address')
    street_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("street.id"))

    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)

    address_for_user: Mapped[AddressesForUser] = relationship(back_populates="address")
