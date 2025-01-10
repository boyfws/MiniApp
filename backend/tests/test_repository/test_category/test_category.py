import pytest
from tests.conftest import get_session_test
from src.repository.category.category import CategoryRepo

cat_repo = CategoryRepo(session_getter=get_session_test)

@pytest.mark.parametrize("cat_name, cat_id", [("Бургеры", 1), ("Пицца", 3)])
async def test_get_category(cat_name: str, cat_id: int):
    result = await cat_repo.get(cat_name)
    assert result == cat_id

async def test_get_all():
    result = await cat_repo.get_all()
    assert result == ["Бургеры", "Суши", "Пицца", "Паста", "Десерты"]