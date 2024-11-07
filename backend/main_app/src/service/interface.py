from abc import ABC, abstractmethod
from typing import TypeVar
from src.repository.interface import TablesRepositoryInterface

AbstractModel = TypeVar('AbstractModel')

class ServiceInterface(ABC):

    @abstractmethod
    def __init__(
            self,
            *repos: TablesRepositoryInterface
    ):
        ...

    @abstractmethod
    async def get(
            self,
            model: AbstractModel
    ) -> AbstractModel:
        ...

    @abstractmethod
    async def update(
            self,
            model: AbstractModel
    ) -> AbstractModel:
        ...

    @abstractmethod
    async def delete(
            self,
            model: AbstractModel
    ) -> AbstractModel:
        ...