from src.models.dto.address import AddressDTO
from src.repository.address.address import AddressRepo


class AddressService:
    def __init__(self, repo: AddressRepo):
        self.repo = repo

    async def add_address(self, model: AddressDTO) -> int:
        return await self.repo.add_address(model)

    async def delete(self, model: AddressDTO) -> None:
        address_id = ...
        await self.repo.delete(address_id)