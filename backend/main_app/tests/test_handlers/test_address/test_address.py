import pytest
from src.models.dto.address import AddressDTO
from tests.test_handlers.fixtures import test_app, truncate_db_api
from tests.common.address import get_addresses

@pytest.mark.parametrize(
    "model", get_addresses()
)
async def test_create(model: AddressDTO, test_app, truncate_db_api):
    response = await test_app.post('/v1/Address/add_address/', json=model.model_dump())
    assert response.status_code == 200
    assert response.json() == {"id": 1}
