import sqlalchemy as sa
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class Category(BaseTable):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(sa.String, nullable=False)