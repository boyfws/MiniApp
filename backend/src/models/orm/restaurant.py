import sqlalchemy as sa
from geoalchemy2 import Geometry
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class Restaurant(BaseTable):
    __tablename__ = "restaurant"
    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("owner.id"), nullable=False)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    main_photo: Mapped[str] = mapped_column(sa.String, nullable=False)
    photos = mapped_column(sa.ARRAY(sa.String))

    # TODO: вписать сюда n таблиц

    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    address_data = mapped_column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=False) # TODO: разобраться как сюда вставить geojson
    categories: Mapped[list[int]] = mapped_column(sa.ARRAY(sa.Integer)) # TODO: вспомнить как писать M:N в этой библе
