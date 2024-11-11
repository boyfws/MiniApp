from src.repository.address.address import AddressRepo
from .address import AddressService
from .address_for_user import AddressesForUserService


def get_address_service() -> AddressService:
    return AddressService(repo=AddressRepo())

def get_address_for_user_service() -> AddressesForUserService:
    return AddressesForUserService()

__all__ = [
    "get_address_service", "AddressService",
    "get_address_for_user_service", "AddressesForUserService"
]