from typing import Optional
from pydantic import BaseModel
from src.models.dto.common import Result


class FavouriteCategoryUpdateRequest(BaseModel):
    user_id: int
    cat_id: int

class FavouriteCategoryUpdateResponse(BaseModel):
    success: Result