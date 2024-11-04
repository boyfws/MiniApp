import sqlalchemy as sa
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class LogActions(BaseTable):
    __tablename__ = "log_actions"

    description: Mapped[str] = mapped_column(sa.String)

    user_activity_logs: Mapped["UserActivityLogs"] = relationship(back_populates="action")
