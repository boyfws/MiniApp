import sqlalchemy as sa
from sqlalchemy import SmallInteger
from sqlalchemy.orm import mapped_column, Mapped
from .. import BaseTable

class FavouriteCategory(BaseTable):
    __tablename__ = "fav_cat_for_user"
    id: Mapped[SmallInteger] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    cat_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("category.id"), nullable=False)
    __table_args__ = (
        sa.PrimaryKeyConstraint("user_id", "cat_id", name="fav_cat_for_user"),
    )
