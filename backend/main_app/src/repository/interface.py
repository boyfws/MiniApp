from abc import abstractmethod, ABC
from contextlib import _AsyncGeneratorContextManager
from typing import TypeVar, Callable

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql_session import get_session

AbstractAsyncSession = TypeVar('AbstractAsyncSession')


class TablesRepositoryInterface(ABC):

    __slots__ = ('session_getter', 'model',)

    def __init__(self, session_getter: Callable[[], _AsyncGeneratorContextManager[AsyncSession]] = get_session) -> None:
        """
        :session_getter Нужно передать коннектор к базе данных
        """
        self.session_getter = session_getter