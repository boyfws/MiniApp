import pytest

from src.models.dto.category import CategoryDTO, CategoryResult
from src.repository.category.category import CategoryRepo
from src.service.category import CategoryService
from tests.sql_connector import get_session_test

@pytest.mark.parametrize(
    "model, expected_dto",
    [
        (CategoryDTO(name="Бургеры"), CategoryResult(cat_id=1)),
        (CategoryDTO(name="Пицца"), CategoryResult(cat_id=3))
    ]
)
async def test_get_category(model: CategoryDTO, expected_dto: CategoryResult):
    result = await CategoryService(repo=CategoryRepo(session_getter=get_session_test)).get(model)
    assert result == expected_dto