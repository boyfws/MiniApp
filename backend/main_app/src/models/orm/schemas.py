from sqlalchemy import (Integer, String, SmallInteger, BigInteger,
    Boolean, JSON, ARRAY, ForeignKey, Index, CheckConstraint, Numeric, MetaData
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped, as_declarative, DeclarativeBase
from geoalchemy2.types import Geometry

metadata = MetaData()


# @as_declarative(metadata=metadata)
# class Base:
#     """Abstract model with declarative base functionality."""

class Base(DeclarativeBase):
    """Abstract model with declarative base functionality."""
    pass

class LogAction(Base):
    __tablename__ = 'log_actions'

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # Relationships
    activities = relationship("UserActivityLog", back_populates="user")
    fav_categories = relationship("FavCatForUser", back_populates="user")
    fav_restaurants = relationship("FavRestForUser", back_populates="user")
    addresses = relationship("AddressesForUser", back_populates="user")

class Owner(Base):
    __tablename__ = 'owners'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    restaurants = relationship("Restaurant", back_populates='owner')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    # Relationships
    # restaurants = relationship("Restaurant", secondary='restaurants_categories', back_populates="categories")


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('owners.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    main_photo: Mapped[str] = mapped_column(String(1000), nullable=False)
    photos: Mapped[list[str]] = mapped_column(ARRAY(String(1000)), nullable=False)
    ext_serv_link_1: Mapped[str] = mapped_column(String(1000))
    ext_serv_link_2: Mapped[str] = mapped_column(String(1000))
    ext_serv_link_3: Mapped[str] = mapped_column(String(1000))
    ext_serv_rank_1: Mapped[float] = mapped_column(Numeric(3, 2))
    ext_serv_rank_2: Mapped[float] = mapped_column(Numeric(3, 2))
    ext_serv_rank_3: Mapped[float] = mapped_column(Numeric(3, 2))
    ext_serv_reviews_1: Mapped[int] = mapped_column(Integer)
    ext_serv_reviews_2: Mapped[int] = mapped_column(Integer)
    ext_serv_reviews_3: Mapped[int] = mapped_column(Integer)
    tg_link: Mapped[str] = mapped_column(String(1000))
    inst_link: Mapped[str] = mapped_column(String(1000))
    vk_link: Mapped[str] = mapped_column(String(1000))
    orig_phone: Mapped[str] = mapped_column(String(11))
    wapp_phone: Mapped[str] = mapped_column(String(11))
    location: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    address: Mapped[dict] = mapped_column(JSONB, nullable=False)
    categories: Mapped[list[int]] = mapped_column(ARRAY(SmallInteger), nullable=False)

    __table_args__ = (
        CheckConstraint('array_length(photos, 1) >= 3 AND array_length(photos, 1) <= 8'),
        CheckConstraint("LEFT(orig_phone, 1) = '7'"),
        CheckConstraint("LEFT(wapp_phone, 1) = '7'")
    )

    owner = relationship("Owner", back_populates="restaurants")
    activities = relationship("UserActivityLog", back_populates="restaurant")


class UserActivityLog(Base):
    __tablename__ = 'user_activity_logs'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    log_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    action_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('log_actions.id', ondelete='RESTRICT', onupdate='RESTRICT'),
                       nullable=False)
    cat_link: Mapped[int] = mapped_column(SmallInteger, ForeignKey('categories.id', ondelete='RESTRICT', onupdate='RESTRICT'))
    restaurant_link: Mapped[int] = mapped_column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE', onupdate='RESTRICT'))

    # Relationships
    user = relationship("User", back_populates="activities")
    action = relationship("LogAction")
    category = relationship("Category")
    restaurant = relationship("Restaurant", back_populates="activities")


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class District(Base):
    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city_id: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Street(Base):
    __tablename__ = 'street'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district_id: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    street_id: Mapped[int] = mapped_column(Integer, nullable=False)
    house: Mapped[int] = mapped_column(SmallInteger)
    location: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326), nullable=False)



class AddressesForUser(Base):
    __tablename__ = 'addresses_for_user'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    address_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('address.id', ondelete='RESTRICT', onupdate='RESTRICT'),
                        primary_key=True)

    # Relationships
    user = relationship("User", back_populates="addresses")
    address = relationship("Address")


class FavCatForUser(Base):
    __tablename__ = 'fav_cat_for_user'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    cat_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('categories.id', ondelete='RESTRICT', onupdate='RESTRICT'),
                    primary_key=True)

    # Relationships
    user = relationship("User", back_populates="fav_categories")
    category = relationship("Category")


class FavRestForUser(Base):
    __tablename__ = 'fav_rest_for_user'

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    rest_id: Mapped[int] = mapped_column(Integer, ForeignKey('restaurants.id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="fav_restaurants")
    restaurant = relationship("Restaurant")


# Индексы, если необходимо
Index('idx_categories_name', Category.name)
Index('idx_gin_name_search', Restaurant.name)
Index('idx_city_name', City.name)
Index('idx_district_name', District.name)
Index('idx_street_name', Street.name)
Index('idx_address_composite', Address.street_id, Address.house)
Index('idx_addresses_for_user_address_id', AddressesForUser.user_id)
Index('idx_fav_cat_for_user_user_id', FavCatForUser.user_id)
Index('idx_fav_rest_for_user_user_id', FavRestForUser.user_id)
