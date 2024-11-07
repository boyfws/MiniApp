from abc import abstractmethod, ABC
from typing import TypeVar

AbstractModel = TypeVar('AbstractModel')
AbstractAsyncSession = TypeVar('AbstractAsyncSession')


class TablesRepositoryInterface(ABC):

    __slots__ = ('session', 'model',)

    @abstractmethod
    async def get(
            self,
            session: AbstractAsyncSession,
            model: AbstractModel
    ) -> AbstractModel:
        ...

    @abstractmethod
    async def update(
            self,
            session: AbstractAsyncSession,
            model: AbstractModel
    ) -> AbstractModel:
        ...

    @abstractmethod
    async def delete(
            self,
            session: AbstractAsyncSession,
            model: AbstractModel
    ) -> AbstractModel:
        ...