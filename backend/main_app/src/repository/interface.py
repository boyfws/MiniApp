from abc import abstractmethod, ABC
from typing import TypeVar

from pydantic import BaseModel

AbstractAsyncSession = TypeVar('AbstractAsyncSession')


class TablesRepositoryInterface(ABC):

    __slots__ = ('session', 'model',)

    @abstractmethod
    async def get(
            self,
            session: AbstractAsyncSession,
            model: BaseModel
    ) -> BaseModel:
        ...

    @abstractmethod
    async def update(
            self,
            session: AbstractAsyncSession,
            model: BaseModel
    ) -> BaseModel:
        ...

    @abstractmethod
    async def delete(
            self,
            session: AbstractAsyncSession,
            model: BaseModel
    ) -> BaseModel:
        ...