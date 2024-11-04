from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class UserActivityLogs(BaseTable):
    __tablename__ = "user_activity_logs"

    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="user_activity_logs")

    action_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("log_actions.id"), nullable=False)
    action: Mapped["LogActions"] = relationship(back_populates="user_activity_logs")

    category_opt_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey("category.id"))
    category: Mapped[Optional["Category"]] = relationship(back_populates="user_activity_logs")

    rest_opt_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey('restaurant.id'))
    restaurant: Mapped[Optional["Restaurant"]] = relationship(back_populates="user_activity_logs")

    log_time: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)