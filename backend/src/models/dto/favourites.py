from pydantic import BaseModel


class FavouriteCategoryDTO(BaseModel):
    user_id: int
    cat_name: str

class FavouriteCategoryRequest(BaseModel):
    user_id: int
    cat_id: int

class FavouriteRestaurantDTO(BaseModel):
    user_id: int
    rest_id: int
