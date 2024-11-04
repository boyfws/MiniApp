import sqlalchemy as sa
from ..base import metadata
from sqlalchemy.orm import mapped_column, Mapped, as_declarative


@as_declarative(metadata=metadata)
class FavouriteRestaurant:
    __tablename__ = "fav_rest_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    cat_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("category.id"), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "cat_id", name="fav_rest_for_user_id"),
    )