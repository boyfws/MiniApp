from pydantic import BaseModel

class AddressDTO(BaseModel):
    region: str
    city: str
    district: str
    street: str
    house: int
    location: str

class AddressRequest(BaseModel):
    id: int

class AddressResult(BaseModel):
   id: int