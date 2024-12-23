from pydantic import BaseModel

class AllFavouriteCategoriesRequest(BaseModel):
    user_id: int

class FavouriteCategoryResponse(BaseModel):
    cat_name: str

class FavouriteCategoryDTO(BaseModel):
    user_id: int
    cat_name: str

class AllFavouriteRestaurantsRequest(BaseModel):
    user_id: int

class FavouriteRestaurantResponse(BaseModel):
    rest_id: int

class FavouriteRestaurantDTO(BaseModel):
    user_id: int
    rest_id: int
