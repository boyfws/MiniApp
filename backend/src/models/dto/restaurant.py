from typing import Optional, List, Tuple, Any
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
    user_id: int

class RestaurantRequestBaseModel(BaseModel):
    owner_id: int = Field(..., ge=1)  # Assuming owner ID is always greater than 0
    name: str = Field(..., min_length=1, max_length=100)
    main_photo: str = Field(..., min_length=1, max_length=1000)
    photos: List[str]
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
    address: dict[str, Any] = Field(...)


class RestaurantRequestFullModel(RestaurantRequestBaseModel):
    categories: List[str]


class RestaurantRequestUpdateModel(RestaurantRequestBaseModel):
    categories: List[int]


class RestaurantDTO(RestaurantRequestFullModel):
    favourite_flag: bool


class RestaurantResult(BaseModel):
    rest_id: int


class RestaurantGeoDTO(BaseModel):
    id: int
    name: str
    main_photo: str
    distance: float
    rating: Optional[float] = Field(None, ge=0, le=10)

class GeoSearchResult(RestaurantGeoDTO):
    category: list[int]


class RestaurantGeoSearch(RestaurantGeoDTO):
    category: list[str]
    favourite_flag: bool
