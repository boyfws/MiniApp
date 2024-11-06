from sqlalchemy import SmallInteger, String

from src.models.orm.base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Category(BaseTable):
    __tablename__ = "category"

    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
