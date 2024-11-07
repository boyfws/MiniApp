from src.repository.address.address import AddressRepo
from .address import AddressService

def get_address_service() -> AddressService:
    return AddressService(repo=AddressRepo())

__all__ = [
    "get_address_service", "AddressService"
]