import sqlalchemy as sa
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class LogActions(BaseTable):
    __tablename__ = "log_actions"
    description: Mapped[str] = mapped_column(sa.String)
