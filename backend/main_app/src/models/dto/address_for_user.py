from pydantic import BaseModel

class AddressForUserDTO(BaseModel):
    user_id: int
    address_id: int

class AllAddressesForUser(BaseModel):
    user_id: int

class AddressesResponse(BaseModel):
    status: int