from typing import Optional

from geoalchemy2 import Geometry
from pydantic import BaseModel
from sqlalchemy import JSON


class RestaurantRequestUsingGeoPoint(BaseModel):
    ...

class RestaurantRequestUsingGeoPointAndName(BaseModel):
    ...

class RestaurantRequestUsingOwner(BaseModel):
    owner_id: int

class RestaurantRequestUsingID(BaseModel):
    rest_id: int

class RestaurantRequestFullModel(BaseModel):
    id: Optional[int]
    owner_id: int
    name: str
    main_photo: str
    photos: list[str]
    ext_serv_link_1: str
    ext_serv_link_2: str
    ext_serv_link_3: str
    ext_serv_rank_1: float
    ext_serv_rank_2: float
    ext_serv_rank_3: float
    ext_serv_reviews_1: int
    ext_serv_reviews_2: int
    ext_serv_reviews_3: int
    tg_link: str
    inst_link: str
    vk_link: str
    orig_phone: str
    wapp_phone: str
    location: int #Geometry(geometry_type='POINT', srid=4326)
    address: int #JSON
    categories: list[int]

class RestaurantResponse(BaseModel):
    ...

class RestaurantResult(BaseModel):
    ...

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
