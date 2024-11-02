import sqlalchemy as sa
from ..base import BaseTable
from sqlalchemy.orm import mapped_column, Mapped

class FavouriteCategory(BaseTable):
    __tablename__ = "fav_cat_for_user"
    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    cat_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("category.id"), nullable=False)
