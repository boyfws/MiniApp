from contextlib import asynccontextmanager, _AsyncGeneratorContextManager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


from src.config import configuration


async_engine_test: AsyncEngine = _create_async_engine(
    url=configuration.db.build_testdb_connection_str(),
    echo=configuration.debug,
    pool_pre_ping=True
)


AsyncSessionLocalTest = async_sessionmaker(
    bind=async_engine_test,
    expire_on_commit=False,
    class_=AsyncSession
)


@asynccontextmanager
async def get_session_test() -> _AsyncGeneratorContextManager[AsyncSession]:
    async with AsyncSessionLocalTest() as session:
        try:
            # Выполняю транзакцию
            yield session
            await session.commit()

        except Exception:
            # В случае ошибки откатываю все назад
            await session.rollback()
            raise

        finally:
            # В любом случае закрываю соединение
            await session.close()