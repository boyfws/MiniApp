from typing import Optional, List, Tuple
from pydantic import BaseModel, Field, field_validator


class Point(BaseModel):
    lon: float
    lat: float

class RestaurantRequestUsingGeoPointAndName(BaseModel):
    point: Point
    name_pattern: str

class RestaurantRequestUsingOwner(BaseModel):
    owner_id: int

class RestaurantRequestUsingID(BaseModel):
    rest_id: int

class RestaurantRequestFullModel(BaseModel):
    owner_id: int = Field(..., ge=1)  # Assuming owner ID is always greater than 0
    name: str = Field(..., min_length=1, max_length=100)
    main_photo: str = Field(..., min_length=1, max_length=1000)
    photos: List[str] = Field(..., min_items=3, max_items=8)
    ext_serv_link_1: Optional[str] = Field(None, max_length=1000)
    ext_serv_link_2: Optional[str] = Field(None, max_length=1000)
    ext_serv_link_3: Optional[str] = Field(None, max_length=1000)
    ext_serv_rank_1: Optional[float] = Field(None, ge=0, le=10)  # Assuming a reasonable range
    ext_serv_rank_2: Optional[float] = Field(None, ge=0, le=10)  # Assuming a reasonable range
    ext_serv_rank_3: Optional[float] = Field(None, ge=0, le=10)  # Assuming a reasonable range
    ext_serv_reviews_1: Optional[int] = Field(None, ge=0)
    ext_serv_reviews_2: Optional[int] = Field(None, ge=0)
    ext_serv_reviews_3: Optional[int] = Field(None, ge=0)
    tg_link: Optional[str] = Field(None, max_length=1000)
    inst_link: Optional[str] = Field(None, max_length=1000)
    vk_link: Optional[str] = Field(None, max_length=1000)
    orig_phone: str = Field(..., min_length=11, max_length=11)
    wapp_phone: str = Field(..., min_length=11, max_length=11)
    location: str
    address: dict = Field(...)  # Using dict instead of JSON, more straightforward
    categories: List[int] = Field(..., min_items=1)  # Assuming at least one category

class RestaurantResponse(BaseModel):
    ...

class RestaurantResult(BaseModel):
    rest_id: int


class RestaurantGeoSearch(BaseModel):
    id: int
    name: str
    main_photo: str
    distance: float

# Summary:
# Для ресторана:
# 1) получить ресторан по rest_id + запрос в user_fav по user_id
# 2) получить ресторан по x, y, limit + запрос в user_fav по user_id
# 3) получить ресторан по x, y, name_pattern + запрос в user_fav по user_id
# 4) редактирование ресторана по rest_id + полностью pydantic модель этой бд
# 5) создание ресторана по полной pydantic модели
# 6) удаление ресторана по rest_id
# 7) удаление всех ресторанов владельца
# 8) получение всех ресторанов владельца
