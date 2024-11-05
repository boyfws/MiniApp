from pydantic import BaseModel


class AddressForUserRequest(BaseModel):
    user_id: int
    address_id: int

class AddressForUserDTO(BaseModel):
    ...

class AddressForUserResult(BaseModel):
    ...