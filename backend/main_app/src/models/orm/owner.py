from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from . import BaseTable


class Owners(BaseTable):
    __tablename__ = "owners"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
