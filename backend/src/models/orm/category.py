import sqlalchemy as sa
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Category(BaseTable):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    cat_id_activity_logs: Mapped["UserActivityLogs"] = relationship(back_populates='opt_link')
