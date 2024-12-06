import pytest

from src.models.dto.category import CategoryDTO, CategoryResult
from src.repository.category.category import CategoryRepo
from src.service.category import CategoryService
from tests.sql_connector import get_session_test

cat_service = CategoryService(repo=CategoryRepo(session_getter=get_session_test))

@pytest.mark.parametrize(
    "model, expected_dto",
    [
        (CategoryDTO(name="Бургеры"), CategoryResult(cat_id=1)),
        (CategoryDTO(name="Пицца"), CategoryResult(cat_id=3))
    ]
)
async def test_get_category(model: CategoryDTO, expected_dto: CategoryResult):
    result = await cat_service.get(model)
    assert result == expected_dto

async def test_get_all():
    result = await cat_service.get_all()
    assert [model.model_dump() for model in result] ==  [
        {"name": "Бургеры"}, {"name": "Суши"},
        {"name": "Пицца"}, {"name": "Паста"}, {"name": "Десерты"}
    ]