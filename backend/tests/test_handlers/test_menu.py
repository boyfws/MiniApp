from typing import Optional
import pytest

from src.models.dto.menu import MenuDTO
from tests.common.menu import get_menus
from tests.mongo_connector import get_test_db
from tests.test_handlers.fixtures import test_app


@pytest.mark.parametrize(
    "model, expected_id",
    [(get_menus()[0], 1), (get_menus()[1], 2),]
)
async def test_update_menu(model: MenuDTO, expected_id: int, test_app):
    response = await test_app.post("/v1_test/Menu/update_menu_by_rest_id/", json=model.model_dump())
    assert response.status_code == 200
    assert response.json() == expected_id

@pytest.mark.parametrize(
    "rest_id, expected_dto",
    [
        (1, get_menus()[0]),
        (2, get_menus()[1]),
        (4000, None)
    ]
)
async def test_get_menu_by_rest_id(
        rest_id: int,
        expected_dto: Optional[MenuDTO],
        test_app
):
    response = await test_app.get(f"/v1_test/Menu/get_menu_by_rest_id/{rest_id}")
    assert response.status_code == 200
    if expected_dto:
        assert response.json() == expected_dto.model_dump()
    else:
        assert response.json() == expected_dto

@pytest.mark.parametrize("rest_id", [1, 2, 4])
async def test_delete_menu_by_rest_id(
        rest_id: int,
        test_app
):
    response = await test_app.delete(f"/v1_test/Menu/delete_menu_by_rest_id/{rest_id}")
    assert response.status_code == 200

async def test_empty_database():
    """После выполнения всех тестов тестовая база пустая"""
    async with get_test_db() as session:
        document_count = await session.menu.count_documents({})
    assert document_count == 0