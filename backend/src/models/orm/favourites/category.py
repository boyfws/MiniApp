import sqlalchemy as sa
from ..base import metadata
from sqlalchemy.orm import mapped_column, Mapped, as_declarative


@as_declarative(metadata=metadata)
class FavouriteCategory:
    __tablename__ = "fav_cat_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    cat_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("category.id"), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "cat_id", name="fav_cat_for_user"),
    )
