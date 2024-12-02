from fastapi import APIRouter

from src.api.v1_test.handlers.address.address import address_router
from src.api.v1_test.handlers.address.addresses_for_user import addresses_for_user_router

router_v1_test = APIRouter(prefix="/v1_test")

router_v1_test.include_router(address_router)
router_v1_test.include_router(addresses_for_user_router)