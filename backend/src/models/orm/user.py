from sqlalchemy.orm import Mapped, relationship, mapped_column

from base import BaseTable


class User(BaseTable):
    __tablename__ = "user"

    address_for_user: Mapped["AddressesForUser"] = relationship(back_populates="user")
    fav_rest_for_user: Mapped["FavouriteRestaurant"] = relationship(back_populates="user")
    fav_cat_for_user: Mapped["FavouriteCategory"] = relationship(back_populates="user")
    user_activity_logs: Mapped["UserActivityLogs"] = relationship(back_populates="user")

