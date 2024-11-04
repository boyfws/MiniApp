from base import BaseTable, metadata
from sqlalchemy.orm import Mapped, mapped_column, as_declarative, relationship
import sqlalchemy as sa
from geoalchemy2.types import Geometry

class City(BaseTable):
    __tablename__ = "city"
    name: Mapped[str]
    address: Mapped[int] = relationship("Addresses", back_populates="city")

class District(BaseTable):
    __tablename__ = "district"
    name: Mapped[str]
    address: Mapped[int] = relationship("Addresses", back_populates="district")

class Street(BaseTable):
    __tablename__ = "street"
    name: Mapped[str]
    address: Mapped[int] = relationship("Addresses", back_populates="street")

class House(BaseTable):
    __tablename__ = "house"
    name: Mapped[str]
    address: Mapped[int] = relationship("Addresses", back_populates="house")


@as_declarative(metadata=metadata)
class Addresses(BaseTable):
    __tablename__ = "Address"
    city: Mapped[int] = relationship("City", back_populates='id')
    district: Mapped[int] = relationship("District", back_populates='id')
    street: Mapped[int] = relationship("Street", back_populates='id')
    house: Mapped[int] = relationship("House", back_populates='id')
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("city", "district", "street", "house", name='address_for_user_id'),
    )
