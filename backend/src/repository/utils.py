from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.owner import OwnerRepo
from src.repository.user import UserRepo


async def _execute_and_fetch_first(session: AsyncSession, stmt: Any, error_message: str) -> Any:
    """Executes a statement and returns the first result or raises an exception."""
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise Exception(error_message)
    return row

async def create_user_if_does_not_exist(user_repo: UserRepo, user_id: int) -> None:
    is_user = await user_repo.is_user(user_id)
    if not is_user:
        await user_repo.create_user(user_id)

async def create_owner_if_does_not_exist(session_getter: Callable[[], AsyncSession], owner_id: int) -> None:
    # если владельца раньше не было в базе, то добавим
    user_repo = OwnerRepo(session_getter=session_getter)
    is_user = await user_repo.is_owner(owner_id)
    if not is_user:
        await user_repo.create_owner(owner_id)