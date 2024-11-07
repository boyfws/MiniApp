import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .. import BaseTable
from src.models.orm.user import Users

class AddressesForUser(BaseTable):
    __tablename__ = "Addresses_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    user: Mapped[Users] = relationship(back_populates="address_for_user")

    address_id: Mapped[tuple[int, int, int, int]] = mapped_column(sa.ForeignKey("Address.address_id"), nullable=False)
    address: Mapped["Addresses"] = relationship(back_populates="address_for_user")

    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "address_id", name="address_for_user_id"),
    )