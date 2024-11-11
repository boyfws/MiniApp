from pydantic import BaseModel

class AddressDTO(BaseModel):
    city: str
    district: str
    street: str
    house: str

class AddressRequest(BaseModel):
    id: int

class AddressResult(BaseModel):
   id: int