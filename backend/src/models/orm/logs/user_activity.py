from sqlalchemy import BigInteger, ForeignKey, SmallInteger, Integer

from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped, relationship


class UserActivityLogs(BaseTable):
    __tablename__ = "user_activity_logs"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger,
                                                ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT'),
                                                nullable=False)
    log_time: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False)  # UNIX timestamp GMT+0
    action_id: Mapped[SmallInteger] = mapped_column(SmallInteger, ForeignKey('log_actions.id', ondelete='RESTRICT',
                                                                             onupdate='RESTRICT'), nullable=False)
    cat_link: Mapped[SmallInteger] = mapped_column(SmallInteger, ForeignKey('categories.id', ondelete='RESTRICT',
                                                                            onupdate='RESTRICT'))
    restaurant_link: Mapped[Integer] = mapped_column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE',
                                                                         onupdate='RESTRICT'))

    log_action: Mapped["LogActions"] = relationship("LogAction", back_populates="user_activity_logs")
    user: Mapped["Users"] = relationship("Users", back_populates="activity_logs")