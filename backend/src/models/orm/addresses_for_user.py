import sqlalchemy as sa
from base import BaseTable, metadata
from sqlalchemy.orm import mapped_column, Mapped, as_declarative


@as_declarative(metadata=metadata)
class AddressesForUser:
    __tablename__ = "Addresses_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    address_id: Mapped[tuple[int, int, int, int]] = mapped_column(sa.ForeignKey("Address.address_for_user_id"), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "address_for_user_id", name="address_for_user_id"),
    )