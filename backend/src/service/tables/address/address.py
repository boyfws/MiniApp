from src.database.sql_session import get_session
from src.models.dto.address import AddressDTO, AddressResult, AddressRequest
from src.repository.tables.address import AddressRepo


class AddressService:
    def __init__(self, repo: AddressRepo):
        self.repo = repo

    async def add_address(self, model: AddressDTO) -> AddressResult:
        async with get_session() as session:
            return await self.repo.add_address(session, model)

    async def delete(self, model: AddressRequest) -> AddressResult:
        async with get_session() as session:
            return await self.repo.delete(session, model)