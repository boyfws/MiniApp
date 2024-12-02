from pydantic import BaseModel

class CategoryDTO(BaseModel):
    name: str

class CategoryResult(BaseModel):
    cat_id: int
