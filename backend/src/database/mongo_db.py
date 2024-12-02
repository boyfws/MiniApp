from contextlib import asynccontextmanager
from typing import Optional, Any, Mapping, Callable, AsyncIterator
from typing_extensions import Never, AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorClientSession
from src.config import configuration


class AsyncMongoDB:
    client: AsyncIOMotorClient[Mapping[str, Any]] = AsyncIOMotorClient(configuration.mongo_db.url)
    database: AsyncIOMotorDatabase[Mapping[str, Any]] = client[configuration.mongo_db.database]

    def __init__(self, collection_name: str = configuration.mongo_db.menu_collection):
        self.menu = self.database[collection_name]
        # Сессия БД. будет создаваться каждый раз в конструкции
        # async with AsyncSession as session ...

    async def __aenter__(self) -> AsyncIOMotorClientSession:
        self.session = await self.client.start_session()  # Создаем сессию
        self.session.start_transaction()  # Начинаем сессию

        return self.session

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type:
            await self.session.abort_transaction()  # Если есть ошибка, то откатывается назад

        else:
            await self.session.commit_transaction()  # Иначе коммитим изменения

        # В любом случае закрываем сессию
        await self.session.end_session()

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncMongoDB]:
    yield AsyncMongoDB()