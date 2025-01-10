import pytest
from sqlalchemy import text

from src.models.dto.address import AddressDTO
from tests.sql_connector import get_session_test
from tests.test_handlers.fixtures import test_app
from tests.common.address import get_addresses

@pytest.mark.parametrize(
    "model, expected_id",
    [
        (get_addresses()[0], 1),
        (get_addresses()[1], 2)
    ]
)
async def test_create(model: AddressDTO, expected_id: int, test_app):
    response = await test_app.post('/v1_test/Address/add_address/', json=model.model_dump())
    assert response.status_code == 200
    assert expected_id == response.json()

# @pytest.mark.parametrize(
#      "address_id",
#      [1, 2]
# )
# async def test_delete(address_id: int, test_app):
#      response = await test_app.delete(f'/v1_test/Address/delete_address/{address_id}')
#      assert response.status_code == 200
#      async with get_session_test() as session:
#          count = await session.execute(text(f"SELECT COUNT(*) FROM address WHERE id = {address_id}"))
#          assert count.scalar() == 0

