from pydantic import BaseModel


class OwnerRequest(BaseModel):
    name: str


class OwnerRequestUpdate(BaseModel):
    old_name: str
    new_name: str

class OwnerResult(BaseModel):
    id: int
