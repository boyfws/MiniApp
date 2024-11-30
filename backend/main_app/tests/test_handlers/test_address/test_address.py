import pytest

from src.models.dto.address import AddressDTO
from tests.test_handlers.fixtures import test_app # , truncate_db_api
from tests.common.address import get_addresses

@pytest.mark.parametrize(
    "model",
    [
        (get_addresses()[0], ), (get_addresses()[1])
    ]
)
async def test_create(model: AddressDTO, test_app, ):
    await test_app.get('/v1/Address/add_address/', params=model)