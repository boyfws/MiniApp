from pydantic import BaseModel

from src.models.dto.address import AddressDTO


class AddressForUserDTO(BaseModel):
    user_id: int
    address_id: int

class DeleteAddressForUser(AddressDTO):
    user_id: int

class AllAddressesForUser(BaseModel):
    user_id: int