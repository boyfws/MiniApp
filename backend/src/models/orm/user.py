from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column
from . import BaseTable
from .logs.user_activity import UserActivityLogs


class Users(BaseTable):
    __tablename__ = "users"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    # address_for_user: Mapped["AddressesForUser"] = relationship(back_populates="user")
    # fav_rest_for_user: Mapped["FavouriteRestaurant"] = relationship(back_populates="user")
    # fav_cat_for_user: Mapped["FavouriteCategory"] = relationship(back_populates="user")
    user_activity_logs: Mapped[list[UserActivityLogs]] = relationship("UserActivityLogs", back_populates="users")

