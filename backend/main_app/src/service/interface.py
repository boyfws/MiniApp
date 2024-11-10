from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.repository.interface import TablesRepositoryInterface

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
            model: BaseModel
    ) -> BaseModel:
        ...

    @abstractmethod
    async def update(
            self,
            model: BaseModel
    ) -> BaseModel:
        ...

    @abstractmethod
    async def delete(
            self,
            model: BaseModel
    ) -> BaseModel:
        ...