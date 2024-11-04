import sqlalchemy as sa
from base import metadata
from sqlalchemy.orm import mapped_column, Mapped, as_declarative, relationship


@as_declarative(metadata=metadata)
class AddressesForUser:
    __tablename__ = "Addresses_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="address_for_user")

    address_id: Mapped[tuple[int, int, int, int]] = mapped_column(sa.ForeignKey("Address.address_id"), nullable=False)
    address: Mapped["Addresses"] = relationship(back_populates="address_for_user")

    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "address_id", name="address_for_user_id"),
    )