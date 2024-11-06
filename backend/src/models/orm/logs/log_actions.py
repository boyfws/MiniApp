from sqlalchemy import SmallInteger, String
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class LogActions(BaseTable):
    __tablename__ = "log_actions"

    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    user_activity_logs: Mapped[list["UserActivityLogs"]] = relationship("UserActivityLogs", back_populates="log_action")
