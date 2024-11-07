from pydantic import BaseModel


class FavouriteCategoryRequest(BaseModel):
    user_id: int
    cat_id: int

class AllFavouriteCategoriesRequest(BaseModel):
    user_id: int

class FavouriteCategoryResponse(BaseModel):
    ...

class FavouriteCategoryDTO(BaseModel):
    ...

class FavouriteRestaurantRequest(BaseModel):
    user_id: int
    rest_id: int

class AllFavouriteRestaurantsRequest(BaseModel):
    user_id: int

class FavouriteRestaurantResponse(BaseModel):
    ...

class FavouriteRestaurantDTO(BaseModel):
    ...

# Для любимых категорий:
# 1) получить все любимые категории по user_id
# 2) удалить все любимые категории по user_id
# 3) добавить любимую категорию по user_id, name
# 4) удалить любимую категорию по user_id, name
