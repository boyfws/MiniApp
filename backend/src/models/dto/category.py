from typing import Optional
from pydantic import BaseModel

class CategoryRequest(BaseModel):
    name: str
    cat_id: int

class CategoryDTO(BaseModel):
    cat_id: int
    name: str

class CategoryResult(BaseModel):
    ...

# Категории:
# 1) добавить категорию по name
# 2) удалить категорию по name
# 3) редактировать название категории по name
