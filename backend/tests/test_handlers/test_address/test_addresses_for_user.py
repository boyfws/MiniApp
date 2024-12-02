import pytest

from src.models.dto.address_for_user import AllAddressesForUser, AddressForUserDTO
from tests.test_handlers.fixtures import test_app
from tests.test_repository.test_address.test_addresses_for_user import create_db_values_1, truncate_db

@pytest.mark.parametrize(
    "model",
    [
        AddressForUserDTO(user_id=1, address_id=1)
    ]
)
async def test_add_address_for_user(model: AddressForUserDTO, test_app, create_db_values_1, truncate_db):
    response = await test_app.post('/v1_test/AddressesForUser/add_address/', json=model.model_dump())
    assert response.status_code == 200

@pytest.mark.parametrize(
    "model",
    [
        AddressForUserDTO(user_id=1, address_id=1),
        AddressForUserDTO(user_id=1, address_id=2)
    ]
)
async def test_delete(model: AddressForUserDTO, test_app, create_db_values_1, truncate_db):
    response = await test_app.delete('/v1_test/AddressesForUser/delete_address/', json=model.model_dump())
    assert response.status_code == 200