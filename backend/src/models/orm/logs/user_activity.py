from datetime import datetime

import sqlalchemy as sa
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class UserActivityLogs(BaseTable):
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    log_time: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    action_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("log_actions.id"), nullable=False)
    opt_link: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("category.id"))