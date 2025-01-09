from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user import UserRepo


async def _execute_and_fetch_first(session: AsyncSession, stmt: Any, error_message: str) -> Any:
    """Executes a statement and returns the first result or raises an exception."""
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise Exception(error_message)
    return row

async def create_user_if_does_not_exist(session_getter: Callable[[], AsyncSession], user_id: int) -> None:
    # если юзера раньше не было в базе, то добавим
    user_repo = UserRepo(session_getter=session_getter)
    is_user = await user_repo.is_user(user_id)
    if not is_user:
        await user_repo.create_user(user_id)
