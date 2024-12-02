from typing import List, Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    Name: str
    Price: List[float]
    Description: Optional[str] = None
    Condition: str

class Category(BaseModel):
    category_name: str
    items: List[Item] = Field(..., alias="items")

class MenuDTO(BaseModel):
    restaurant_id: int
    categories: List[Category]
    restaurant_description: str