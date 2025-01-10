import pytest

from tests.test_handlers.fixtures import test_app

@pytest.mark.parametrize(
    "category_name, expected_id",
    [
        ("Бургеры", 1),
        ("Пицца", 3)
    ]
)
async def test_get_category(category_name: str, expected_id: int, test_app):
    response = await test_app.get(f"/v1_test/Category/get_category_id/{category_name}")
    assert response.status_code == 200
    assert response.json() == expected_id

async def test_get_all(test_app):
    response = await test_app.get(f"/v1_test/Category/get_all_categories/{1}")
    assert response.status_code == 200
    assert response.json() == ["Бургеры", "Суши", "Пицца", "Паста", "Десерты"]