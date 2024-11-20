from pydantic import BaseModel

class AddressDTO(BaseModel):
    city: str
    district: str
    street: str
    house: int
    location: str

class AddressRequest(BaseModel):
    id: int

class AddressResult(BaseModel):
   id: int