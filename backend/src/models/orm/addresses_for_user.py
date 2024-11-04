import sqlalchemy as sa
from base import metadata
from sqlalchemy.orm import mapped_column, Mapped, as_declarative, relationship


@as_declarative(metadata=metadata)
class AddressesForUser:
    __tablename__ = "Addresses_for_user"
    user_id: Mapped[int] = relationship("User", back_populates='id')
    address_id: Mapped[tuple[int, int, int, int]] = relationship("Addresses", back_populates='address_id')
    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "address_id", name="address_for_user_id"),
    )