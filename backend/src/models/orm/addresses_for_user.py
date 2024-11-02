import sqlalchemy as sa
from base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped


class AddressesForUser(BaseTable):
    __tablename__ = "Addresses_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("address.id"), nullable=False)