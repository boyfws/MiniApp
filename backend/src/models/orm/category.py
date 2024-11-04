import sqlalchemy as sa
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Category(BaseTable):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    cat_id: Mapped[int] = relationship("FavouriteCategory", back_populates='cat_id')
    cat_id_activity_logs: Mapped[int] = relationship("UserActivityLogs", back_populates='opt_link')
