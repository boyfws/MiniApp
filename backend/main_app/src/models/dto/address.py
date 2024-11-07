from pydantic import BaseModel

class AddressDTO(BaseModel):
    city: str
    district: str
    street: str
    house: str
    location: tuple[int, int]

class AddressRequest(BaseModel):
    id: int

class AddressResult(BaseModel):
    id: int