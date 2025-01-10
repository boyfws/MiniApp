import pytest

from src.repository.category.category import CategoryRepo
from src.service.category import CategoryService
from tests.sql_connector import get_session_test

cat_service = CategoryService(repo=CategoryRepo(session_getter=get_session_test))

@pytest.mark.parametrize("cat_name, cat_id", [("Бургеры", 1), ("Пицца", 3)])
async def test_get_category(cat_name: str, cat_id: int):
    result = await cat_service.get(cat_name)
    assert result == cat_id

async def test_get_all():
    result = await cat_service.get_all()
    assert result ==  ["Бургеры", "Суши", "Пицца", "Паста", "Десерты"]