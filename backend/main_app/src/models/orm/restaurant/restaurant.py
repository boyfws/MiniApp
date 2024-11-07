import sqlalchemy as sa
from geoalchemy2 import Geometry
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Restaurant(BaseTable):
    __tablename__ = "restaurant"
    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("owner.id"), nullable=False)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    main_photo: Mapped[str] = mapped_column(sa.String, nullable=False)
    photos: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=False)
    website: Mapped[str] = mapped_column(sa.String)

    ext_serv_link_1: Mapped[str] = mapped_column(sa.String)
    ext_serv_rank_1: Mapped[float] = mapped_column(sa.Float)
    ext_serv_num_rev_1: Mapped[int] = mapped_column(sa.Integer)

    ext_serv_link_2: Mapped[str] = mapped_column(sa.String)
    ext_serv_rank_2: Mapped[float] = mapped_column(sa.Float)
    ext_serv_num_rev_2: Mapped[int] = mapped_column(sa.Integer)

    ext_serv_link_3: Mapped[str] = mapped_column(sa.String)
    ext_serv_rank_3: Mapped[float] = mapped_column(sa.Float)
    ext_serv_num_rev_3: Mapped[int] = mapped_column(sa.Integer)

    location = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    address_data = mapped_column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=False) # TODO: разобраться как сюда вставить geojson
    categories: Mapped[list[int]] = relationship()
