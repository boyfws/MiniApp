from pydantic import BaseModel


class FavouriteCategoryRequest(BaseModel):
    ...

class AllFavouriteCategoriesRequest(BaseModel):
    ...

class FavouriteCategoryResponse(BaseModel):
    ...

class FavouriteCategoryDTO(BaseModel):
    ...

class FavouriteRestaurantRequest(BaseModel):
    ...

class AllFavouriteRestaurantsRequest(BaseModel):
    ...

class FavouriteRestaurantResponse(BaseModel):
    ...

class FavouriteRestaurantDTO(BaseModel):
    ...
