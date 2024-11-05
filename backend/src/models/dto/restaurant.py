from pydantic import BaseModel


class RestaurantRequestUsingGeoPoint(BaseModel):
    ...

class RestaurantRequestUsingGeoPointAndName(BaseModel):
    name: str
    ...

class RestaurantRequestUsingOwner(BaseModel):
    owner_id: int

class RestaurantRequestUsingID(BaseModel):
    rest_id: int
    user_id: int

class RestaurantRequestFullModel(BaseModel):
    ...

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
