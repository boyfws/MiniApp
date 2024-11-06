from src.database.sql_session import get_session
from src.models.dto.category import CategoryResult, CategoryRequestUpdate
from src.repository.tables.category import CategoryRepo
from src.service.tables.interface import ServiceInterface, AbstractModel


class CategoryService(ServiceInterface):
    def __init__(self, repo: CategoryRepo):
        self.repo = repo
    async def delete(self, model: AbstractModel) -> AbstractModel:
        pass

    async def update(self, model: CategoryRequestUpdate) -> CategoryResult:
        async with get_session() as session:
            return await self.repo.update(model=model, session=session)

    async def get(self, model: AbstractModel) -> AbstractModel:
        pass

    async def create(self, model: AbstractModel) -> AbstractModel:
        pass
