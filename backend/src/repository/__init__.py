from typing import Optional, Callable

from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession


async def get_row(session: AsyncSession, stmt) -> int:
    result = await session.execute(stmt)
    return result.scalar_one()

async def get_or_create_item(
        session: AsyncSession,
        search_stmt: Callable,
        create_stmt: Callable,
        *args,
        **kwargs
) -> int:
    """
    Generic function to find or create an item in the database.
    """
    search = await session.execute(search_stmt(*args, **kwargs))
    item_id = search.scalar_one_or_none()
    if item_id is None:
        create = await session.execute(create_stmt(*args, **kwargs))
        item_id = create.scalar_one()
        await session.commit()
    return item_id