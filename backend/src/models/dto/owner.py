from pydantic import BaseModel


class OwnerDTO(BaseModel):
    owner_id: int


class OwnerResult(BaseModel):
    ...
