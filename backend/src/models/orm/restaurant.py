import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ARRAY
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class Restaurant(BaseTable):
    __tablename__ = "restaurant"
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    main_photo: Mapped[str] = mapped_column(sa.String, nullable=False)
    photos = mapped_column(ARRAY(sa.String))
    # TODO: вписать сюда какие-то n колонок
    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    address_data = mapped_column(nullable=False) # TODO: разобраться как сюда вставить geojson
    categories = mapped_column(ARRAY(sa.String)) # TODO: вспомнить как писать M:N в этой библе
