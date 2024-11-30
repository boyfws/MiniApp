from src.models.dto.category import CategoryDTO, CategoryResult
import pytest
from contextlib import nullcontext as does_not_raise, AbstractContextManager
from tests.conftest import get_session_test, cleanup
from src.repository.category.category import CategoryRepo

@pytest.mark.parametrize(
    "model, expected_dto, expectation",
    [
        (CategoryDTO(name="Бургеры"), CategoryResult(cat_id=1), does_not_raise()),
        (CategoryDTO(name="Пицца"), CategoryResult(cat_id=3), does_not_raise())
    ]
)
async def test_get_category(model: CategoryDTO, expected_dto: CategoryResult, expectation: AbstractContextManager):
    async with expectation:
        result = await CategoryRepo(session_getter=get_session_test).get(model)
        assert expected_dto.cat_id == result.cat_id
