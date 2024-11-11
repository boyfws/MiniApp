from pydantic import BaseModel

class CategoryRequestByName(BaseModel):
    name: str

class CategoryDTO(BaseModel):
    id: int
    name: str

class CategoryResult(BaseModel):
    cat_id: int
