from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


async def _execute_and_fetch_first(session: AsyncSession, stmt: Any, error_message: str) -> Any:
    """Executes a statement and returns the first result or raises an exception."""
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise Exception(error_message)
    return row