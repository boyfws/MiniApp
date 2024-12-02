from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.repository.address.address import AddressRepo


class AddressService:
    def __init__(self, repo: AddressRepo):
        self.repo = repo

    async def add_address(self, model: AddressDTO) -> AddressResult:
        return await self.repo.add_address(model)

    async def delete(self, model: AddressRequest) -> AddressResult:
        return await self.repo.delete(model)