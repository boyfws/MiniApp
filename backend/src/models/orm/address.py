from base import BaseTable
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from geoalchemy2.types import Geometry


class Addresses(BaseTable):
    __tablename__ = "Address"
    city: Mapped[int] = mapped_column(sa.Integer)
    district: Mapped[int] = mapped_column(sa.Integer)
    street: Mapped[int] = mapped_column(sa.Integer)
    house: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
